import sys
sys.path.append("..")
from cn.imerit.glaive.mqttclient import *
import unittest
import mock
    
class Test(unittest.TestCase):            
    def setUp(self):
        self.client = Client('000001')
        pass

    def tearDown(self):
        pass
    
    def testcase001(self):
        self.assertEqual(self.client.serverid, '000001')
        pass
    
    def testcase002(self):
        topic = self.client.combine_topic('1', '2', None)
        self.assertEqual(topic, '1/%s/2'%(self.client.serverid))
        pass
        
    def testcase003(self):
        topic = self.client.combine_topic('1', '2', '3456')
        self.assertEqual(topic, '1/%s/2/3456'%(self.client.serverid))        
        pass
    
    def testcase004(self):
        topic = self.client.combine_topic('1', '2', ('3'))
        self.assertEqual(topic, '1/%s/2/3'%(self.client.serverid))        
        pass
    
    def testcase005(self):
        topic = self.client.combine_topic('1', '2', ('3','4'))
        self.assertEqual(topic, '1/%s/2/3/4'%(self.client.serverid))        
        pass
    
    def testcase006(self):
        topic = self.client.combine_topic('1', '2', ('3',''))
        self.assertEqual(topic, '1/%s/2/3/'%(self.client.serverid))        
        pass
    
    def testcase007(self):
        topic = self.client.combine_topic('1', '2', ('3', '', '4'))
        self.assertEqual(topic, '1/%s/2/3//4'%(self.client.serverid))        
        pass
    
    def testcase008(self):
        mock_publish = mock.Mock(return_value=None)
        mqtt.Client.publish = mock_publish 
        self.client.publish('000001', 'echo', None, 'abc')
        self.assertEqual(mock_publish.called, True)
        pass
    
    def testcase009(self):
        mock_publish = mock.Mock(return_value=None)
        mqtt.Client.publish = mock_publish 
        self.client.publish('000001', 'echo', ('123'), 'abc')
        self.assertEqual(mock_publish.called, True)
        self.assertEqual(mock_publish.call_args[0][0], '000001/000001/echo/123')
        pass
        
if __name__ == "__main__":
    #unittest.main()
    pass