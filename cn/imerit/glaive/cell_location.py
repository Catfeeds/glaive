#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月20日

@author: Jarvis
'''

import geo
import db
import math
import urllib2,json
import logging
import requests
from math import*

# def query_cell_locations(cells):
#     locs = []
#     for cell in cells:
#         try:
#             http_url = 'https://app.imerit.cn/zlt/api/cell.php?mcc=%s&mnc=%s&lac=%s&cid=%s'%cell[0:4]
#             req=urllib2.Request(http_url)
#             #post data to server
#             resp = urllib2.urlopen(req, timeout=5)
#             #get response
#             qrcont=resp.read()
#             result = json.loads(qrcont)
#             if not result:
#                 logging.warning('cell location not found for %s %s %s %s'%cell)
#             locs.append((result['data'][0], result['data'][1], result['data'][2], cell[4]))
#         except Exception,e:
#             print e
#             pass
#     return locs
# def query_cell_locations(cells):
#     logging.info('query_cell_locations %s' % (cells))
#     locs = []
#     nearbts = ''
#     bts = ''
#     i=0
#     celllen=len(cells)
#     if (celllen < 6):
#         for cell1 in cells:
#             try:
#                 cell=list(cell1)
#                 if cell[4] < -100:
#                     break
#                 cell[4] = -20
#                 i=i+1
#                 if (i ==1):
#                     bts =','.join(str(i) for i in cell)
#                 else:
#                     nearbts = nearbts + "|" + ','.join(str(i) for i in cell)
#             except Exception, e:
#                 logging.error('%s[%s %s %s %s]' % (e, cell[0], cell[1], cell[2], cell[3]))
#                 pass
#     else:
#         for cell1 in cells:
#             try:
#                 cell=list(cell1)
#                 if cell[4] < -100:
#                     break
#                 cell[4] = -20
#                 i=i+1
#                 if (i ==1):
#                     bts =','.join(str(i) for i in cell)
#                 elif(i ==2 or i==3):
#                     nearbts = nearbts + "|" + ','.join(str(i) for i in cell)
#             except Exception, e:
#                 logging.error('%s[%s %s %s %s]' % (e, cell[0], cell[1], cell[2], cell[3]))
#                 pass
#     http_url = 'http://apilocate.amap.com/position?accesstype=0&bts=%s&nearbts=%s&output=json&key=196c8358d7f7d9b3e3c5cd95e3ca5819' % (bts, nearbts)
#     logging.warn('url=%s' % (http_url))
#     r = requests.get(http_url)
#     type = r.json()['result']['type']
#     if (type != '0'):
#         lat = float(r.json()['result']['location'].split(',')[1])+0.002915
#         lng = float(r.json()['result']['location'].split(',')[0])-0.004905
#         radius = float(r.json()['result']['radius'])
#         locs.append((lat, lng, radius))
#     else:
#         logging.warn('cell not found for %s' % (bts))
#     return locs
def query_cell_locations(cells):
    logging.info('query_cell_locations %s' % (cells))
    locs = []
    nearbts = ''
    bts = ''
    i=0
    for cell1 in cells:
        try:
            cell = list(cell1)
            i=i+1
            if(cell[4] < -95):
                break
            cell[4] = -1
            if (i == 1):
                bts =','.join(str(i) for i in cell)
            else:
                nearbts = nearbts + "|" + ','.join(str(i) for i in cell)
        except Exception, e:
            logging.error('%s[%s %s %s %s]' % (e, cell[0], cell[1], cell[2], cell[3]))
            pass
    http_url = 'http://apilocate.amap.com/position?accesstype=0&bts=%s&nearbts=%s&output=json&key=196c8358d7f7d9b3e3c5cd95e3ca5819' % (bts, nearbts)
    r = requests.get(http_url)
    type = r.json()['result']['type']
    if (type != '0'):
        lat = float(r.json()['result']['location'].split(',')[1])+0.002915
        lng = float(r.json()['result']['location'].split(',')[0])-0.004905
        radius = float(r.json()['result']['radius'])
        locs.append((lat, lng, radius))
    return locs
# def query_cell_locations(cells):
#     locs = []
#     for cell in cells:
#         try:
#             http_url = 'http://apilocate.amap.com/position?accesstype=0&bts=%s,%s,%s,%s,-65s&output=json&key=196c8358d7f7d9b3e3c5cd95e3ca5819' % (cell[0], cell[1], cell[2], cell[3])
#             r = requests.get(http_url)
#             type=r.json()['result']['type']
#             if (type!='0'):
#                 # lat = float(r.json()['result']['location'].split(',')[1])+0.00265
#                 lat = float(r.json()['result']['location'].split(',')[1])+0.002915
#                 lng = float(r.json()['result']['location'].split(',')[0])-0.004905
#                 # lng = float(r.json()['result']['location'].split(',')[0])-0.00516
#                 radius = int(r.json()['result']['radius'])
#                 locs.append((lat, lng, radius))
#             else:
#                 logging.warn('cell not found for %s %s %s %s' % (cell[0], cell[1], cell[2], cell[3]))
#         except Exception, e:
#             logging.error('%s[%s %s %s %s]' % (e, cell[0], cell[1], cell[2], cell[3]))
#             pass
#     return locs
def Distance(lat1,lng1,lat2,lng2):
    radlat1=radians(lat1)  
    radlat2=radians(lat2)  
    a=radlat1-radlat2  
    b=radians(lng1)-radians(lng2)  
    s=2*asin(sqrt(pow(sin(a/2),2)+cos(radlat1)*cos(radlat2)*pow(sin(b/2),2)))  
    earth_radius=6378.137  
    s=s*earth_radius  
    if s<0:  
        return -s  
    else:  
        return s
        
def get_cell_pos(locs):
    d1 = Distance(locs[0][0],locs[0][1],locs[1][0],locs[1][1])    
    d2 = Distance(locs[0][0],locs[0][1],locs[2][0],locs[2][1])
    d3 = Distance(locs[1][0],locs[1][1],locs[2][0],locs[2][1])
    if d1<1 and d2<1 and d3<1:
        p = ((locs[0][0] + locs[1][0] + locs[2][0])/3.0, (locs[0][1] + locs[1][1] + locs[2][1])/3.0, 500)
    elif d1>1 and d2>1 and d3<1:
        p= ((locs[2][0] + locs[1][0])/2.0, (locs[2][1] + locs[1][1])/2.0, 500)
    elif d2>1 and d3>1 and d1<1:
        p= ((locs[1][0] + locs[0][0])/2.0, (locs[1][1] + locs[0][1])/2.0, 500)
    elif d1>1 and d3>1 and d2<1:
        p = ((locs[0][0] + locs[2][0])/2.0, (locs[0][1] + locs[2][1])/2.0, 500)
    else:
        p = ((locs[0][0] + locs[1][0] + locs[2][0])/3.0, (locs[0][1] + locs[1][1] + locs[2][1])/3.0, 500)
        
    return p
   
def calc_location(cells):
    # locs = db.get_cell_locations(cells)
    locs = query_cell_locations(cells)
    pos = (0, 0, 0)
    if len(locs) >= 3:
        # pos = get_cell_pos(locs)
        pos = ((locs[0][0] + locs[1][0] + locs[2][0]) / 3.0, (locs[0][1] + locs[1][1] + locs[2][1]) / 3.0, 500)
    elif len(locs) == 2:
        pos = ((locs[0][0] + locs[1][0])/2.0, (locs[0][1] + locs[1][1])/2.0, 500)
    elif len(locs) == 1:
        pos = (locs[0][0], locs[0][1], 500)
    #print pos
    logging.warn('--------locs====okok-----------------------------------')
    return pos
