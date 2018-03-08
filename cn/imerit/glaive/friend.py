#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''

import struct,time
import logging
import config
import db
import geo
import decode
import cell_location
import urllib2

class MatchCache:
    def __init__(self, time, cells, gps, mode):
        self.time = time
        self.cells = cells
        self.gps = gps
	self.mode = mode

def on_friend(client, dev, command, params, message):
    logging.info("on_friend %s"%(dev.devid()))
    data = decode.decode_ul(message)
    rtime = data[0][5]
    rtime = time.time()
    cells = ['%d_%d_%d_%d'%(x[0], x[1], x[2], x[3]) for x in data[2][0][2]]
    logging.info("friend cells:%s"%(cells))
    gps = (data[2][0][0][0],data[2][0][0][1])
    mode = 1
    if not gps[0] or not gps[1]:
        mode = 0
        gps = cell_location.calc_location(data[2][0][2])
    friend_match_cache = db.cacheobj_get_friend_match_cache()
    removed = []
    matched = None
   
    logging.info("friend cache:%s"%(friend_match_cache))
    if dev.imei in friend_match_cache.keys():
        friend_match_cache[dev.imei] = MatchCache(rtime,cells,gps, mode).__dict__
    
    for imei in friend_match_cache:
        match_cache = friend_match_cache[imei]
        diff_time = abs(rtime - match_cache['time'])        
        logging.info("diff_time=%f",diff_time)
	if( time.time() - match_cache['time'] > config.friend_match.timeout ):
            removed.append(imei)
            continue
        if imei != dev.imei:
            match_mode = mode
            if mode != match_cache['mode'] and mode == 1:
                match_mode = 0
            match_cells = 0
            for c1 in cells:
                if c1 in match_cache['cells']:
                    match_cells = match_cells + 1
            diff_gps = geo.distance(gps[0], gps[1], match_cache['gps'][0], match_cache['gps'][1])
	    logging.info("friend %f %f %f"%(diff_time, match_cells, diff_gps))
            if( diff_time < 10 and (match_cells > 2 or (mode==1 and diff_gps < 20.0) or (mode==0 and diff_gps < 300.0)) ):
                matched = imei
                removed.append(imei)
                break

    for imei in removed:
        del friend_match_cache[imei]
    if matched:
        #db.make_friends(dev, matched)
        friend = db.get_device_record_by_imei(matched)
        dev.new_friend(matched, friend.device_phone, friend.device_name)
        data = db.cacheobj_get_device_host(matched)
        url = 'http://%s:%s/device/%s/newfriend/%s'%(data[2], data[3], matched, dev.imei)
	logging.info("friend url:%s"%(url))
        try:
            res = urllib2.urlopen(url, '{}')
            ret = res.read()
	    logging.info("%s"%(ret))
        except Exception as e:
            logging.info("%s"%(e))
            pass
    else:
        friend_match_cache[dev.imei] = MatchCache(rtime, cells, gps, mode).__dict__
    db.cacheobj_set_friend_match_cache(friend_match_cache) 
    pass

def on_friend_confirm(client, dev, command, params, message):
    logging.info("on_friend_confirm %s"%(params[0]))
    db.make_friends(dev, params[0])
    dev.sync_phonebook()
    pass
