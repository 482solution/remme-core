# Copyright 2018 REMME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

import hashlib
from google.protobuf.text_format import ParseError
from sawtooth_processor_test.message_factory import MessageFactory
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.handler import TransactionHandler


class BasicHandler(TransactionHandler):
    def __init__(self, name, versions):
        self._family_name = name
        self._family_versions = versions
        self._prefix = hashlib.sha512(self._family_name.encode('utf-8')).hexdigest()[:6]

    @property
    def family_name(self):
        return self._family_name

    @property
    def family_versions(self):
        return self._family_versions

    @property
    def namespaces(self):
        return [self._prefix]

    def apply(self, transaction, context):
        pass

    def process_state(self, context, signer_pubkey, transaction_payload):
        return {}

    def get_message_factory(self, signer=None):
        return MessageFactory(
            family_name=self._family_name,
            family_version=self._family_versions[-1],
            namespace=self._prefix,
            signer=signer
        )

    def process_apply(self, context, pb_class, transaction):
        transaction_payload = pb_class()
        transaction_payload.ParseFromString(transaction.payload)
        updated_state = self.process_state(context, transaction.header.signer_public_key, transaction_payload)
        self._store_state(context, updated_state)

    def make_address(self, appendix):
        address = self._prefix + appendix
        try:
            assert isinstance(address, str)
            assert len(address) == 70
            int(address, 16)
        except (AssertionError, ValueError):
            raise InternalError('Addresses should be 70 characters long. Prefix: {}. Appendix: {}.'
                                .format(self._prefix, appendix))
        return address

    def make_address_from_data(self, data):
        appendix = hashlib.sha512(data.encode('utf-8')).hexdigest()[:64]
        return self.make_address(appendix)

    def get_data(self, context, pb_class, address):
        raw_data = context.get_state([address])
        if raw_data:
            try:
                data = pb_class()
                data.ParseFromString(raw_data[0].data)
                return data
            except IndexError:
                return None
            except ParseError:
                raise InternalError('Failed to deserialize data')
        else:
            return None

    def _store_state(self, context, updated_state):
        addresses = context.set_state({k: v.SerializeToString() for k, v in updated_state.items()})
        if len(addresses) < len(updated_state):
            raise InternalError('Failed to update all of states. Updated: {}. Full list of states to update: {}.'
                                .format(addresses, updated_state.keys()))
