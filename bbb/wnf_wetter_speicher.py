#! /usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import json
import geheim
import sqlite3

aLetzteTemp = 0.0
aLetzteTime = time.time()


def isDatenbankOK():
    con = sqlite3.connect('wnftemp.db')
    cur = con.cursor()
    sql = """
create table if not exists zeitgrad (
    id integer primary key autoincrement ,
	zeit integer not null,
	grad numeric not null
);
    """
    cur.execute(sql)
    sql = 'select count(*) from zeitgrad'
    rows = cur.execute(sql)
    for r in rows:
        print('Bisher erfasste Datensätze %s' % r[0])
    con.commit()
    return True


def speicher(aZeit, aGrad):
    print(aZeit, aGrad)
    con = sqlite3.connect('wnftemp.db')
    cur = con.cursor()
    sql = "INSERT INTO zeitgrad (zeit,grad) VALUES (?,?)"
    cur.execute(sql, (aZeit, aGrad))
    con.commit()
    return cur.lastrowid


def anzeigeID(aID):
    if aID:
        con = sqlite3.connect('wnftemp.db')
        cur = con.cursor()
        sql = "SELECT zeit,grad,id FROM zeitgrad WHERE ID=%s" % (aID)
        rows = cur.execute(sql)
        for r in rows:
            s = time.strftime("%H:%M:%S",time.localtime(r[0]))
            print('Speicher: %s  Temperatur %s°C' % (s, "{0:.1f}".format(r[1])))
        con.commit()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("computer/esp1")


def on_message(client, userdata, msg):
    global aLetzteTemp
    global aLetzteTime
    try:
        # print(client)
        # print(userdata)
        # print(msg)
        # print(msg.topic + " " + str(msg.payload))
        aJson = json.loads(msg.payload.decode('utf8'))
        # print(aJson)
        # print(aJson['TEMP'])
        x = aJson['TEMP']
        x = float("{0:.1f}".format(x))
        if ((x >= aLetzteTemp + 0.25) or (x <= aLetzteTemp - 0.25)):
            aLetzteTemp = x
            # print(aJson['TIME'])
            # t = aJson['TIME']
            # s = time.strftime("%b %d %Y %H:%M:%S", time.gmtime(t))
            aZeit = time.time()
            aGrad = x
            aLetzteTime = aZeit
            aID = speicher(aZeit, aGrad)
            s = time.strftime("%H:%M:%S")
            print('Messung : %s  Temperatur %s°C' % (s, "{0:.1f}".format(x)))
            anzeigeID(aID)
    except Exception as E:
        print('Fehler', E)
        raise


def main():
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
