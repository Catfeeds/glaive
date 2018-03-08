import sys
sys.path.append('..')
from cn.imerit.glaive import config
config.database.host = '127.0.0.1'
from cn.imerit.glaive.notification import *
import unittest
#import mock

class Test(unittest.TestCase):
            
    def setUp(self):
        config.lang.dir = '../lang'
        reload(sys)
        sys.setdefaultencoding('utf-8')
        pass

    def tearDown(self):
        pass
    
    def testcase001(self):
        print 'value=',get_string('cn', 'Fence Alarm')
        #push_event([3560, 3456], 'abc', {"dev":123})
        pass
    
    def testcase002(self):
        title = get_string('cn', 'Low Power')
        extras={'type':TypeLowPower,'imei':'502151020009767','power':20, 'time':time.time(), 'device_name':'abc'}
        push_event([3885, 3899], title, TypeLowPower, extras)
        pass
        
if __name__ == "__main__":
    unittest.main()