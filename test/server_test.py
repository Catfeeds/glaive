import sys
sys.path.append('..')
from cn.imerit.glaive.server import *
import unittest
import mock

class Test(unittest.TestCase):
            
    def setUp(self):
        self.msg_mock = mock.Mock()
        self.dev_mock = mock.Mock()
        self.get_device_from_imei_mock = mock.Mock(return_value=self.dev_mock)
        self.dev_mock.active.return_value = None
        self.process_command_mock = mock.Mock(return_value=None)
        device.get_device_from_imei = self.get_device_from_imei_mock
        device.process_command = self.process_command_mock
        pass

    def tearDown(self):
        pass
    
    def testcase001(self):
        self.msg_mock.topic = 'xyz'
        mqtt_on_message("", "", self.msg_mock)
        pass
    
    def testcase002(self):
        self.msg_mock.topic = 'xyz/abc'
        mqtt_on_message("", "", self.msg_mock)
        pass
        
    def testcase003(self):
        self.msg_mock.topic = '123456/78900000/'
        mqtt_on_message("", "", self.msg_mock)
        pass
    
    def testcase004(self):
        self.msg_mock.topic = '%s/78900000/cmd/123'%(config.id)
        self.msg_mock.payload = "1234567890"
        mqtt_on_message("", "", self.msg_mock)
        self.get_device_from_imei_mock.assert_called_with('78900000')
        self.process_command_mock.assert_called_with('cmd', ("", self.dev_mock, "cmd", ["123"], "1234567890"))
        
    def testcase005(self):
        self.msg_mock.topic = '%s/78900000/cmd'%(config.id)
        self.msg_mock.payload = "1234567890"
        mqtt_on_message("", "", self.msg_mock)
        self.get_device_from_imei_mock.assert_called_with('78900000')
        self.process_command_mock.assert_called_with('cmd', ("", self.dev_mock, "cmd", None, "1234567890"))
        
    def testcase006(self):
        self.msg_mock.topic = '%s/78900000/cmd/123,456'%(config.id)
        self.msg_mock.payload = "1234567890"
        mqtt_on_message("", "", self.msg_mock)
        self.get_device_from_imei_mock.assert_called_with('78900000')
        self.process_command_mock.assert_called_with('cmd', ("", self.dev_mock, "cmd", ["123,456"], "1234567890"))
        
    def testcase007(self):
        self.msg_mock.topic = '%s/78900000/cmd/123,456/789'%(config.id)
        self.msg_mock.payload = "1234567890"
        mqtt_on_message("", "", self.msg_mock)
        self.get_device_from_imei_mock.assert_called_with('78900000')
        self.process_command_mock.assert_called_with('cmd', ("", self.dev_mock, "cmd", ["123,456", "789"], "1234567890"))
        
    def testcase008(self):
        self.msg_mock.topic = '%s/78900000/cmd/123,456/789'%(config.id)
        self.msg_mock.payload = "1234567890"
        self.get_device_from_imei_mock.return_value = None
        mqtt_on_message("", "", self.msg_mock)
        self.dev_mock.active.assert_not_called()
        self.process_command_mock.assert_not_called()
        
if __name__ == "__main__":
    unittest.main()