#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月20日

@author: Jarvis
'''

import struct
import logging

def decode_us(bytes):
    return struct.unpack('<IbbbbI', bytes)
    pass

def decode_ul(bytes):
    device_status = decode_us(bytes[0:12])
    interval,loccount = struct.unpack('<HH', bytes[12:16])
    locs = []
    for i in range(0, loccount):
        p = 16 + i * 80
        lat,lng,alt,speed,bearing,gpsrtime = struct.unpack('<fffHHI', bytes[p:(p+20)])
        p = 36 + i * 80
        mcc,mnc,ta,cellcount,cellrtime = struct.unpack('<HHHHI', bytes[p:(p+12)])
        p = p + 12
        cells = []
        cellstr = '%d,%d'%(ta, cellcount)
        for j in range(0, cellcount):
            lac,cid,strength,pad1 = struct.unpack('<HHhH', bytes[p:(p+8)])
            cellstr = '%s,%d,%d,%d,%d,%d'%(cellstr,mcc,mnc,lac,cid,strength)
            cells.append((mcc,mnc,lac,cid,strength))
            p = p + 8
        locs.append(((lat,lng,alt,speed,bearing,gpsrtime), (mcc,mnc,ta,cellcount,cellrtime), cells, cellstr))
    return (device_status, (interval,loccount), locs)
    pass

def decode_ug(bytes):
    device_status = decode_us(bytes[0:12])
    interval,loccount = struct.unpack('<HH', bytes[12:16])
    locs = []
    for i in range(0, loccount):
        p = 16 + i * 20
        lat,lng,alt,speed,bearing,gpsrtime = struct.unpack('<fffHHI', bytes[p:(p+20)])
        locs.append((lat,lng,alt,speed,bearing,gpsrtime))
    return (device_status, (interval,loccount), locs)
    pass

def decode_uc(bytes):
    device_status = decode_us(bytes[0:12])
    interval,loccount = struct.unpack('<HH', bytes[12:16])
    locs = []
    for i in range(0, loccount):
        p = 16 + i * 60
        mcc,mnc,ta,cellcount,cellrtime = struct.unpack('<HHHHI', bytes[p:(p+12)])
        p = p + 12
        cells = []
        cellstr = '%d,%d'%(ta, cellcount)
        for j in range(0, cellcount):
            lac,cid,strength,pad1 = struct.unpack('<HHhH', bytes[p:(p+8)])
            cellstr = '%s,%d,%d,%d,%d,%d'%(cellstr,mcc,mnc,lac,cid,strength)
            cells.append((mcc,mnc,lac,cid,strength))
            p = p + 8
        locs.append(((mcc,mnc,ta,cellcount,cellrtime), cells, cellstr))
    return (device_status, (interval,loccount), locs)
    pass
