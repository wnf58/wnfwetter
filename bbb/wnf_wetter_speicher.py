#! /usr/bin/python3 -u
# -*- coding: utf-8 -*-

import os
import paho.mqtt.client as mqtt
import time
import json
import geheim
import sqlite3
import wnf_wetter_tools as T

aLetzteTemp = 0.0
aLetzteTime = time.time()


def isDatenbankOK():
    dn = T.iniGetDatenbank()
    if dn == '':
        return False
    con = sqlite3.connect(dn)
    cur = con.cursor()
    sql = """
create table if not exists zeitgrad (
    id integer primary key autoincrement ,
	zeit integer not null,
	grad numeric not null
);
    """
    cur.execute(sql)
    sql = "select count(*) from pragma_table_info('zeitgrad') where name = 'druck'"
    cur.execute(sql)
    for row in cur:
        if row[0] == 0:
            sql = 'alter table zeitgrad add column druck numeric null'
            cur.execute(sql)
            sql = 'alter table zeitgrad add column feucht numeric null'
            cur.execute(sql)
            con.commit()
    sql = 'select count(*) from zeitgrad'
    rows = cur.execute(sql)
    for r in rows:
        print('Bisher erfasste Datensätze %s' % r[0])
    con.commit()
    return True


def speicher(aZeit, aGrad, aDruck, aFeuchte):
    # print(aZeit, aGrad)
    con = sqlite3.connect(T.iniGetDatenbank())
    cur = con.cursor()
    sql = "INSERT INTO zeitgrad (zeit,grad,druck,feucht) VALUES (?,?,?,?)"
    cur.execute(sql, (aZeit, aGrad, aDruck, aFeuchte))
    con.commit()
    return cur.lastrowid


def updateLetzteZeit(aZeit):
    aID = 0
    # print(aZeit)
    con = sqlite3.connect(T.iniGetDatenbank())
    cur = con.cursor()
    sql = "SELECT MAX(id) FROM zeitgrad"
    rows = cur.execute(sql)
    for r in rows:
        aID = r[0]
    if aID > 0:
        sql = "UPDATE zeitgrad SET zeit = ? WHERE ID = ?"
        cur.execute(sql, (aZeit, aID))
    con.commit()
    return aID


def anzeigeID(aID):
    if aID:
        con = sqlite3.connect(T.iniGetDatenbank())
        cur = con.cursor()
        sql = "SELECT zeit,grad,druck,feucht,id FROM zeitgrad WHERE ID=%s" % (aID)
        rows = cur.execute(sql)
        for r in rows:
            s = time.strftime("%H:%M:%S", time.localtime(r[0]))
            print('Speicher: %s  Temperatur %s°C Luftdruck %s Luftfeuchtigkeit %s' % (s,
                                                     "{0:.1f}".format(r[1]),
                                                     "{0:.1f}".format(r[2]),
                                                     "{0:.1f}".format(r[3])
                                                     ))
        con.commit()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe("computer/esp1")
    client.subscribe(geheim.BBB_SUBSCRIBE)


def on_message(client, userdata, msg):
    global aLetzteTemp
    global aLetzteTime
    try:
        #print(client)
        #print(userdata)
        #print(type(msg))
        # print(msg.topic + " | "+str(msg.qos)+' | ' + str(msg.payload))
        aJson = json.loads(msg.payload.decode('utf8'))
        # print(aJson)
        # print(aJson['TEMP'])
        x = aJson['T']
        x = float("{0:.1f}".format(x))
        aZeit = time.time()
        if ((x >= aLetzteTemp + 0.25) or (x <= aLetzteTemp - 0.25)):
            aLetzteTemp = x
            # print(aJson['TIME'])
            # t = aJson['TIME']
            # s = time.strftime("%b %d %Y %H:%M:%S", time.gmtime(t))
            aGrad = x
            aLetzteTime = aZeit
            aDruck = aJson['L']
            aDruck = float("{0:.1f}".format(aDruck))
            aFeuchte = aJson['F']
            aFeuchte = float("{0:.1f}".format(aFeuchte))
            aID = speicher(aZeit, aGrad, aDruck, aFeuchte)
            s = time.strftime("%H:%M:%S")
            print('Messung : %s  Temperatur %s°C Luftdruck %s Luftfeuchtigkeit %s' % (s,
                                                                                      "{0:.1f}".format(aGrad),
                                                                                      "{0:.1f}".format(aDruck),
                                                                                      "{0:.1f}".format(aFeuchte)))
            anzeigeID(aID)
        elif (aZeit - aLetzteTime) > 60:
            # alle 60 Sekunden die Zeit aktualisieren, auch wenn die Tempereatur sich nicht ändert
            aID = updateLetzteZeit(aZeit)
            aLetzteTime = aZeit
            anzeigeID(aID)
    except Exception as E:
        print('Fehler', E)
        raise


def main():
    # os.chdir(os.path.dirname(__file__))
    if isDatenbankOK():
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(geheim.BBB_IP, 1883, 60)
        client.loop_forever()
    else:
        print('Die Datenbank konnte nicht geöffnet werden.')


if __name__ == '__main__':
    main()
