#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月20日

@author: Jarvis
'''

import json
from bottle import Bottle, run
from requestlogger import WSGILogger, ApacheFormatter
from logging.handlers import TimedRotatingFileHandler
import config
import device as devicem
import db
import notification#测试围栏引入
import wait
import time, datetime
app = Bottle()


def response_json(code, msg='success', data=None):
    return '{"errcode":%d,"errmsg":"%s","data":%s}' % (code, msg, json.dumps(data))


@app.route('/server/devices', method='GET')
def server_devices():
    return response_json(0, data={'devices': devicem.get_device_count()})


@app.route('/server/servers', method='GET')
def server_servers():
    return '0'


@app.route('/device/<imei:re:[0-9]{15}>', method='GET')
def device(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    loc = None
    data = db.cacheobj_get_location(imei)
    if data:
        loc = {'lat': data[0], 'lng': data[1], 'time': data[2]}
    data = {'location': loc}
    data['active'] = db.cacheobj_get_device_online(imei)
    #data['active'] = db.http_get_device_online(imei)


    data['power'] = db.cacheobj_get_device_power(imei)
    data['rssi'] = db.cacheobj_get_device_rssi(imei)
    data['satellite'] = db.cacheobj_get_device_satellite(imei)
    flags = db.cacheobj_get_device_flags(imei)
    data['flag32'] = flags[0]
    data['flag8'] = flags[1]
    return response_json(0, data=data)


@app.route('/device/<imei:re:[0-9]{15}>/host', method='GET')
def device_getprop_host(imei):
    data = db.cacheobj_get_device_host(imei)
    if not data:
        return response_json(-1, 'no data')
    return response_json(0, data={'mqtt': {'host': data[0], 'port': data[1]}, 'web': {'host': data[2], 'port': data[3]},
                                  'server': data[4]})


@app.route('/device/<imei:re:[0-9]{15}>/loc', method='GET')
def device_getprop_loc(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    data = db.cacheobj_get_location(imei)
    if not data:
        return response_json(-1, 'no location')
    return response_json(0, data={'lat': data[0], 'lng': data[1], 'time': data[2]})


@app.route('/device/<imei:re:[0-9]{15}>/active', method='GET')
def device_getprop_active(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    return response_json(0, data={'active':db.cacheobj_get_device_online(imei)})
    #return response_json(0, data={'active': db.http_get_device_online(imei)})


@app.route('/device/<imei:re:[0-9]{15}>/power', method='GET')
def device_getprop_power(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    return response_json(0, data={'power': db.cacheobj_get_device_power(imei)})


@app.route('/device/<imei:re:[0-9]{15}>/users', method='POST')
def device_setprop_users(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.users = None
    dev.get_users()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/fences', method='POST')
def device_setprop_fences(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.fences = None
    dev.get_fences()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/config', method='POST')
def device_setprop_config(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.config = None
    dev.sync_config()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/phonebook', method='POST')
def device_setprop_phonebook(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.sync_phonebook()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/family', method='POST')
def device_setprop_family(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.sync_family()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/nodisturb', method='POST')
def device_setprop_nodisturb(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.sync_nodisturb()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/alarm', method='POST')
def device_setprop_alarm(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.sync_alarm()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/voice/<fromuser:re:[0-9]+>/<voiceid:re:[0-9]+>', method='POST')
def device_setprop_voice(imei, fromuser, voiceid):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.send_voice(fromuser, voiceid)
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/monitor/<fromuser:re:[0-9]+>', method='POST')
def device_setprop_monitor(imei, fromuser):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.monitor(fromuser)
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/reset', method='POST')
def device_shutdown(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.reset()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/shutdown', method='POST')
def device_shutdown(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.shutdown()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/find', method='POST')
def device_find(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.find()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/factory', method='POST')
def device_factory(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.factory()
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/loc', method='POST')
def device_loc(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    data1 = wait.waitObject('location', imei, 5, dev.loc)
    if not data1:
        return response_json(-2, 'Timeout')
    return response_json(0, data={'lat': data1[0], 'lng': data1[1], 'time': data1[2]})


@app.route('/device/<imei:re:[0-9]{15}>/takephoto/<fromuser:re:[0-9]+>/<sid>', method='POST')
def device_takephoto(imei, fromuser, sid):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.takephoto(fromuser, sid)
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/echo', method='POST')
def device_echo(imei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    if not wait.waitObject('echo', imei, 5, dev.echo):
        return response_json(-2, 'Timeout')
    return response_json(0)


@app.route('/device/<imei:re:[0-9]{15}>/newfriend/<friendimei:re:[0-9]{15}>', method='POST')
def device_new_friend(imei, friendimei):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')

    friend = db.get_device_record_by_imei(friendimei)
    dev.new_friend(friendimei, friend.device_phone, friend.device_name)
    return response_json(0)

@app.route('/device/<imei:re:[0-9]{15}>/mode/<value:re:[0-2]{1}>', method='POST')
def device_mode(imei, value):
    dev = devicem.get_device_from_imei(imei)
    if not dev:
        return response_json(-1, 'no device')
    dev.mode(value)
    record = dev.get_record()
    if not record:
        return
    db.update_config_mode(record.device_id, value)
    return response_json(0)

@app.route('/info')
def info():
    return 'Hello glaive'


# @app.route('/hello/<imei:re:[0-9]{15}>')
# def hello(imei):
#     return "hello"
@app.route('/hello/<imei:re:[0-9]{15}>')
def hello(imei):
    try:
        dev = devicem.get_device_from_imei(imei)
        users = db.get_users_by_device(dev.devid())
        power=666
        notification.low_power(dev.imei, users, power, dev.get_record().device_name)
        return '%s'%(dev.get_record().device_name)
        # dev = devicem.get_device_from_imei(imei)
        # if not dev:
        #     return response_json(-1, 'no device')
        # dev.shutdown()
        # return response_json(0)
    except Exception as e:
        return e
    pass



def web_server_start(param):
    try:
        run(app, host=config.web.host, port=config.web.port, debug=False, server='gevent')
    except Exception as e:
        print(e)
    pass


def web_server_start_localhost(param):
    try:
        run(app, host='localhost', port=config.web.port, debug=False, server='gevent')
    except Exception as e:
        print(e)
    pass
