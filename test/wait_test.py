import sys
sys.path.append('..')
from cn.imerit.glaive.wait import *
import unittest
import mock
import gevent

class TestObj:
    def __init__(self, x):
        self.x = x
    
    def method1(self):
        print 'method1',self.x
        
obj = TestObj('abc')

def func1():
    print 'func1'
    data = waitObject('location', '1234567', 20, obj.method1)
    print data
    
def func2():
    gevent.sleep(10)
    notifyWait('location', '1234567', (0, 0, 0))
    

gevent.joinall([
    gevent.spawn(func1),
    gevent.spawn(func2),
    ])