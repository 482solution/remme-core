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

import argparse
from sawtooth_sdk.processor.core import TransactionProcessor
from remme.certificate.certificate_handler import CertificateHandler
from remme.token.token_handler import TokenHandler
from remme.shared.logging import setup_logging


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transaction processor.')
    parser.add_argument('endpoint')
    args = parser.parse_args()
    processor = TransactionProcessor(url=args.endpoint)
    processor.add_handler(TokenHandler())
    processor.add_handler(CertificateHandler())
    try:
        setup_logging('remme-' + str(processor.zmq_id)[2:-1])
        processor.start()
    except KeyboardInterrupt:
        pass
    finally:
        processor.stop()
