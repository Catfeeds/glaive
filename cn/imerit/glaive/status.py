#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''

import decode
import notification
import db
import wait
import logging

def update_status(client, dev, status):
    try:
        flag32, power, rssi, satellite, flag8, rtime = status
        db.cacheobj_set_device_rssi(dev.imei, rssi, dev.get_udinterval())
        db.cacheobj_set_device_satellite(dev.imei, satellite, dev.get_udinterval())
        db.cacheobj_set_device_flags(dev.imei, (flag32, flag8), dev.get_udinterval())
        power_old = db.cacheobj_get_device_power(dev.imei)
        logging.info('pppppppppppppppppppppp %s %s' % (power_old, power))
        if (power < 10) and (power_old > power):
            logging.info('-----------------------------------------------tui song dian liang!')
            users = db.get_users_by_device(dev.devid())
            notification.low_power(dev.imei, users, power, dev.get_record().device_name)
            logging.info('name============= %s' % (dev.get_record().device_name))
        db.cacheobj_set_device_power(dev.imei, power, dev.get_udinterval()+15)
    except Exception, e:
        logging.error('update status error %s' % e)
        pass

def on_upload_status(client, dev, command, params, message):
    status = decode.decode_us(message)
    update_status(client, dev, status)
    #wait.notifyWait('location', dev.imei, (0, 0, status[5]))
    pass