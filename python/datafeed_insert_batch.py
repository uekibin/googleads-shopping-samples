#!/usr/bin/python
#
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
"""Adds several datafeeds to the specified account, in a single batch."""

from __future__ import print_function
import json
import sys

import datafeed_sample
import shopping_common

# Number of datafeeds to insert.
BATCH_SIZE = 5


def main(argv):
  # Authenticate and construct service.
  service, config, _ = shopping_common.init(argv, __doc__)
  merchant_id = config['merchantId']

  batch = {
      'entries': [{
          'batchId': i,
          'merchantId': merchant_id,
          'method': 'insert',
          'datafeed': datafeed_sample.create_datafeed_sample(
              config, 'feed%s' % shopping_common.get_unique_id()),
      } for i in range(BATCH_SIZE)],
  }

  request = service.datafeeds().custombatch(body=batch)
  result = request.execute()

  if result['kind'] == 'content#datafeedsCustomBatchResponse':
    entries = result['entries']
    for entry in entries:
      if not shopping_common.json_absent_or_false(entry, 'datafeed'):
        print('Datafeed %s with name "%s" created.' %
              (entry['datafeed']['id'], entry['datafeed']['name']))
      elif not shopping_common.json_absent_or_false(entry, 'errors'):
        print('Errors for batch entry %d:' % entry['batchId'])
        print(json.dumps(entry['errors'], sort_keys=True, indent=2,
                         separators=(',', ': ')))
  else:
    print('There was an error. Response: %s' % result)


if __name__ == '__main__':
  main(sys.argv)
