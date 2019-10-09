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

import os
import sys
import json
from io import StringIO

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
PACKAGE_PARENT = '../..'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from bin.parse_commands import main 


class GenerateReadMeCommands():

    def readFile(self, fileName):

        with open(fileName, 'r') as myfile:
                fileString = myfile.read()
            
        return fileString

    def main(self):

        os.environ['AKAMAI_CLI'] = "True"
        akamaiCMD = "akamai query"
        
        print(self.readFile(os.path.join(SCRIPT_DIR, "header.md")) )


        print("## Help Text")
        args = [ "help"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())

        print("## Querying Log Delivery Service (LDS)")
        args = [ "help", "ldslist"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())

        print("## Querying Netstorage NS4")
        args = [ "help", "netstoragelist"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())
        
        print("## Querying Netstorage Users")
        args = [ "help", "netstorageuser"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())

        print("## Querying Control Center Group CPCodes")
        args = [ "help", "groupcpcodelist"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())

        print("## Generic Filter Template Utility")
        args = [ "help", "filtertemplate"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())

        print("## Querying Property Mangager Configurations")
        args = [ "help", "bulksearch"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())

        print("## Bulk Search Template Utility")
        args = [ "help", "bulksearchtemplate"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        self.printHelpTest(result.getvalue())

        print("### Bulk Search Built In Templates")
        print()
        print("Out-of-the box bulk searches done on the endpoint. They are listed when running the command:")
        args = [ "bulksearchtemplate"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        result = f"{akamaiCMD} {' '.join(args)} \n\n{result.getvalue()} "
        self.printHelpTest(result)

        print()
        print("default.json bulk search template finds all configuration cpcode values:")
        args = [ "bulksearchtemplate", "--get", "default.json"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        result = f"{akamaiCMD} {' '.join(args)} \n\n{result.getvalue()} "
        self.printHelpTest(result)

        print()
        print("origins.json template finds all configuration with their origin values:")
        args = [ "bulksearchtemplate", "--get", "origins.json"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        result = f"{akamaiCMD} {' '.join(args)} \n\n{result.getvalue()} "
        self.printHelpTest(result)

        print()
        print("gtm-origins.json template finds all configurations with gtm origins:")
        args = [ "bulksearchtemplate", "--get", "gtm-origins.json"]
        result, _ = self.redirectOutputToArray(lambda args : main(args) , args, False)
        result = f"{akamaiCMD} {' '.join(args)} \n\n{result.getvalue()} "
        self.printHelpTest(result)


    def printHelpTest(self, value):
        print()
        print("``` ")
        print(value)
        print("``` ")


    def redirectOutputToArray(self, fun, value, ignoreNewLines = True):

        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out

        saved_stderr = sys.stderr
        outerr = StringIO()
        sys.stderr = outerr
        
        _ = fun(value)

        sys.stdout = saved_stdout
        sys.stderr = saved_stderr

        return (out, outerr)
       

if __name__ == '__main__':
    prog = GenerateReadMeCommands()
    prog.main()


