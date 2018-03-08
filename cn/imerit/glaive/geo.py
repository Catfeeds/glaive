#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月20日

@author: Jarvis
'''

from math import *

earth_radius = 6376137

def distance(lat1,lng1,lat2,lng2):
    radlat1=radians(lat1)  
    radlat2=radians(lat2)
    a=radlat1-radlat2  
    b=radians(lng1)-radians(lng2)
    s=2*asin(sqrt(pow(sin(a/2),2)+cos(radlat1)*cos(radlat2)*pow(sin(b/2),2)))  
    earth_radius=6378137
    s=s*earth_radius  
    if s<0:
        return -s  
    else:  
        return s