# Copyright 2017 Akamai Technologies, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import os
import json

import sys
from io import StringIO
from collections import OrderedDict

from bin.query_result import QueryResult
from bin.fetch_propertymanager import PropertyManagerFetch
from bin.parse_commands import main 

from unittest.mock import patch
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from bin.credentialfactory import CredentialFactory

class MockResponse:

    def __init__(self):
        self.status_code = None
        self.reset()
        
    def reset(self):
        self.jsonObj = []

    def appendResponse(self, obj):
        self.jsonObj.insert(0,obj)

    def json(self):

        if self.json is not None and len(self.jsonObj) > 0:
            return self.jsonObj.pop()
        else :
            raise Exception("no more mock responses")

        return self.jsonObj




class PropertyManagerBulkSearch_Test(unittest.TestCase):

    def setUp(self):
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.edgerc = "{}/other/.dummy_edgerc".format(self.basedir)
        self.allsearchresponses = [
            "{}/json/papi/_v1_bulk/rules-search-requests-synch.json".format(self.basedir),
            "{}/json/papi/v1/properties/prp_3/versions/10/rules.json".format(self.basedir),
            "{}/json/papi/v1/properties/prp_1/versions/1/rules.json".format(self.basedir),
            "{}/json/papi/v1/properties/prp_15/versions/2/rules.json".format(self.basedir)
            
        ]

        self.allstagingresponses = [
            "{}/json/papi/_v1_bulk/rules-search-requests-synch.json".format(self.basedir),
            "{}/json/papi/v1/properties/prp_1/versions/1/rules.json".format(self.basedir)
            
        ]
        pass

    def testURLStructure(self):


        factory = CredentialFactory()
        context = factory.load(self.edgerc, None, "account_key_789")

        fetch = PropertyManagerFetch()
        
        url = fetch.buildBulkSearchUrl(context)
        self.assertIn("?accountSwitchKey=account_key_789", url)
        self.assertNotIn("group", url)
        self.assertNotIn("contract", url)

        url = fetch.buildBulkSearchUrl(context,contractId="contract_123")
        self.assertIn("contract_123", url)

        url = fetch.buildBulkSearchUrl(context)
        self.assertNotIn("contract_123", url)

        url = fetch.buildBulkSearchUrl(context,groupId="groupId_123")
        self.assertIn("groupId_123", url)

    @patch('requests.Session')
    def testIntegration(self, mockSessionObj):
        fetch = PropertyManagerFetch()

        accountKey="1-abcdef"
        
        contractId="ctr_C-0000"
        

        postdata = {
                        "bulkSearchQuery": {
                            "syntax": "JSONPATH",
                            "match": "$.behaviors[?(@.name == 'cpCode')].options.value.id"
                        }
                    }

        session = mockSessionObj()
        response = MockResponse()

        for mockJson in self.allsearchresponses:
            response.appendResponse(self.getJSONFromFile(mockJson))
            

        session.post.return_value = response
        session.get.return_value = response
        response.status_code = 200

        edgerc = self.edgerc
        
        (_, json) = fetch.bulksearch(edgerc=edgerc, postdata=postdata, account_key=accountKey, contractId=contractId, network="Production", debug=True)

        self.assertEquals(1, len(json))
        results = json[0]["matchLocationResults"]
        self.assertEquals(1, len(results))
        self.assertEquals(12345,results[0])

        response.reset()

        for mockJson in self.allstagingresponses:
            response.appendResponse(self.getJSONFromFile(mockJson))

        (_, json) = fetch.bulksearch(edgerc=edgerc, postdata=postdata, account_key=accountKey, contractId=contractId, network="Staging", debug=True)

        self.assertEquals(1, len(json))
        results = json[0]["matchLocationResults"]
        self.assertEquals(2, len(results))

        self.assertEquals(12345, results[0])
        self.assertEquals(678910, results[1])
        

        return json

    

    def getJSONFromFile(self, jsonPath):
            
            with open(jsonPath, 'r') as myfile:
                jsonStr = myfile.read()
            
            jsonObj = json.loads(jsonStr)
            return jsonObj

       

if __name__ == '__main__':
    unittest.main()


