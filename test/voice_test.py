import sys
sys.path.append('..')
from cn.imerit.glaive.voice import *
from cn.imerit.glaive import device
import unittest
import mock
    
class Test(unittest.TestCase):
    user = None
    bind = None
            
    def setUp(self):
        config.database.host = '192.168.1.233'
        config.database.port = 3306
        config.redis.host = '192.168.1.233'
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
        
        self.reqmock = mock.Mock(return_value=mock.Mock())
        self.respMock = mock.Mock()
        self.respMock.read.return_value = '{"errcode":0,"errmsg":"success","data":{"url":"http://www.baidu.com"}}'
        self.urlopenMock = mock.Mock(return_value=self.respMock)
        urllib2.Request = self.reqmock
        urllib2.urlopen = self.urlopenMock
        notification.new_voice = mock.Mock(return_value=1)
        
        self.devMock = mock.Mock()
        self.devMock.imei = '502151020009768'
        user1 = mock.Mock()
        user1.user_name = '123'
        user1.user_id = 123
        user2 = mock.Mock()
        user2.user_name = '456'
        user2.user_id = 456
        self.devMock.users = [user1, user2]
        self.devMock.get_users.return_value = self.devMock.users
        pass

    def tearDown(self):
        db.ZltDevice.delete(88888)
        pass
    
    def testcase001(self):
        url = save_voice_file('1234567890')
        print url
        self.assertNotEqual(url, None);
        pass
    
    def testcase002(self):
        on_voice(mock.Mock(), self.devMock, 'voc',  None, '1234567890')
        self.assertEqual(notification.new_voice.called, True)
        pass    
    
    def testcase007(self):        
        client = mock.Mock()
        dev = device.get_device_from_imei('502151020009768')
        on_voice(mock.Mock(), dev, 'voc', None, str(bytearray(4000)))
        print 'dur=',notification.new_voice.call_args
        
    def testcase008(self):        
        client = mock.Mock()
        dev = device.get_device_from_imei('502151020009768')
        on_voice(mock.Mock(), dev, 'voc', None, '1234567890')
        
if __name__ == "__main__":
    unittest.main()