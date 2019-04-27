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
    aStatus = (('Version', C.PROGBUILD),
               ('Proxy-Hostname', T.getHostname()),
               ('zuletzt aktualisiert', '%s (Serverzeit)' % (T.getHHMMSS()))
               )
    aCount, aDaten, aDatenKopf = db.dbListZeitGradAsRows()
    aLesbar = []
    for r in aDaten:
        aLesbar += [(r[0], time.strftime("%H:%M:%S", time.localtime(r[1])), "{0:.1f}".format(r[2]))]
    print(aLesbar)
    output = template('wnf_wetter_status',
                      title=aCaption,
                      WetterStatus=aStatus,
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


@get("/daten/<filepath:re:.*\.csv>")
def csv(filepath):
    return static_file(filepath, root=os.path.join(www, "daten"))


@route('/')
def index():
    return wetterstatus()


@route('/100')
def route_100():
    db.refresh_100(os.path.join(www, "daten", "wetter_100.csv"))
    db.refresh_24h(os.path.join(www, "daten", "wetter_24h.csv"))
    db.refresh_Woche(os.path.join(www, "daten", "wetter_woche.csv"))
    return html('wetter_100_werte.html')


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
