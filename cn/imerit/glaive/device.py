#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''

import gevent, time
from gevent import monkey
import binascii,urllib2,logging
import struct
import config
import register
import location
import status
import voice
import friend
import sos
import db
import photo
import wait
import study

monkey.patch_all()

device_map = {}
device_count = 0

mqtt_client = None

def get_device_count():
    return device_count

class Device(object):
    def __init__(self, imei):
        self.imei = imei
        self.record = None
        self.config = None
        self.fences = None
        self.users = None
        self.active_time = time.time()
        self.dismiss_time = time.time()
        self._sid = 0
        
    def sid(self):
        self._sid = self._sid + 1
        return self._sid
    
    def register(self):
        pass
    
    def get_udinterval(self):
        udinterval = config.default.device_udinterval
        cfg = self.get_config()
        if cfg:
            udinterval = cfg.device_config_udinterval
        return udinterval
    
    def active(self):
        self.active_time = time.time()
        udinterval = self.get_udinterval()
        db.cacheobj_set_device_online(self.imei, 1, udinterval + 60)
        db.cacheobj_set_device_host(self.imei, 
                                  config.mqtt.host if config.mqtt.host != 'localhost' else config.pub_addr, 
                                  config.mqtt.port, 
                                  config.web.host, 
                                  config.web.port,                                   
                                  config.id )
        pass
    
    def deactive(self):
        db.cacheobj_set_device_online(self.imei, 0, 0)
    
    def update_location(self, lat, lng, rtime):
        #udinterval = self.get_udinterval()
        db.cacheobj_set_device_location(self.imei, lat, lng, rtime, 0)
        pass
    
    def update_power(self, power):
        udinterval = self.get_udinterval()
        db.cacheobj_set_device_power(self.imei, power, udinterval + 60)
        pass
    
    def devid(self):
        record = self.get_record()
        if not record:
            return 0
        return record.device_id
    
    def get_record(self):
        if not self.record:
            self.record = db.get_device_record_by_imei(self.imei)
        return self.record
        pass
    
    def get_fences(self):
        self.fences = db.get_fences_by_device(self.get_record().device_id)
        return self.fences
        pass
    
    def get_users(self):
        self.users = db.get_users_by_device(self.get_record().device_id)
        return self.users
        pass
    
    def get_config(self):
        self.config = db.get_device_config(self.get_record().device_id)
        return self.config
    
    def sync_config(self):
        cfg = db.get_device_config(self.get_record().device_id)
        data = struct.pack('<HHIHH', 0, int(cfg.device_config_heartbeat), int(cfg.device_config_config), int(cfg.device_config_udinterval), int(cfg.device_config_interval))
        mqtt_client.publish(self.imei, 'cfg', None, bytearray(data))
    
    def sync_family(self):
        binds = db.get_bind_users_by_device(self.devid())
        items = []
        for item in binds:
            items.append(binascii.b2a_hex(item.bind_nick.decode('utf-8').encode('utf-16le')))
            items.append(item.user.user_name)
        mqtt_client.publish(self.imei, 'fm', None, ','.join(items))
        pass
    
    def sync_phonebook(self):
        phonebook = db.get_phonebook_by_device(self.devid())
        items = []
        for item in phonebook:
            items.append(binascii.b2a_hex(item.devicepb_name.decode('utf-8').encode('utf-16le')))
            items.append(item.devicepb_phone)
        mqtt_client.publish(self.imei, 'pb', None, ','.join(items))
        pass
    
    def sync_nodisturb(self):        
        nds = db.get_nodisturb_by_device(self.devid())
        items = []
        for nd in nds:
            items.append('%d'%(nd.devicend_begin))
            items.append('%d'%(nd.devicend_end))
            items.append(nd.devicend_repeat)
        mqtt_client.publish(self.imei, 'nd', None, ','.join(items))
        pass
    
    def sync_alarm(self):
        alarms = db.get_alarms(self.devid())
        items = []
        for alarm in alarms:
            items.append('%d'%(alarm.clock_begin))
            items.append(alarm.clock_repeat)
            items.append(binascii.b2a_hex(alarm.about.decode('utf-8').encode('utf-16le')))
        mqtt_client.publish(self.imei, 'al', None, ','.join(items))
        pass
    
    def send_voice(self, fromuser, voiceid):
        voice = db.get_voice(int(voiceid))
        file = urllib2.urlopen(voice.voice_url)
        db.update_voice_read(int(voiceid), 0)
        mqtt_client.publish(self.imei, 'voc', (fromuser,voiceid), bytearray(file.read()))
        pass
    
    def monitor(self, fromuser):
        mqtt_client.publish(self.imei, 'mon', (fromuser), fromuser, 0)
    
    def shutdown(self):
        mqtt_client.publish(self.imei, 'shut', None, "", 0)
        
    def reset(self):
        mqtt_client.publish(self.imei, 'rst', None, "", 0)
    
    def find(self):
        mqtt_client.publish(self.imei, 'find', None, "")
        
    def factory(self):
        mqtt_client.publish(self.imei, 'fac', None, "", 0)
        
    def echo(self):
        mqtt_client.publish(self.imei, 'echo', None, "")
        
    def loc(self):
        mqtt_client.publish(self.imei, 'loc', None, "")
        
    def takephoto(self, fromuser, sid):
        mqtt_client.publish(self.imei, 'tp', (fromuser, sid), "")
        
    def new_friend(self, friend_imei, friend_phone, friend_name):
        pb = db.find_phonebook(self.devid(), friend_phone)
        logging.info("new friend:%s"%(pb))
        if not pb:
            mqtt_client.publish(self.imei, 'nfr', friend_imei, "%s,%s"%(friend_phone,binascii.b2a_hex(friend_name.decode('utf-8').encode('utf-16le'))))
    def mode(self,value):
        mqtt_client.publish(self.imei, 'mode', value, "")

    def tim(self):
        msg = struct.pack('<II', time.time(), time.time())
        mqtt_client.publish(self.imei, 'tim', None, bytearray(msg))
        
