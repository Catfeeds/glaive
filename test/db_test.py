import sys
sys.path.append("..")
from cn.imerit.glaive.db import *
from cn.imerit.glaive import decode
import unittest
import mock
    
class Test(unittest.TestCase):  
    
    def setUp(self):
        config.database.host = '192.168.1.233'
        config.database.port = 3306
        config.redis.host = '192.168.1.233'
        #config.mecacheobj.host = '192.168.1.233'
        init_database()
        devrec = ZltDevice(device_id=88888, 
                           device_imei='888888888888888', 
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
        ZltDevice.delete(88888)
        pass
    
    def testcase001(self):
        dev = get_device_record_by_imei('888888888888888')
        self.assertEqual(dev.device_id, 88888)
        pass
    
    def testcase002(self):
        cfg = get_device_config(88888)
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.device_config_id, 88888)
        pass
    
    def testcase003(self):
        fences = get_fences_by_device(88888)
        self.assertIsNotNone(fences)
        self.assertEquals(len(fences), 0)
    
    def testcase004(self):
        binds = get_users_by_device(88888)
        self.assertIsNotNone(binds)
        for bind in binds:
            bind.user_lang = 'cn'
            break
        for bind in binds:
            print bind.user_name,bind.user_lang
        
    def testcase005(self):
        id = insert_location(88888, time.time(), 22.5, 114.0, 0, 0, 0, 0, 0)
        locs = ZltLocation.select(ZltLocation.q.location_id==id)
        self.assertIsNotNone(locs)
        loc = locs.getOne(None)
        self.assertIsNotNone(loc)
        self.assertEquals(loc.location_lati, 22.5)
        self.assertEquals(loc.location_longi, 114.0)
        ZltLocation.delete(id)
        
    def testcase006(self):
        id = insert_cell_location(88888, time.time(), "1,2,3,4,5,6")
        cells = ZltCellid.select(ZltCellid.q.cellid_id==id)
        self.assertIsNotNone(cells)
        cell = cells.getOne(None)
        self.assertIsNotNone(cell)
        ZltCellid.delete(id)
        
    def testcase007(self):        
        msghex = '020000004a64363076a6bf582c010100cc010000ff000600000000002326ba10fbff00002326130eb9ff000038268710b5ff000038269110afff00002326b010adff00007c24fa11abff0000'
        msg = msghex.decode('hex')
        data = decode.decode_uc(msg)
        locs = get_cell_locations(data[2][0][1])
        print locs
        
    def testcase008(self):
        cacheobj_set_device_power('502151020009767', 99, 0)
        power = cacheobj_get_device_power('502151020009767')
        self.assertEqual(power, 99)
        
    def testcase009(self):
        cacheobj_set_device_online('502151020009767', 1, 0)
        power = cacheobj_get_device_online('502151020009767')
        self.assertEqual(power, 1)
        cacheobj_set_device_online('502151020009767', 0, 0)
        power = cacheobj_get_device_online('502151020009767')
        self.assertEqual(power, 0)
        
    def testcase010(self):
        cacheobj_set_device_power('502151020009767', 99, 1)
        time.sleep(2)
        power = cacheobj_get_device_power('502151020009767')
        self.assertEqual(power, 0)
        
if __name__ == "__main__":
    unittest.main()