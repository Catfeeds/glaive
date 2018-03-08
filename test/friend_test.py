import sys
sys.path.append("..")
from cn.imerit.glaive.friend import *
from cn.imerit.glaive import db
from cn.imerit.glaive import device
from sqlobject import *
import unittest
import mock
    
class Test(unittest.TestCase):  
    
    def setUp(self):
        config.database.host = '192.168.1.233'
        config.database.port = 3306
        config.redis.host = '192.168.1.233'
        db.init_database()
        self.devrec1 = db.ZltDevice(device_id=88888, 
                           device_imei='502151020009769', 
                           device_name='ABC', 
                           device_card='111',
                           device_debug=0, 
                           device_phone='111',
                           device_owner=0,
                           device_cardsupply=0, 
                           device_status=0, 
                           device_position=0,
                           device_app=0,
                           device_type=0,
                           board_model='',
                           product_name='')
        self.devrec1.syncUpdate()
        self.devrec2 = db.ZltDevice(device_id=88889, 
                           device_imei='502151020009768', 
                           device_name='DEF', 
                           device_card='222',
                           device_debug=0, 
                           device_phone='222',
                           device_owner=0,
                           device_cardsupply=0, 
                           device_status=0, 
                           device_position=0,
                           device_app=0,
                           device_type=0,
                           board_model='',
                           product_name='')
        self.devrec2.syncUpdate()
        db.cacheobj_set_friend_match_cache({})
        pass

    def tearDown(self):
        db.ZltDevice.delete(88888)
        db.ZltDevice.delete(88889)
        db.ZltDevicepb.deleteMany(db.ZltDevicepb.q.devicepb_device==88888)
        db.ZltDevicepb.deleteMany(db.ZltDevicepb.q.devicepb_device==88889)
        pass
    
    def testcase001(self):
        hex = '0200000061600000263a32592c010100'
        hex = hex + '0000000000000000000000000000000000000000'
        hex = hex + 'cc010000ff000600153a32598884fa02cfff00008884134bbfff000088847653bdff00008884fd02bbff000088847553b7ff000088848d0ab1ff0000'
    
        dev = device.Device('502151020009769')
        dev1 = device.Device('502151020009768')
        on_friend(None, dev, 'fr', None, hex.decode('hex'))
        on_friend(None, dev1, 'fr', None, hex.decode('hex'))
        pb1 = db.ZltDevicepb.select(db.ZltDevicepb.q.devicepb_device==88888 and db.ZltDevicepb.q.devicepb_phone==self.devrec2.device_phone)
        pb2 = db.ZltDevicepb.select(db.ZltDevicepb.q.devicepb_device==88889 and db.ZltDevicepb.q.devicepb_phone==self.devrec1.device_phone)
        self.assertNotEqual(pb1.getOne(), None, '')
        self.assertNotEqual(pb2.getOne(), None, '')
        pass
        
if __name__ == "__main__":
    unittest.main()