def on_echo(client, dev, command, params, message):
    #client.publish(dev.imei, 'echo', params, message)
    wait.notifyWait('echo', dev.imei, 1)
    pass

def dismiss_device(dev):
    dev.deactive()
    time.sleep(300)
    if( dev.active_time > dev.dismiss_time ):
        return
    global device_map
    global device_count
    if( device_map.has_key(dev.imei)):
        device_count = device_count - 1
        del device_map[dev.imei]

def on_dismiss(client, dev, command, params, message):
    dev.dismiss_time = time.time()
    gevent.spawn(dismiss_device, dev)
    pass

def default_process(client, dev, command, params, message):
    pass
        
def get_device_from_imei(imei):
    global device_map
    global device_count
    if( device_map.has_key(imei)):
        return device_map[imei]
    dev = Device(imei)
    record = dev.get_record()
    if( not record):
        logging.debug('record for %s not found'%(imei))
        return None
    device_map[imei] = dev
    device_count = device_count + 1
    return dev
    pass

command_process_map = {
    'reg':register.on_register,
    'log':register.on_logon,
    'ul':location.on_upload_location,
    'ug':location.on_upload_gps,
    'uc':location.on_upload_cell,
    'us':status.on_upload_status,
    'echo':on_echo,
    'voc':voice.on_voice,
    'vocf':voice.on_voice_fail,
    'vocp':voice.on_voice_play,
    'dis':on_dismiss,
    'fr':friend.on_friend,
    'p':photo.on_photo,
    'sos':sos.on_sos,
    'study':study.on_study,
    'frc':friend.on_friend_confirm,
    }

def process_command(command, params):
    if (command_process_map.has_key(command)):
        gevent.spawn(command_process_map[command], params[0], params[1], params[2], params[3], params[4])
        return
    default_process(params[0], params[1], params[2], params[3], params[4])
    pass
