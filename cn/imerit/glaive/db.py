#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月20日

@author: Jarvis
'''

from sqlobject import *
import redis
import time, datetime
import logging
import config
import json
import requests
from __builtin__ import True


def init_database():
    global cacheobj
    sqlhub.processConnection = connectionForURI(
        '%s://%s:%s@%s:%s/%s?use_unicode=1&charset=utf8' % (config.database.provider,
                                                            config.database.user,
                                                            config.database.password,
                                                            config.database.host,
                                                            config.database.port,
                                                            config.database.db))

    cacheobj = redis.Redis(host=config.redis.host, port=config.redis.port, db=0)


init_database()


class ZltDevice(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'device_id'

    device_id = IntCol()
    device_imei = StringCol(length=24, default=None)
    device_card = StringCol(length=32, default=None)
    device_name = StringCol(length=24, default=None)
    device_status = IntCol()
    device_debug = IntCol()
    device_position = IntCol()
    device_app = IntCol()
    device_type = IntCol()
    device_owner = IntCol()
    device_master = IntCol()
    device_debug = IntCol()
    device_cardsupply = IntCol()
    device_phone = StringCol()
    board_model = StringCol(length=100)
    product_name = StringCol(length=100)
    finesMap = RelatedJoin('ZltFine', joinColumn='fine_map_device', otherColumn='fine_map_fine',
                           intermediateTable='zlt_fine_map')


class ZltDeviceConfig(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'device_config_id'

    device_config_id = IntCol()
    device_config_interval = IntCol()
    device_config_udinterval = IntCol()
    device_config_host = StringCol(length=128)
    device_config_port = IntCol()
    device_config_heartbeat = IntCol()
    device_config_serverid = StringCol(length=24)
    device_config_config = IntCol()
    device_config_mode = IntCol()


class ZltCellid(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'cellid_id'

    cellid_id = IntCol()
    cellid_device = IntCol()
    cellid_info = StringCol(length=255, default=None)
    cellid_time = TimestampCol()


class ZltCelldata(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'celldata_id'

    celldata_id = IntCol()
    celldata_mcc = IntCol()
    celldata_mnc = IntCol()
    celldata_cid = IntCol()
    celldata_lac = IntCol()
    celldata_lat = FloatCol()
    celldata_lng = FloatCol()
    celldata_accuracy = IntCol()


class ZltLocation(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'location_id'

    location_id = IntCol()
    location_device = IntCol()
    location_uptime = TimestampCol()
    location_lati = FloatCol()
    location_longi = FloatCol()
    location_time = TimestampCol()
    location_speed = FloatCol()
    location_course = FloatCol()
    location_eleva = FloatCol()
    location_accuracy = FloatCol()
    location_cellid = FloatCol()


class ZltLocationRt(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'location_id'

    location_id = IntCol()
    location_device = IntCol()
    location_uptime = TimestampCol()
    location_lati = FloatCol()
    location_longi = FloatCol()
    location_time = TimestampCol()
    location_speed = FloatCol()
    location_course = FloatCol()
    location_eleva = FloatCol()
    location_accuracy = FloatCol()
    location_cellid = FloatCol()


class ZltFine(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'fine_id'

    fine_id = IntCol()
    fine_user = IntCol()
    fine_name = StringCol(length=128)
    fine_type = IntCol()
    fine_lng1 = FloatCol()
    fine_lat1 = FloatCol()
    fine_lng2 = FloatCol()
    fine_lat2 = FloatCol()
    devicesMap = RelatedJoin('ZltDevice', joinColumn='fine_map_fine', otherColumn='fine_map_device',
                             intermediateTable='zlt_fine_map')
    status = 0


class ZltFineMap(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'fine_map_id'

    fine_map_id = IntCol()
    fine_map_fine = IntCol()
    fine_map_device = IntCol()


class ZltUser(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'user_id'

    user_id = IntCol()
    user_name = StringCol()
    user_lang = StringCol()


class ZltUsertoken(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'usertoken_id'

    usertoken_id = IntCol()
    usertoken_user = IntCol()
    usertoken_app = IntCol()


class ZltAppcfg(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'appcfg_id'

    appcfg_id = IntCol()
    appcfg_app = IntCol()
    appcfg_key = StringCol()
    appcfg_value = StringCol()


class ZltBind(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'bind_id'

    bind_id = IntCol()
    bind_device = IntCol()
    bind_user = IntCol()
    bind_valid = IntCol()
    bind_nick = StringCol()
    device = ForeignKey('ZltDevice', dbName='bind_device')
    user = ForeignKey('ZltUser', dbName='bind_user')


class ZltVoice(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'voice_id'

    voice_id = IntCol()
    voice_from = StringCol()
    voice_to = StringCol()
    voice_url = StringCol()
    voice_duration = IntCol()
    voice_time = TimestampCol()
    voice_post = IntCol()
    voice_read = IntCol()


class ZltPhoto(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'photo_id'

    photo_id = IntCol()
    photo_device = IntCol()
    photo_to = StringCol(length=255)
    photo_url = StringCol(length=255)


class ZltEvent(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'event_id'

    event_id = IntCol()
    event_jpushid = StringCol(length=32)
    event_recipient = IntCol()
    event_type = IntCol()
    event_time = TimestampCol()
    event_extra = StringCol()
    event_status = IntCol()


class ZltDevicepb(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'devicepb_id'

    devicepb_id = IntCol()
    devicepb_device = IntCol()
    devicepb_phone = StringCol()
    devicepb_name = StringCol()


class ZltDevicend(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'devicend_id'

    devicend_id = IntCol()
    devicend_device = IntCol()
    devicend_begin = IntCol()
    devicend_end = IntCol()
    devicend_repeat = StringCol()


class ZltDevicestudy(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'devicestudy_id'

    devicestudy_id = IntCol()
    devicestudy_device = IntCol()
    devicestudy_code = StringCol()
    devicestudy_time = TimestampCol()


class ZltClock(SQLObject):
    class sqlmeta:
        lazyUpdate = True
        idName = 'id'

    clock_device = IntCol()
    clock_begin = IntCol()
    clock_repeat = StringCol(length=8)
    about = StringCol(length=200)


def insert_location(devid, rtime, lat, lng, alt, speed, bearing, accuracy, cellloc):
    logging.info("insert_location %s" % (devid))
    try:
        now = datetime.datetime.fromtimestamp(time.time())
        gpstime1 = datetime.datetime.fromtimestamp(rtime)
        loc = ZltLocation(location_id=None, location_device=devid, location_uptime=now, location_time=gpstime1,
                          location_lati=lat, location_longi=lng, location_speed=speed, location_course=bearing,
                          location_eleva=alt, location_accuracy=accuracy, location_cellid=cellloc)
        loc.syncUpdate()
        return loc.location_id
    except Exception as e:
        logging.error(e)
    return 0
    pass


def insert_realtime_location(devid, rtime, lat, lng, alt, speed, bearing, accuracy, cellloc):
    logging.info("insert_realtime_location %s" % (devid))
    try:
        now = datetime.datetime.fromtimestamp(time.time())
        gpstime1 = datetime.datetime.fromtimestamp(rtime)
        results = ZltLocationRt.selectBy(location_device=devid)
        locRt = results.getOne(None)
        if (locRt == None):
            locRt = ZltLocationRt(location_id=None, location_device=devid, location_uptime=now, location_time=gpstime1,
                                  location_lati=lat, location_longi=lng, location_speed=speed, location_course=bearing,
                                  location_eleva=alt, location_accuracy=accuracy, location_cellid=cellloc)
            locRt.syncUpdate()
        else:
            locRt.location_uptime = now
            locRt.location_time = gpstime1
            locRt.location_lati = lat
            locRt.location_longi = lng
            locRt.location_speed = speed
            locRt.location_course = bearing
            locRt.location_eleva = alt
            locRt.location_accuracy = accuracy
            locRt.location_cellid = cellloc
            locRt.syncUpdate()
        return locRt.location_id
    except Exception as e:
        logging.error(e)
    return 0
    pass


# def insert_cell_location(devid, rtime, info):
#     logging.info("insert_cell_location %s"%(devid))
#     try:
#         gpstime = datetime.datetime.fromtimestamp(rtime)
#         cell = ZltCellid(cellid_id=None, cellid_device=devid, cellid_info=info, cellid_time=gpstime)
#         cell.syncUpdate()
#         return cell.cellid_id
#     except Exception as e:
#         logging.error(e)
#     return 0
#     pass
def insert_cell_location(devid, rtime, info):
    logging.info("insert_cell_location %s" % (devid))
    try:
        gpstime = datetime.datetime.fromtimestamp(rtime)
        results = ZltCellid.selectBy(cellid_device=devid)
        cellId = results.getOne(None)
        if (cellId == None):
            cellId = ZltCellid(cellid_id=None, cellid_device=devid, cellid_info=info, cellid_time=gpstime)
            cellId.syncUpdate()
        else:
            cellId.cellid_info = info
            cellId.cellid_time = gpstime
            cellId.syncUpdate()
        return cellId.cellid_id
    except Exception as e:
        logging.error(e)
    return 0
    pass

def delete_cellid(devid):
    logging.info("delete_cellid_location %s" % (devid))
    try:
        results = ZltCellid.selectBy(cellid_device=devid)
        cellId = results.getOne(None)
        if not cellId:
            return
        cellId.delete(cellId.cellid_id)
        return cellId.cellid_id
    except Exception as e:
        logging.error(e)
def insert_voice(fromid, recipient, url, dur):
    logging.info("insert_voice %s %s" % (fromid, recipient))
    try:
        now = datetime.datetime.fromtimestamp(time.time())
        voicedb = ZltVoice(voice_id=None, voice_from=fromid, voice_to=recipient, voice_duration=dur, voice_time=now,
                           voice_post=0, voice_url=url, voice_read=0)
        voicedb.syncUpdate()
        return voicedb.voice_id
    except Exception as e:
        logging.error(e)
    return 0
    pass


def insert_event(recipient, jpushid, type, extras, status):
    logging.info("insert_event %s" % (recipient))
    try:
        now = datetime.datetime.fromtimestamp(time.time())
        event = ZltEvent(event_id=None, event_jpushid=jpushid, event_recipient=recipient, event_time=now,
                         event_type=type, event_extra=extras, event_status=status)
        event.syncUpdate()
        return event.event_id
    except Exception as e:
        logging.error(e)
    return 0
    pass


def insert_photo(dev, recipient, url):
    logging.info("insert_photo %s" % (dev.devid()))
    try:
        photo = ZltPhoto(photo_id=None, photo_device=dev.devid(), photo_to=recipient, photo_url=url)
        photo.syncUpdate()
        return photo.photo_id
    except Exception as e:
        logging.error(e)
        pass
    return 0


def insert_study(dev, datas):
    results = []
    for d in datas:
        try:
            t = datetime.datetime.fromtimestamp(float(d['time']))
            study = ZltDevicestudy(devicestudy_id=None, devicestudy_device=dev.devid(), devicestudy_code=d['code'],
                                   devicestudy_time=t)
            study.syncUpdate()
            results.append(study.devicestudy_id)
            pass
        except Exception as e:
            results.append(0)
            pass
    return results


def get_voice(vocid):
    logging.info("get_voice %s" % (vocid))
    try:
        voicedb = ZltVoice.select(ZltVoice.q.voice_id == vocid)
        return voicedb.getOne()
    except Exception, e:
        logging.error(e)
    return None


def get_cellid(device):
    logging.info("get_cellid %s" % (device))
    try:
        results = ZltCellid.selectBy(cellid_device=device)
        rec = results.getOne(None)
        return rec
    except Exception, e:
        # logging.error(e)
        return e


def update_voice_read(vocid, status):
    logging.info("update_voice_read %s" % (vocid))
    try:
        result = ZltVoice.select(ZltVoice.q.voice_id == vocid)
        voicedb = result.getOne(None)
        voicedb.voice_read = status
        voicedb.syncUpdate()
    except Exception as e:
        logging.error(e)
    pass


def get_unread_voice(voiceto):
    logging.info("get_unread_voice %s" % (voiceto))
    try:
        results = ZltVoice.select(ZltVoice.q.voice_to == voiceto and ZltVoice.q.voice_read == -1)
        return list(results)
    except Exception as e:
        logging.error(e)
    pass


def get_device_record_by_imei(imei):
    logging.info("get_device_record_by_imei %s" % (imei))
    try:
        results = ZltDevice.selectBy(device_imei=imei)
        rec = results.getOne(None)
        return rec
    except Exception as e:
        logging.error(e)
        return None


def get_device_record_by_phone(phone):
    logging.info("get_device_record_by_phone %s" % (phone))
    try:
        result = ZltDevice.select(ZltDevice.q.device_phone == phone)
        return result.getOne(None)
    except Exception as e:
        logging.error(e)
        return None


def get_device_config(device):
    logging.info("get_device_config %s" % (device))
    try:
        results = ZltDeviceConfig.selectBy(device_config_id=device)
        cfg = results.getOne(None)
        if not cfg:
            default = config.default
            cfg = ZltDeviceConfig(device_config_id=device, device_config_interval=default.device_interval,
                                  device_config_udinterval=default.device_udinterval,
                                  device_config_host=default.device_host,
                                  device_config_port=default.device_port,
                                  device_config_heartbeat=default.device_heartbeat,
                                  device_config_serverid=default.device_server_id,
                                  device_config_config=default.device_config,
                                  device_config_mode=default.device_mode)
            cfg.syncUpdate()
        return cfg
    except Exception as e:
        logging.error(e)
        return None


def update_config_mode(device, value):
    logging.info("update_config_mode %s" % (value))
    try:
        result = ZltDeviceConfig.selectBy(device_config_id=device)
        modedb = result.getOne(None)
        if not modedb:
            return
        modedb.device_config_mode = int(value)
        modedb.syncUpdate()
    except Exception as e:
        logging.error(e)
    pass


def update_cell_loction_time(device, rtime):
    logging.info("update_cell_loction %s" % (rtime))
    try:
        result = ZltLocationRt.selectBy(location_device=device)
        loc = result.getOne(None)
        # if not loc:
        #     return
        # time = datetime.datetime.fromtimestamp(rtime)
        loc.location_time = rtime
        loc.syncUpdate()
        return loc
    except Exception as e:
        return e
    pass


def get_alarms(device):
    logging.info("get_alarms %s" % (device))
    try:
        results = ZltClock.select(ZltClock.q.clock_device == device)
        return list(results)
    except Exception as e:
        logging.error(e)
        return []


def get_fences_by_device(device):
    logging.info("get_fences_by_device %s" % (device))
    try:
        results = ZltDevice.select(ZltDevice.q.device_id == device).throughTo.finesMap
        return list(results)
    except Exception as e:
        logging.error(e)
        return []


def get_users_by_device(device):
    logging.info("get_users_by_device %s" % (device))
    try:
        results = ZltBind.select(AND(ZltBind.q.bind_device == device, ZltBind.q.bind_valid == 1)).throughTo.user
        return list(results)
    except Exception as e:
        logging.error(e)
        return []


def get_bind_users_by_device(device):
    logging.info("get_bind_users_by_device %s" % (device))
    try:
        results = ZltBind.select(AND(ZltBind.q.bind_device == device, ZltBind.q.bind_valid == 1))
        return list(results)
    except Exception as e:
        logging.error(e)
        return []


def get_user(userid):
    logging.info("get_user %s" % (userid))
    try:
        results = ZltUser.select(ZltUser.q.user_id == userid)
        return results.getOne()
    except Exception as e:
        logging.error(e)
        return None


def get_user_by_name(username):
    logging.info("get_user_by_name %s" % (username))
    try:
        results = ZltUser.select(ZltUser.q.user_name == username)
        return results.getOne()
    except Exception as e:
        logging.error(e)
        return None


def get_user_logged_app(userid):
    try:
        results = ZltUsertoken.select(ZltUsertoken.q.usertoken_user == userid).orderBy('-usertoken_tokentime')
        return list(results)[0].usertoken_app
    except Exception as e:
        logging.error(e)
        return None


def get_app_jpush_config(appid):
    try:
        results = ZltAppcfg.select(AND(ZltAppcfg.q.appcfg_app == appid, ZltAppcfg.q.appcfg_key == 'jpush_appkey'))
        appkey = results.getOne().appcfg_value
        results = ZltAppcfg.select(AND(ZltAppcfg.q.appcfg_app == appid, ZltAppcfg.q.appcfg_key == 'jpush_secret'))
        secret = results.getOne().appcfg_value
        return (appkey, secret)
    except Exception as e:
        logging.error(e)
        return None


def get_phonebook_by_device(device):
    logging.info("get_phonebook_by_device %s" % (device))
    try:
        results = ZltDevicepb.select(ZltDevicepb.q.devicepb_device == device)
        return list(results)
    except Exception as e:
        logging.error(e)
        return []


def find_phonebook(device, phone):
    try:
        results = ZltDevicepb.select(
            AND(ZltDevicepb.q.devicepb_device == device, ZltDevicepb.q.devicepb_phone == phone))
        return results.getOne()
    except Exception as e:
        logging.error(e)
        return None


def make_friends(dev, imeiOther):
    logging.info("make_friends %s %s" % (dev.devid(), imeiOther))
    try:
        rec = dev.get_record()
        rec1 = get_device_record_by_imei(imeiOther)
        pb1ret = ZltDevicepb.select(
            AND(ZltDevicepb.q.devicepb_device == rec.device_id, ZltDevicepb.q.devicepb_phone == rec1.device_phone))
        if not pb1ret.count():
            pb1 = ZltDevicepb(devicepb_id=None, devicepb_device=rec.device_id, devicepb_phone=rec1.device_phone,
                              devicepb_name=rec1.device_name)
            pb1.syncUpdate()
    except Exception as e:
        logging.error(e)


def get_nodisturb_by_device(device):
    logging.info("get_nodisturb_by_device %s" % (device))
    try:
        results = ZltDevicend.select(ZltDevicend.q.devicend_device == device)
        return list(results)
    except Exception as e:
        logging.error(e)
        return []


def get_cell_locations(cells):
    logging.info("get_cell_locations")
    locs = []
    for cell in cells:
        results = ZltCelldata.selectBy(celldata_mcc=cell[0], celldata_mnc=cell[1], celldata_lac=cell[2],
                                       celldata_cid=cell[3])
        try:
            result = results.getOne()
            if (result):
                # logging.info('found for %d %d %d %d =%d, %f,%f,%f'%(cell[0],cell[1],cell[2],cell[3],result.celldata_id,result.celldata_lat,result.celldata_lng,result.celldata_accuracy))
                locs.append((result.celldata_lat, result.celldata_lng, result.celldata_accuracy, cell[4]))
            else:
                logging.warn('cell not found for %s %s %s %s' % (cell[0], cell[1], cell[2], cell[3]))
        except Exception, e:
            logging.error('%s[%s %s %s %s]' % (e, cell[0], cell[1], cell[2], cell[3]))
            pass
    return locs


def get_unread_events(userid):
    logging.info("get_unread_events %s" % (userid))
    events = ZltEvent.select(ZltEvent.q.recipient == userid and ZltEvent.q.status == 0)
    if not events:
        return 0
    return events.count()
    pass


def cacheobj_set_device_power(imei, power, time):
    logging.info("cacheobj_set_device_power %s" % (imei))
    cacheobj.set('%s/power' % (imei), '%d' % (power), time)


def cacheobj_get_device_power(imei):
    logging.info("cacheobj_get_device_power %s" % (imei))
    try:
        val = cacheobj.get('%s/power' % (imei))
        if not val:
            return 0
        return int(val)
    except Exception, e:
        logging.error(val, e)
        pass
    return 0


def cacheobj_set_device_rssi(imei, rssi, time):
    logging.info("cacheobj_set_device_rssi %s" % (imei))
    cacheobj.set('%s/rssi' % (imei), '%d' % (rssi), time)


def cacheobj_get_device_rssi(imei):
    logging.info("cacheobj_get_device_rssi %s" % (imei))
    try:
        val = cacheobj.get('%s/rssi' % (imei))
        if not val:
            return 0
        return int(val)
    except Exception, e:
        logging.error(val, e)
        pass
    return 0


def cacheobj_set_device_satellite(imei, satellite, time):
    logging.info("cacheobj_set_device_satellite %s" % (imei))
    cacheobj.set('%s/satellite' % (imei), '%d' % (satellite), time)


def cacheobj_get_device_satellite(imei):
    logging.info("cacheobj_get_device_satellite %s" % (imei))
    try:
        val = cacheobj.get('%s/satellite' % (imei))
        if not val:
            return 0
        return int(val)
    except Exception, e:
        logging.error(val, e)
        pass
    return 0


def cacheobj_set_device_flags(imei, flags, time):
    logging.info("cacheobj_set_device_flags %s" % (imei))
    cacheobj.set('%s/flags' % (imei), '%d,%d' % flags, time)


def cacheobj_get_device_flags(imei):
    logging.info("cacheobj_get_device_flags %s" % (imei))
    try:
        val = cacheobj.get('%s/flags' % (imei))
        if not val:
            return (0, 0)
        return val.split(',')[:2]
    except Exception, e:
        logging.error(val, e)
        pass
    return (0, 0)


def cacheobj_set_device_online(imei, status, time):
    logging.info("cacheobj_set_device_online %s" % (imei))
    cacheobj.set('%s/online' % (imei), '%d' % (status), time)


def cacheobj_clear_device(imei):
    logging.info("cacheobj_clear_device %s" % (imei))
    cacheobj.delete('%s/online' % (imei))
    cacheobj.delete('%s/location' % (imei))
    cacheobj.delete('%s/power' % (imei))


def cacheobj_get_device_online(imei):
    logging.info("cacheobj_get_device_online %s" % (imei))
    try:
        val = cacheobj.get('%s/online' % (imei))
        if not val:
            return 0
        return int(val)
    except Exception, e:
        logging.error(val, e)
        pass
    return 0


def http_get_device_online(imei):
    logging.info("http_get_device_online %s" % (imei))
    try:
        r = requests.get(config.mqtt.api_url + '?' + config.mqtt.api_client_param + '=' + imei,
                         auth=(config.mqtt.user, config.mqtt.password))
        if len(r.json()['result']) == 0:
            return 0
        return 1
    except Exception, e:
        logging.error(r, e)
        pass
    return 0


def cacheobj_set_device_location(imei, lat, lng, rtime, time):
    logging.info("cacheobj_set_device_location %s" % (imei))
    cacheobj.set('%s/location' % (imei), '%f,%f,%d' % (lat, lng, int(rtime)), time)


def cacheobj_get_location(imei):
    logging.info("cacheobj_get_location %s" % (imei))
    try:
        val = cacheobj.get('%s/location' % (imei))
        if not val:
            return None
        vals = val.split(',')
        return (float(vals[0]), float(vals[1]), int(vals[2]))
    except Exception, e:
        logging.error(val, e)
        pass
    return None


def cacheobj_set_device_fence_status(imei, fenceid, status, time):
    logging.info("cacheobj_set_device_fence_status %s status=%d" % (imei,status))
    cacheobj.set('%s/fence/%d' % (imei, fenceid), '%d' % (status), time)


def cacheobj_get_device_fence_status(imei, fenceid):
    logging.info("cacheobj_get_device_fence_status %s" % (imei))
    try:
        val = cacheobj.get('%s/fence/%d' % (imei, fenceid))
        if not val:
            return 0
        return int(val)
    except Exception, e:
        logging.error(val, e)
        pass
    return 0


def cacheobj_set_server(id, addr, mqtt_host, mqtt_port, web_port):
    logging.info("cacheobj_set_server %s" % (id))
    cacheobj.set('%s/addr' % (id), '%s,%s,%d,%d' % (addr, mqtt_host, int(mqtt_port), int(web_port)), 0)


def cacheobj_set_device_host(imei, mqtthost, mqttport, webhost, webport, server):
    logging.info("cacheobj_set_device_host %s" % (imei))
    cacheobj.set('%s/host' % (imei), '%s,%d,%s,%d,%s' % (mqtthost, int(mqttport), webhost, int(webport), server), 0)


def cacheobj_get_device_host(imei):
    logging.info("cacheobj_get_device_host %s" % (imei))
    try:
        val = cacheobj.get('%s/host' % (imei))
        if not val:
            return None
        vals = val.split(',')
        return (vals[0], int(vals[1]), vals[2], int(vals[3]), vals[4])
    except Exception, e:
        logging.error(val, e)
        pass
    return None


def cacheobj_get_friend_match_cache():
    logging.info("cacheobj_get_friend_match_cache")
    try:
        val = cacheobj.get('friend_match_cache')
        if not val:
            return {}
        return json.loads(val)
    except Exception, e:
        logging.error(val, e)
        pass
    return {}


def cacheobj_set_friend_match_cache(caches):
    logging.info("cacheobj_set_friend_match_cache")
    val = json.dumps(caches)
    cacheobj.set('friend_match_cache', val, config.friend_match.timeout)

