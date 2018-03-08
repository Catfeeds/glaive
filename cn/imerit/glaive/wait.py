#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''

import gevent
from gevent.event import AsyncResult

waitObjects = {}
def notifyWait(name, imei, data):
    if not waitObjects.has_key(name):
        return
    if waitObjects[name].has_key(imei):
        waitObjects[name][imei].set(data)
        
def notifyTimeout(obj, timeout):
    gevent.sleep(timeout)
    #obj.set(None)
        
def waitObject(name, imei, timeout, f):
    global waitObjects
    if not waitObjects.has_key(name):
        waitObjects[name] = {}
    waitObjects[name][imei] = AsyncResult()
    f()
    gevent.spawn(notifyTimeout, waitObjects[name][imei], timeout)
    obj = waitObjects[name][imei].get()
    del waitObjects[name][imei]
    return obj