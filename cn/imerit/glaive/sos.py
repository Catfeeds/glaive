#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017��1��19��

@author: Jarvis
'''

import struct,time
import notification

def on_sos(client, dev, command, params, message):
    users = dev.get_users()
    notification.sos(dev.imei, users, dev.get_record().device_name)
    pass