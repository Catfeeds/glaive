#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年8月26日

@author: Jarvis
'''

import struct,time
import logging
import config
import db

def on_study(client, dev, command, params, message):
    rs = message.split(';')
    datas = []
    for r in rs:
        fs = r.split(',')
        if len(fs)==2:
            t = float(fs[1])
            if( abs(t - time.time()) > 300 ):
                t = time.time() 
            datas.append({'code':fs[0],'time':t})
    db.insert_study(dev, datas)
    pass
