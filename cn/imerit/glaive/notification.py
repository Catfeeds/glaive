#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''

import db
import jpush
import config
import json,time
import os,sys,re
import logging

TypeLowPower = 2
TypeFence = 1
TypeNewVoice = 5
TypeSOS = 6
TypePhoto = 7
TypeSMS = 8

languages = {}

def get_string(lang, key, default=None):
    global languages
    try:
        if not languages.has_key(lang):
            languages[lang] = None
        map = languages[lang]
        if not map:
            f = open('%s/%s.lang'%(config.lang.dir, lang))
            if f:
                try:
                    js = '{%s}'%(','.join([re.sub(r'//.*','',line) for line in f.readlines() if len(line)>1 and len(re.sub(r'//.*','',line))>1]))
                    map = json.loads(js)
                finally:
                    f.close()
            languages[lang] = map
        if map:
            if map.has_key(key):
                return map[key]
    except Exception as e:
        logging.warn(e)
    if default:
        return default
    return key

#_jpush = jpush.JPush(config.jpush.appkey, config.jpush.secret);
#_jpush.set_logging("DEBUG");
#logging.info('initialize jpush %s %s'%(config.jpush.appkey, config.jpush.secret))

def push_event_for_push(push, recipients, title, type, extras):
    push.audience = jpush.audience({'alias':['u%014d'%(recipient) for recipient in recipients]})
    logging.info('title=%s'%(title))
    ios_msg = jpush.ios(alert=title.encode('utf-8'),badge='+1',extras=extras)
    android_msg = jpush.android(alert=title.encode('utf-8'),extras=extras)
    push.notification = jpush.notification(alert=title.encode('utf-8'), android=android_msg, ios=ios_msg)
    push.platform = jpush.all_
    push.options = {'apns_production':config.jpush.production}
    msg_id = ''
    try:
        rsp = push.send()
        msg_id = rsp.payload["msg_id"]
        logging.info(rsp)
    except Exception as e:
        logging.warning(e)
        pass
    for recipient in recipients:
        db.insert_event(recipient, msg_id, type, json.dumps(extras), 0)
apppush = {}

def push_event(recipients, title, type, extras):
    global apppush
    logging.info("push_event %s"%(type))
    rg = {}
    for recipient in recipients:
        appid = db.get_user_logged_app(recipient)
        if not rg.has_key(appid):
            rg[appid] = []
        rg[appid].append(recipient)
        if not apppush.has_key(appid):
            cfg = db.get_app_jpush_config(appid)
            apppush[appid] = jpush.JPush(cfg[0], cfg[1])
    for app in apppush:
        if (not rg.has_key(app)) or (not rg[app]):
            continue
        push = apppush[app].create_push()
        push_event_for_push(push, rg[app], title, type, extras)

def fence(imei, fenceid, users, status, time, device_name, fence_name):
    if len(users)<=0:
        return
    title = get_string(users[0].user_lang, 'Fence Alarm')
    extras={'type':TypeFence,'imei':imei,'fine':fenceid,'status':status,'time':time, 'device_name':device_name, 'fence_name':fence_name}
    push_event([user.user_id for user in users], title, TypeFence, extras)
    pass

def new_voice(imei, voiceid, users, url, dur, device_name):
    if len(users)<=0:
        logging.info('no user to notification')
        return
    title = get_string(users[0].user_lang, 'New Voice')
    extras={'type':TypeNewVoice,'imei':imei,'voice':voiceid, 'time':time.time(), 'duration':dur, 'url':url, 'device_name':device_name}
    push_event([user.user_id for user in users], title, TypeNewVoice, extras)
    pass

def photo(imei, photoid, users, url, sid, device_name):
    if len(users)<=0:
        logging.info('no user to notification')
        return
    title = get_string(users[0].user_lang, 'Photo')
    extras={'type':TypePhoto, 'imei':imei, 'photo':photoid, 'time':time.time(), 'url':url, 'sid':sid, 'device_name':device_name}
    push_event([user.user_id for user in users], title, TypePhoto, extras)

def low_power(imei, users, power, device_name):
    if len(users)<=0:
        return
    title = get_string(users[0].user_lang, 'Low Power')
    extras={'type':TypeLowPower,'imei':imei,'power':power, 'time':time.time(), 'device_name':device_name}
    push_event([user.user_id for user in users], title, TypeLowPower, extras)
    pass

def sos(imei, users, address, device_name):
    if len(users)<=0:
        return
    title = get_string(users[0].user_lang, 'SOS')
    extras={'type':TypeSOS, 'imei':imei, 'address':address, 'time':time.time(), 'device_name':device_name}
    push_event([user.user_id for user in users], title, TypeSOS, extras)
    pass

def sms(imei, users, text, device_name):
    if len(users)<=0:
        return
    title = get_string(users[0].user_lang, 'SMS')
    extras={'type':TypeSMS, 'imei':imei, 'text':text, 'device_name':device_name}
    push_event([user.user_id for user in users], title, TypeSMS, extras)
    pass