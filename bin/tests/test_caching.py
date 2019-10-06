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

from bin.decorator import count_calls
from bin.decorator import cache
from bin.decorator import CacheManager
from bin.decorator import CallCount

class CachingTest(unittest.TestCase):

    def test_upper(self):
        
        @count_calls
        @cache
        def fibonacci(num):
            if num < 2:
                return num
            return fibonacci(num - 1) + fibonacci(num - 2)
        
        f1 = fibonacci(7)
        
        self.assertEqual(13, CallCount().get("fibonacci"))

        CallCount().clear("fibonacci")
        self.assertEqual(0, CallCount().get("fibonacci"))

        f2 = fibonacci(7)
        self.assertEqual(f1, f2)

        self.assertEqual(1, CallCount().get("fibonacci"))
        

    

if __name__ == '__main__':
    unittest.main()