#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月19日

@author: Jarvis
'''


from gevent import monkey
monkey.patch_all()

import cn.imerit.glaive.config as config
import getopt,os,sys,time,logging,traceback

def usage():
    pass

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'h:p:c:', ['id=','help'])
    for op, value in opts:
        if(op == '-c'):
            #dir = os.path.dirname(value)
            #file = os.path.splitext(os.path.basename(value))[0]
            #sys.path.append(dir)
            #exec 'import %s'%(file)
            logging.basicConfig(format=config.log.format, level=config.log.level, filename=config.log.file)
    for op, value in opts:
        if(op == '--id'):
            config.id = value
        elif(op == '-h'):
            config.mqtt.host = value
        elif(op == '-p'):
            config.mqtt.port = value
        elif(op == '--help'):
            usage()
            exit(0)
    from cn.imerit.glaive import server
    server.start()
    pass