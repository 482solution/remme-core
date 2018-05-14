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

# FIXME: Need something to do with sdk and remove from here
FROM hyperledger/sawtooth-rest-api:1.0.1
RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y python3 python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev

# FROM python:3.6
WORKDIR /root
COPY ./requirements.txt .
RUN pip3 install -r ./requirements.txt
RUN mkdir -p remme/remme
COPY ./remme ./remme/remme
COPY ./setup.py ./remme
RUN pip3 install ./remme
COPY ./bash/.bashrc /root/.bashrc