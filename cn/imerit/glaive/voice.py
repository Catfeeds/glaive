#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月20日

@author: Jarvis
'''

import time, urllib2, json,logging
import config
import db
import notification

def upload(serverid, http_url, name, filename, content, mime='image/png'):
    logging.info("voice.upload");
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="serverid"\r\n')
    data.append(serverid)
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (name, filename))
    data.append('Content-Type: %s\r\n' % (mime))
    data.append(content)
    data.append('--%s--\r\n' % boundary)

    http_body='\r\n'.join(data)
    qrcont = ''
    try:
        #buld http request
        req=urllib2.Request(http_url, data=http_body)
        #header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        req.add_header('User-Agent','Mozilla/5.0')
        #post data to server
        resp = urllib2.urlopen(req, timeout=5)
        #get response
        qrcont=resp.read()
        return json.loads(qrcont)
    except Exception as e:
        logging.error(e)
        logging.error(str(qrcont))
        #logging.error(qrcont.encode('hex'))
    return None

def save_voice_file(data):
    res = upload(config.id, config.voice.upload_url,
                 'file', 'voc%015d.amr'%(time.time()), data)
    if not res:
        logging.error('upload voice error')
        return None
    if res["errcode"] != 0:
        logging.error('upload voice error, code=',res["errcode"])
        return None
    url = res["data"]["url"]
    return url
    pass

def on_voice(client, dev, command, params, message):
    logging.info("on_voice %s"%(dev.devid()))
    url = save_voice_file(message)
    if not url:
        logging.error('upload voice failed')
        return
    dur = (len(message)+800)/1600
    users = dev.get_users()
    if len(users)==0:
        logging.info('not found users for device %s'%(dev.imei))
        return
    if( params and isinstance(params, list) and len(params)>0 ):
        targets = params[0].split(',')
        app_users = []
        family_users = [user.user_name for user in users]
        others = []
        for target in targets:
            x = [user for user in users if user.user_name == target]
            if x:
                app_users.append(x[0])
            else:
                x = db.get_user_by_name(target)
                if x:
                    app_users.append(x)
                else:
                    others.append(target)
        if app_users:
            vocid = db.insert_voice('d%s'%(dev.imei), 'u%s'%([user.user_name for user in app_users]), url, dur)
            if vocid:
                notification.new_voice(dev.imei, vocid, app_users, url, dur, dev.get_record().device_name)
        for target in others:
            odev = db.get_device_record_by_phone(target)
            if odev:
                vocid = db.insert_voice('d%s'%(dev.imei), 'd%s'%(odev.device_imei), url, dur)
                client.publish(odev.device_imei, 'voc', ('%s'%(dev.get_record().device_phone),'%s'%(vocid)), bytearray(message))
    else:
        vocid = db.insert_voice('d%s'%(dev.imei), 'u%s'%([user.user_name for user in users]), url, dur)
        notification.new_voice(dev.imei, vocid, users, url, dur, dev.get_record().device_name)
    pass

def on_voice_fail(client, dev, command, params, message):
    logging.info("on_voice_fail %s"%(dev.devid()))
    if params and isinstance(params, list):
        db.update_voice_read(params[0], -1)
    pass

def on_voice_play(client, dev, command, params, message):
    logging.info("on_voice_play %s"%(dev.devid()))
    if params and isinstance(params, list):
        db.update_voice_read(params[0], 1)
    voices = db.get_unread_voice('d%s'%(dev.imei))
    for voice in voices:
        fromuser = voice.voice_from[1:]
        dev.send_voice(fromuser, voice.voice_id)
        break;
    pass
