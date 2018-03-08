#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''

import gevent
from gevent import monkey
import time
import logging

import config


import mqttclient
import device
import web
import db;

monkey.patch_all()


def mqtt_on_connect(client, user_data, rc):
    if( rc != 0 ):
        client.connect(config.mqtt.host, config.mqtt.port, 60)
        return
    client.subscribe('%s/#'%(config.id))
    db.cacheobj_set_server(config.id,
                           config.local_addr,
                           config.mqtt.host if config.mqtt.host!='localhost' else config.pub_addr,
                           config.mqtt.port,
                           config.web.port)
    pass

def mqtt_on_message(client, user_data, msg):
    try:
        logging.info("%s %s", msg.topic, msg.payload.encode('hex')[0:256])
        arrs = msg.topic.split('/')
        if len(arrs)<3:
            logging.error("message topic format error %s"%(msg.topic))
            return
        target = arrs[0]
        imei = arrs[1]
        command = arrs[2]
        params = None
        if( len(arrs)>3 ):
            params = arrs[3:]
        if target != config.id:
            return
        dev = device.get_device_from_imei(imei)
        if( not dev ):
            logging.warning('device %s not found'%(imei))
            return
        dev.active()
        device.process_command(command, (client, dev, command, params, msg.payload))
    except Exception as e:
        logging.error(e)
        pass
    pass

def mqtt_on_log(client, user_data, level, buf):
    logging.debug(buf)
    pass

def mqtt_loop(client):
    while True:
        client.loop()

def start():    
    mqtt_client = mqttclient.Client(config.id)
    mqtt_client.username_pw_set(config.mqtt.user, config.mqtt.password)
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    mqtt_client.on_log = mqtt_on_log
    #mqtt_client.on_publish = mqtt_on_publish
    #mqtt_client.on_subscribe = mqtt_on_subscribe
    mqtt_client.connect(config.mqtt.host, config.mqtt.port, 60)
    
    gevent.spawn(mqtt_loop, mqtt_client)
    device.mqtt_client = mqtt_client
    gevent.spawn(web.web_server_start, mqtt_client)
    gevent.spawn(web.web_server_start_localhost, mqtt_client)
    while(True):
        gevent.sleep(1)
    pass
