import sys
sys.path.append('..')
from cn.imerit.glaive.decode import *
from cn.imerit.glaive import db
import unittest
import mock

class Test(unittest.TestCase):
            
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def testcase001(self):
        msghex = '020000004a64363076a6bf582c010100cc010000ff000600000000002326ba10fbff00002326130eb9ff000038268710b5ff000038269110afff00002326b010adff00007c24fa11abff0000'
        msg = msghex.decode('hex')
        data = decode_uc(msg)
        print data
        pass
    
    def testcase002(self):
        pass
        
if __name__ == "__main__":
    unittest.main()