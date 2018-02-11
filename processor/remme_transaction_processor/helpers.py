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
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_processor_test.message_factory import MessageFactory
from transaction_pb2 import Transaction

# TODO: think about more logging in helper functions


class BasicHandler(TransactionHandler):
    def __init__(self, name, versions):
        self._family_name = name
        self._family_versions = versions
        self._prefix = hashlib.sha512(self.FAMILY_NAME.encode('utf-8')).hexdigest()[0:6]

    @property
    def family_name(self):
        return self._family_name

    @property
    def family_versions(self):
        return self._family_versions

    @property
    def namespaces(self):
        return [self._prefix]

    # methods to modify in custom handler

    def apply(self, transaction, context):
        pass

    def process_state(self, signer, method, data, state):
        pass

    def get_factory(self, signer=None):
        return MessageFactory(
            family_name=self._family_name,
            family_version=self._family_versions[-1],
            namespace=self._prefix,
            signer=signer
        )

    def process_apply(self, transaction, context, pb_class):
        self.context = context
        # signer is taken from header
        # transaction follows Transaction proto
        signer, method, data = self._decode_transaction(transaction)

        state = self.get_data(pb_class, signer)

        updated_state = self.process_state(signer, method, data, state)
        adresses = self.context.set_state(updated_state)

        if len(adresses) < len(updated_state):
            raise InternalError("State Error")

    def make_address(self, appendix):
        return self._prefix + appendix

    def _decode_transaction(self, transaction):
        transaction_payload = Transaction()
        try:
            transaction_payload.ParseFromString(transaction.payload)
        except:
            raise InvalidTransaction("Invalid payload serialization")

        signer = self.make_address(transaction.header.signer_public_key)
        data = transaction_payload.data
        method = transaction_payload.method

        return signer, method, data

    def get_data(self, pb_class, signer):
        data = pb_class()
        data_address = self.make_address(signer)
        raw_data = self.context.get_state([data_address])
        try:
            data.ParseFromString(raw_data[0])
        except IndexError:
            return None, None
        except:
            raise InternalError("Failed to deserialize data")
        return data

    # used from child handlers
    def store_state(self, updated_state, data_pb_instance, key):
        serialized = data_pb_instance.SerializeToString(updated_state)
        data_address = self.make_address(signer)
        adresses = self.context.set_state({ data_address: serialized })
        if len(adresses) < 1:
            raise InternalError("State Error")
