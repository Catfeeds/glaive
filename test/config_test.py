# import sys
# sys.path.append('..')
# from cn.imerit.glaive.config import *
# import unittest
# import mock
# 
# class Test(unittest.TestCase):
#             
#     def setUp(self):
#         pass
# 
#     def tearDown(self):
#         pass
#     
#     def testcase001(self):
#         Config.Inst('../server.conf')
#         pass
#     
#     def testcase002(self):
#         pass
#         
# if __name__ == "__main__":
#     unittest.main()

class mqttConfig:
    host = 'localhost'
    port = 1883
    

mqtt = mqttConfig()

mqtt.host = 'localhost'
print mqtt.host
mqtt.host = '192.168.1.233'
print mqtt.host