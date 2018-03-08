#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月20日

@author: Jarvis
'''

import paho.mqtt.client as mqtt
import logging

class Client(mqtt.Client):
    def __init__(self, id):
        super(Client, self).__init__(id)
        self.serverid = id
        
    def combine_topic(self, target, command, params):
        if( not params):
            return '%s/%s/%s'%(target, self.serverid, command)
        if( isinstance(params, list) or isinstance(params, tuple)):
            return '%s/%s/%s/%s'%(target, self.serverid, command, '/'.join(params))
        return '%s/%s/%s/%s'%(target, self.serverid, command, params)
    
    def publish(self, target, command, params, message, qos=1):
        topic = self.combine_topic(target, command, params)
        logging.info("publish %s %s"%(topic, qos))
        super(Client, self).publish(topic, message, qos=qos)
        pass