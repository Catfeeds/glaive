import sys
sys.path.append('..')
from cn.imerit.glaive.photo import *
from cn.imerit.glaive import device
import unittest
import mock
    
class Test(unittest.TestCase):
            
    def setUp(self):
        config.database.host = '192.168.1.233'
        config.database.port = 3306
        reload(notification)
        db.init_database()
        try:
            db.ZltDevice.delete(88888)
        except Exception,e:
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
        db.ZltPhoto.deleteMany(db.ZltPhoto.q.photo_device==88888)
        pass
    
    def testcase001(self):
        dev = device.Device('502151020009767')
        on_photo(None, dev, 'p', ['13751119410', '0', 'jpg'], '123456')
        pass    
        
if __name__ == "__main__":
    unittest.main()