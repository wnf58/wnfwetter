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
    aCaption = "%s.%d" % (C.PROGNAME, C.PROGBUILD)
    aStatus = (('Version', aCaption),
                         ('Proxy-Hostname', T.getHostname()),
                         ('zuletzt aktualisiert', '%s (Serverzeit)' % (T.getHHMMSS()))
                         )
    aCount, aDaten,aDatenKopf = db.dbListZeitGradAsRows()
    aLesbar=[]
    for r in aDaten:
        aLesbar+=[(r[0],time.strftime("%H:%M:%S",time.localtime(r[1])),"{0:.1f}".format(r[2]))]
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


@route('/')
def index():
    return wetterstatus()


def isDatenbankOK():
    dn = T.iniGetDatenbank()
    if dn=='':
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
    #os.chdir(os.path.dirname(__file__))
    if isDatenbankOK():
        print('Starten wnf_wetter_http')
        startBottle()
    else:
        print('Die Datenbank konnte nicht geöffnet werden.')


if __name__ == '__main__':
    main()
