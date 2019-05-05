#! /usr/bin/python3
# -*- coding: utf-8 -*-

from bottle import route, get, template, static_file
import os
import time
import sqlite3
import wnf_wetter_const as C
import wnf_wetter_tools as T
import wnf_wetter_db as db

www = os.path.join(os.path.dirname(__file__), 'www')


def keinZugriff(daten):
    s = ('Kein Zugriff %s (Serverzeit %s)' % (C.PROGBUILD, (time.strftime("%d.%m.%Y %H:%M:%S"))))
    return template('<b>Hello {{name}}!</b><hr>{{meldung}}', name=daten, meldung=s)


def wetterstatus():
    aCaption = C.PROGNAME
    aCount, aDaten, aDatenKopf = db.dbListZeitGradAsRows()
    aLesbar = []
    for r in aDaten:
        aLesbar += [(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(r[0])), "{0:.1f}".format(r[1]))]
    print(aLesbar)
    output = template('wetter_status',
                      title=aCaption,
                      WetterStatus=statusZeilen(),
                      WetterCount=aCount,
                      WetterDaten=aLesbar,
                      WetterKopf=aDatenKopf
                      )
    return output


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root=os.path.join(www, "css"))


@get("/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root=os.path.join(www, "img"))


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root=os.path.join(www, "js"))


@get("/<filepath:re:.*\.html>")
def html(filepath):
    return static_file(filepath, root=www)


@get("/<filepath:re:.*\.json>")
def json(filepath):
    return static_file(filepath, root=www)


@get("/daten/<filepath:re:.*\.csv>")
def csv(filepath):
    return static_file(filepath, root=os.path.join(www, "daten"))


@route('/')
def index():
    return wetterstatus()


def statusZeilen():
    zeit, temp = db.letzterMesswert()
    zeit = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(zeit))
    temp = "{0:.1f}".format(temp)
    aStatus = (('Version', C.PROGBUILD),
               ('Proxy-Hostname', T.getHostname()),
               ('zuletzt aktualisiert', '%s (Serverzeit)' % (T.getHHMMSS())),
               ('letzter Messwert um', '%s ' % (zeit)),
               ('aktuelle Temperatur', '%s ' % (temp))
               )
    return aStatus


def wetterLinie(aUeberschrift, aCSVDatei):
    aCaption = C.PROGNAME
    output = template('wetter_linie',
                      title=aCaption,
                      WetterStatus=statusZeilen(),
                      Ueberschrift=aUeberschrift,
                      CSVDatei=aCSVDatei
                      )
    return output


@route('/100')
def route_100():
    dn = "wetter_100.csv"
    db.refresh_100(os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 100 Werte', dn)


@route('/07d')
def route_07d():
    dn = "wetter_07d.csv"
    db.refresh_xxTage(7, os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 7 Tage', dn)


@route('/28d')
def route_28d():
    dn = "wetter_28d.csv"
    db.refresh_xxTage(28, os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 4 Wochen', dn)


@route('/24h')
def route_24h():
    dn = 'wetter_24h.csv'
    db.refresh_24h(os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 24 Stunden', dn)


def isDatenbankOK():
    dn = T.iniGetDatenbank()
    if dn == '':
        return False
    con = sqlite3.connect(dn)
    cur = con.cursor()
    sql = 'select count(*) from zeitgrad'
    rows = cur.execute(sql)
    for r in rows:
        print('Bisher erfasste Datensätze %s' % r[0])
    con.commit()
    return True


def startBottle():
    from bottle import run, debug
    debug(True)
    aPortClient = T.iniGetBottlePort()
    run(host='0.0.0.0', port=aPortClient)


def main():
    # os.chdir(os.path.dirname(__file__))
    if isDatenbankOK():
        print('Starten wnf_wetter_http')
        startBottle()
    else:
        print('Die Datenbank konnte nicht geöffnet werden.')


if __name__ == '__main__':
    main()
