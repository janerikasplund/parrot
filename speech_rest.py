#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Google Cloud Speech API sample application using the REST API for batch
processing."""

# [START import_libraries]
import argparse
import base64
import json
import os
import re

from googleapiclient import discovery

import httplib2

from oauth2client.client import GoogleCredentials
# [END import_libraries]

# Path to local discovery file
# [START discovery_doc]
API_DISCOVERY_FILE = os.path.join(
    os.path.dirname(__file__), '/home/jan/parrot/speech-discovery_google_rest_v1.json')
# [END discovery_doc]


# Application default credentials provided by env variable
# GOOGLE_APPLICATION_CREDENTIALS
def get_speech_service():
    # [START authenticating]
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    with open(API_DISCOVERY_FILE, 'r') as f:
        doc = f.read()

    return discovery.build_from_document(
        doc, credentials=credentials, http=httplib2.Http())
    # [END authenticating]


def main(speech_file):
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
    # [START construct_request]
    with open(speech_file, 'rb') as speech:
        # Base64 encode the binary audio file for inclusion in the JSON
        # request.
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().recognize(
        body={
            'initialRequest': {
                'encoding': 'FLAC',
                'sampleRate': 44100,
		'languageCode': 'en-US'
            },
            'audioRequest': {
                'content': speech_content.decode('UTF-8')
                }
            })
    # [END construct_request]
    # [START send_request]
    response = service_request.execute()
    jresponse = (json.dumps(response))
    str = jresponse
    match = re.search('("transcript": ")(.+)("})', str)
    if match:
        print match.group(2)
    else:
        print(jresponse)
    # [END send_request]



# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='Full path of audio file to be recognized')
    args = parser.parse_args()
    main(args.speech_file)
    # [END run_application]
