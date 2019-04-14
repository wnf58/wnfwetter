#! /usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import json
import geheim
import sqlite3

aLetzteTemp = 0.0


def isDatenbankOK():
    con = sqlite3.connect('wnftemp.db')
    cur = con.cursor()
    sql="""
CREATE TABLE `temp` (
	`id`	integer NOT NULL,
	`Timestamp`	INTEGER NOT NULL,
	`Temperatur`	INTEGER NOT NULL,
	`Dauer`	INTEGER NOT NULL,
	PRIMARY KEY(`id`)
);
    """
    cur.execute(sql)
    con.commit()
    return False


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("computer/esp1")


def on_message(client, userdata, msg):
    global aLetzteTemp
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
            s = time.strftime("%H:%M:%S")
            print('Messung: %s  Temperatur %s°C' % (s, "{0:.1f}".format(x)))
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
