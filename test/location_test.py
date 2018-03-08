import sys
sys.path.append('..')
from cn.imerit.glaive.location import *
from cn.imerit.glaive import config
from cn.imerit.glaive import device
from cn.imerit.glaive import db
import logging
import unittest
import mock

class Test(unittest.TestCase):
            
    def setUp(self):
        config.database.host = '192.168.1.233'
        config.database.port = 3306
        config.redis.host = '192.168.1.233'
        db.init_database()
        try:
            db.ZltDevice.delete(88888)
        except:
            pass
        devrec = db.ZltDevice(device_id=88888, 
                              device_imei='502151020009768', 
                              device_name='', 
                              device_card='',
                              device_debug=0, 
                              device_phone='',
                              device_owner=0,
                              device_cardsupply=0, 
                              device_status=0, 
                              device_position=0,
                              device_app=0,
                              device_type=0,
                              board_model='',
                              product_name='')
        devrec.syncUpdate()
        pass

    def tearDown(self):
        db.ZltDevice.delete(88888)
        pass
    
    def testcase001(self):
        msghex = '020000004a64363076a6bf582c010100cc010000ff000600000000002326ba10fbff00002326130eb9ff000038268710b5ff000038269110afff00002326b010adff00007c24fa11abff0000'
        msg = msghex.decode('hex')
        client = mock.Mock()
        dev = device.get_device_from_imei('502151020009767')
        on_upload_cell(client, dev, 'uc', None, msg)
        power = db.cacheobj_get_device_power(dev.imei)
        print ('power=%d'%(power))
        pass
    
    def testcase002(self):
        pass
        
if __name__ == "__main__":
    unittest.main()