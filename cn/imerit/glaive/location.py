#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''
import decode
import db
import geo
import cell_location
import status
import notification
import logging
import json
import wait
import time, datetime

def check_circle_fence(lat, lng, clat, clng, radius):
    distance = geo.distance(lat,lng,clat,clng)
    if distance < radius:
        return 1
    return 0
    pass

def check_rect_fence(lat, lng, lat0, lng0, lat1, lng1):
    if (lat >= lat0 and lat <= lat1 and lng >= lng0 and lng <= lng1):
        return 1
    return 0
    pass

def update_location(dev, rtime, lat, lng, alt, speed, bearing, accuracy, cellrecid):
    wait.notifyWait('location', dev.imei, (lat, lng, rtime))
    record = dev.get_record()
    db.insert_realtime_location(record.device_id, rtime, lat, lng, alt, speed, bearing, accuracy, cellrecid)
    dev.update_location(lat, lng, rtime)
    for fence in dev.get_fences():
        cache_status = db.cacheobj_get_device_fence_status(dev.imei, fence.fine_id)
        if fence.fine_type==0:
            status = check_circle_fence(lat, lng, fence.fine_lat1, fence.fine_lng1, fence.fine_lng2)
        else:
            status = check_rect_fence(lat, lng, fence.fine_lat1, fence.fine_lng1, fence.fine_lat2, fence.fine_lng2)
        # if( cache_status != status ):
        #修复导致进入围栏也提示离开
        if( cache_status != status):
            user = db.get_user(fence.fine_user)
            notification.fence(dev.imei, fence.fine_id, [user], status, rtime, dev.get_record().device_name, fence.fine_name)
            db.cacheobj_set_device_fence_status(dev.imei, fence.fine_id, status, 0)
    pass

def on_upload_location(client, dev, command, params, message):
    logging.info('on_upload_location %s'%(dev.devid()))
    data = decode.decode_ul(message)
    record = dev.get_record()
    if not record:
        return
    gps = None
    cells = None
    for i in range(0, data[1][1]):
        gps = data[2][i][0]
        rtime = gps[5]
        if not rtime:
            rtime = data[0][5]
        gps = (gps[0], gps[1], gps[2], gps[3], gps[4], rtime)
        if( gps[0] != 0 and gps[1] != 0):
            db.insert_location(record.device_id, gps[5], gps[0], gps[1], gps[2], gps[3], gps[4], 0, 0)
        
        cells_hdr = data[2][i][1]
        rtime = cells_hdr[4]
        if not rtime:
            rtime = data[0][5] + data[1][0]
        cells = data[2][i][2]
        cellsinfo = data[2][i][3]
        # 这个表用来过滤了，存入0，0会导致过滤出错
        # recid = db.insert_cell_location(record.device_id, rtime, cellsinfo)
        recid=0
        lat, lng, accuracy = cell_location.calc_location(cells)
        if( gps[0] == 0 or gps[1] == 0 ):
            db.insert_location(record.device_id, rtime, lat, lng, 0, 0, 0, accuracy, recid)
            gps = (lat, lng, 0, 0, 0, rtime)
            cells = (accuracy, recid)
        else:
            cells = (0, 0)
    #if gps and cells:
    if gps or cells:
        update_location(dev, gps[5], gps[0], gps[1], gps[2], gps[3], gps[4], cells[0], cells[1])
    status.update_status(client, dev, data[0])
    pass

def on_upload_gps(client, dev, command, params, message):
    logging.info('on_upload_gps %s'%(dev.devid()))
    data = decode.decode_ug(message)
    record = dev.get_record()
    if not record:
        return
    gps = None
    for i in range(0, data[1][1]):
        gps = data[2][i]
        rtime = gps[5]
        if not rtime:
            rtime = data[0][5] + i * data[1][0]
        gps = (gps[0], gps[1], gps[2], gps[3], gps[4], rtime)
        if( gps[0] != 0 and gps[1] != 0):
            db.insert_location(record.device_id, gps[5], gps[0], gps[1], gps[2], gps[3], gps[4], 0, 0)
    if gps:
        update_location(dev, gps[5], gps[0], gps[1], gps[2], gps[3], gps[4], 0, 0)
    status.update_status(client, dev, data[0])
    pass

def on_upload_cell(client, dev, command, params, message):
    logging.info('on_upload_cell %s'%(dev.devid()))
    data = decode.decode_uc(message)
    logging.info(json.dumps(data))
    record = dev.get_record()
    if not record:
        return
    gps = None
    for i in range(0, data[1][1]):
        cells_hdr = data[2][i][0]
        rtime = cells_hdr[4]
        if not rtime:
            rtime = data[0][5] + i * data[1][0]
        cells = data[2][i][1]
        cellsinfo = data[2][i][2]
        status.update_status(client, dev, data[0])
        if (cellsinfo[0] == '0' and cellsinfo[2] == '0'):
            logging.warn('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@cellsinfo = 0')
            return
        #这是判断基站是否和上一次的相同，如果相同的基站数超过三个就使用上一次的点
        #bug第二天之后要清空cellid表
        cellId=db.get_cellid(record.device_id)
        if cellId:
            str1 = cellId.cellid_info
            str2 = cellsinfo
            arr1 = str1.split(',')
            arr2 = str2.split(',')
            i = 0
            count = 0
            signal = 0
            try:
                while 1:
                    j = 0
                    while 1:
                        if (arr1[i * 5 + 2] == arr2[j * 5 + 2] and arr1[i * 5 + 3] == arr2[j * 5 + 3] and arr1[i * 5 + 4] ==
                            arr2[j * 5 + 4] and arr1[i * 5 + 5] == arr2[j * 5 + 5]):
                            count = count + 1
                            difference = abs((int(arr1[i * 5 + 6]) - int(arr2[j * 5 + 6])))
                            if ( difference <= 20):
                                signal =  signal + 1
                        j = j + 1
                        if j >= int(arr2[1]):
                            break
                    i = i + 1
                    if i >= int(arr1[1]):
                        break
            except Exception, e:
                logging.error('%s>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' % (e))
                pass
            logging.warn('--------------count=%s signal=%s' % (count,signal))
            # if ((int(arr1[1]) >= 3 and count >=3 and signal >= 2) or ((int(arr1[1])<=3 or int(arr2[1])<=3) and count >= 1 and signal >= 1)):
            if ((int(arr1[1]) >= 4 and count >= 3 and signal >=2) or ((int(arr1[1])<=3 or int(arr2[1])<=3) and count >= 1)):
                now = datetime.datetime.fromtimestamp(time.time())
                db.update_cell_loction_time(record.device_id, now)
                logging.warn('------------------count=%s!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! signal=%s' % (count,signal))
                return
        else:
            logging.error('-------not cell id---------')
        recid = db.insert_cell_location(record.device_id, rtime, cellsinfo)
        lat, lng, accuracy = cell_location.calc_location(cells)
        if (lat != 0 and lng != 0):
            db.insert_location(record.device_id, rtime, lat, lng, 0, 0, 0, accuracy, recid)
            gps = (lat, lng, 0, 0, 0, rtime, accuracy, recid)
    if gps:
        update_location(dev, gps[5], gps[0], gps[1], gps[2], gps[3], gps[4], gps[6], gps[7])
    pass
