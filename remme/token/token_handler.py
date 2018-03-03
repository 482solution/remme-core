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

import logging
from google.protobuf.text_format import ParseError
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from remme.protos.token_pb2 import Account, GenesisStatus, TokenMethod, GenesisPayload, \
    TransferPayload
from remme.shared.basic_handler import *

LOGGER = logging.getLogger(__name__)

ZERO_ADDRESS = '0' * 64

FAMILY_NAME = 'token'
FAMILY_VERSIONS = ['0.1']


# TODO: ensure receiver_account.balance += transfer_payload.amount is within uint64
class TokenHandler(BasicHandler):
    def __init__(self):
        super().__init__(FAMILY_NAME, FAMILY_VERSIONS)
        self.zero_address = self.make_address(ZERO_ADDRESS)

    def get_state_processor(self):
        return {
            TokenMethod.TRANSFER: {
                'pb_class': TransferPayload,
                'processor': self._transfer
            },
            TokenMethod.GENESIS: {
                'pb_class': GenesisPayload,
                'processor': self._genesis
            }
        }

    def _get_account_by_pub_key(self, context, pub_key):
        address = self.make_address_from_data(pub_key)
        account = self.get_data(context, Account, address)

        return (address, account)

    def _genesis(self, context, pub_key, genesis_payload):
        (signer_key, account) = self._get_account_by_pub_key(context, pub_key)
        genesis_status = self.get_data(context, GenesisStatus, self.zero_address)
        if not genesis_status:
            genesis_status = GenesisStatus()
        elif genesis_status.status:
            raise InvalidTransaction('Genesis is already initialized.')
        genesis_status.status = True
        account = Account()
        account.balance = genesis_payload.total_supply
        LOGGER.info('Generated genesis transaction. Emmitted {} tokens to address {}'
                    .format(genesis_payload.total_supply, signer_key))
        return {
            signer_key: account,
            self.zero_address: genesis_status
        }

    def _transfer(self, context, pub_key, transfer_payload):
        (signer_key, signer_account) = self._get_account_by_pub_key(context, pub_key)

        if signer_key == transfer_payload.address_to:
            raise InvalidTransaction("Account cannot sent tokens to itself.")

        receiver_account = self.get_data(context, Account, transfer_payload.address_to)

        if not receiver_account:
            receiver_account = Account()

        if signer_account.balance < transfer_payload.value:
            raise InvalidTransaction("Not enough transferable balance. Signer's current balance: {}"
                                     .format(signer_account.balance))

        receiver_account.balance += transfer_payload.value
        signer_account.balance -= transfer_payload.value

        LOGGER.info('Transferred {} tokens from {} to {}'.format(transfer_payload.value,
                                                                 receiver_account.balance,
                                                                 signer_account.balance))

        return {
            signer_key: signer_account,
            transfer_payload.address_to: receiver_account
        }
