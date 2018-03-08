#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017��1��19��

@author: Jarvis
'''

import struct,time
import logging
import config
import voice
import db
import notification

def save_photo_file(data, type):
    res = voice.upload(config.id, config.voice.upload_url,
                 'file', 'photo%015d.%s'%(time.time(), type), data)
    if not res:
        logging.error('upload photo error')
        return None
    if res["errcode"] != 0:
        logging.error('upload photo error, code=',res["errcode"])
        return None
    url = res["data"]["url"]
    return url
    pass

def on_photo(client, dev, command, params, message):
    logging.info("on_photo %s"%(dev.devid()))
    type = 'jpg'
        
    if not ( isinstance(params, list) and len(params)>=2):
        logging.warn('photo params error')
        return
    sid = params[1]
    
    if len(params)>=3:
        type=params[2]
    
    url = save_photo_file(message, type)
    if not url:
        logging.warn('upload photo failed,url='+url)
        return
    if( isinstance(params, list) and len(params)==0 ):
        return
    
    user = db.get_user_by_name(params[0])
    if not user:
        user = db.get_user(dev.get_record().device_master)
        if not user:
            logging.warn('no user for %s'%(params[0]))
            return
    photoid = db.insert_photo(dev, '%s'%([user.user_id]), url)
    if not photoid:
        logging.warn('insert photo db error')
        return
    notification.photo(dev.imei, photoid, [user], url, params[1], dev.get_record().device_name)
    pass