#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''

import struct,time
import logging
import db

def on_register(client, dev, command, params, message):
    devid,iccid,imsi,origintime,ver,caplen,=struct.unpack('<16s24s16sIHH', message[0:64])
    caps = message[64:]
    record = dev.get_record()
    if not record:
        return
    record.device_card = iccid
    record.syncUpdate()
    client.publish(dev.imei, 'actr', None, '%s'%(dev.imei))
    cfg = db.get_device_config(record.device_id)
    if not cfg:
        return
    value = cfg.device_config_mode
    client.publish(dev.imei, 'mode', value, '')
    dev.sync_phonebook()
    dev.sync_family()
    dev.sync_nodisturb()
    dev.sync_alram()
    dev.sync_config()
    pass

def on_logon(client, dev, command, params, message):
    record = dev.get_record()
    if not record:
        return
    ver,data_index,origintime=struct.unpack('<HHI', message)
    logging.debug('origintime=%d'%(origintime))
    logging.debug('ver=%x'%(ver))

    msg = struct.pack('<II', origintime, time.time())
    client.publish(dev.imei, 'tim', None, bytearray(msg))
    #更新上一次的对比数据
    db.delete_cellid(record.device_id)
    pass
