#! /usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import sqlite3
import time
# Das alles fürs Logging
from datetime import datetime
from functools import wraps

from bottle import route, get, template, static_file, request, response

import wnf_wetter_const as C
import wnf_wetter_db as db
import wnf_wetter_tools as T
from wnf_wetter_brandenburg import brandenburgTemperatur, brandenburgTempToCSV, brandenburgWerte

logger = logging.getLogger('wnf_wetter_http')

# set up the logger
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('wnf_wetter_http.log')
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_to_logger(fn):
    '''
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    '''
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        # modify this to log exactly what you need:
        logger.info('%s %s %s %s %s' % (request.remote_addr,
                                        request_time,
                                        request.method,
                                        request.url,
                                        response.status))
        return actual_response
    return _log_to_logger

www = os.path.join(os.path.dirname(__file__), 'www')

def keinZugriff(daten):
    s = ('Kein Zugriff %s (Serverzeit %s)' % (C.PROGBUILD, (time.strftime("%d.%m.%Y %H:%M:%S"))))
    return template('<b>Hello {{name}}!</b><hr>{{meldung}}', name=daten, meldung=s)

def formatWert(aWert):
    if aWert:
        return "{0:.1f}".format(aWert)
    else:
        return ''


def wetterstatus():
    aCaption = C.PROGNAME
    aCount, aDaten, aDatenKopf = db.dbListZeitGradAsRows()
    aLesbar = []
    for r in aDaten:
        aLesbar += [(time.strftime("%d.%m.%Y %H:%M:%S",
                     time.localtime(r[0])),
                     formatWert(r[1]),
                     formatWert(r[2]),
                     formatWert(r[3])
                     )]
    print(aLesbar)
    aTemperatur = statusZeilen()[4][1]
    output = template('wetter_status',
                      title=aCaption,
                      AktuelleTemperatur=aTemperatur,
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
    zeit, aTemperatur, aDruck, aFeuchte = db.letzterMesswert()
    print(aTemperatur)
    return wetterThermometer('Nf', aTemperatur)
    # return wetterThermometer_2('Nf', aTemperatur)
    # return wetterstatus()


def letzteTempNF():
    zeit, aTemp, aDruck, aFeuchte = db.letzterMesswert()
    return aTemp


def statusZeilen():
    zeit, aTemp, aDruck, aFeuchte = db.letzterMesswert()
    zeit = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(zeit))
    r = T.getLuftdruckRec(aDruck,aTemp)
    aTemp = "{0:.1f}".format(aTemp)
    aDruck = "{0:.1f}".format(int(aDruck/100))
    aFeuchte = "{0:.1f}".format(aFeuchte)
    aStatus = (('Version', C.PROGBUILD),
               ('Proxy-Hostname', T.getHostname()),
               ('zuletzt aktualisiert', '%s (Serverzeit)' % (T.getHHMMSS())),
               ('letzter Messwert um', '%s ' % (zeit)),
               ('aktuelle Temperatur', '%s °C' % (aTemp)),
               ('aktueller Luftdruck', '%s hPa' % (aDruck)),
               ('normierter Luftdruck', '%s hPa ' % (r[0])),
               ('Wetterlage', '%s ' % (r[1])),
               ('aktuelle Luftfeuchtigkeit', '%s %%' % (aFeuchte))
               )
    return aStatus


def statusZeilen_BB(aTemperatur, aZeit):
    aStatus = ((
        ('letzter Messwert um', '%s ' % (aZeit)),
        ('Temperatur', '%s ' % (aTemperatur))
    ))
    return aStatus


def wetterTemperatur(aStatus):
    aTemperatur = aStatus[4][1]
    aLetzterWert = aStatus[3][1]
    # print(aLetzterWert, type(aLetzterWert))
    aLetzterWert = T.strToDateTime(aLetzterWert)
    # print(aLetzterWert, type(aLetzterWert))
    aLetzterWert = datetime.now() - aLetzterWert
    aLetzterWert = aLetzterWert.total_seconds()
    if aLetzterWert > 60:
        aTemperatur = 'Kein Messwert'
    return aTemperatur


def wetterLinie(aUeberschrift, aCSVDatei, aMinMax):
    print(aMinMax)
    print(type(aMinMax))
    aCaption = C.PROGNAME
    aStatus = statusZeilen()
    aTemperatur = wetterTemperatur(aStatus)
    aBrandenburg = brandenburgTemperatur()[0]
    output = template('wetter_linie',
                      title=aCaption,
                      AktuelleTemperatur=aTemperatur,
                      WetterStatus=aStatus,
                      Ueberschrift=aUeberschrift,
                      CSVDatei=aCSVDatei,
                      rangemin=aMinMax[0],
                      rangemax=aMinMax[1],
                      MinTemperatur=aMinMax[2],
                      MaxTemperatur=aMinMax[3],
                      BBTemperatur=aBrandenburg
                      )
    return output


def wetterThermometer(aUeberschrift, aTemperatur):
    aCaption = C.PROGNAME
    T.thermometer_1_Template(aTemperatur)
    output = template('thermometer',
                      title=aCaption,
                      Ueberschrift=aUeberschrift,
                      AktuelleTemperatur=aTemperatur
                      )
    return output


def wetterThermometer_2(aUeberschrift, aTemperatur):
    aCaption = C.PROGNAME
    T.thermometer_1_Template(aTemperatur)
    output = template('thermometer_2_template',
                      title=aCaption,
                      Ueberschrift=aUeberschrift,
                      AktuelleTemperatur=aTemperatur
                      )
    return output


def wetterLinie_BB(aUeberschrift, aCSVDatei, aMinMax):
    print(aMinMax)
    print(type(aMinMax))
    aCaption = C.PROGNAME
    aTemperatur, aZeit = brandenburgTemperatur()
    aStatus = statusZeilen_BB(aTemperatur, aZeit)
    aNiederfrohna = letzteTempNF()
    output = template('wetter_linie_bb',
                      title=aCaption,
                      AktuelleTemperatur=aTemperatur,
                      WetterStatus=aStatus,
                      Ueberschrift=aUeberschrift,
                      CSVDatei=aCSVDatei,
                      rangemin=aMinMax[0],
                      rangemax=aMinMax[1],
                      MinTemperatur=aMinMax[2],
                      MaxTemperatur=aMinMax[3],
                      NFTemperatur=aNiederfrohna
                      )
    return output


def wetterWerte_BB(aUeberschrift, aTage):
    aCount, aDaten, aDatenKopf = brandenburgWerte(aTage)
    aTemperatur = brandenburgTemperatur()[0]
    output = template('wetter_werte_bb',
                      Ueberschrift=aUeberschrift,
                      AktuelleTemperatur=aTemperatur,
                      WetterCount=aCount,
                      WetterDaten=aDaten,
                      WetterKopf=aDatenKopf
                      )
    return output


def wetterMinMax(aUeberschrift, aCSVDatei, aMinMax):
    aCaption = C.PROGNAME
    aStatus = statusZeilen()
    aTemperatur = wetterTemperatur(aStatus)
    aBBTemperatur = brandenburgTemperatur()[0]
    output = template('wetter_minmax',
                      title=aCaption,
                      AktuelleTemperatur=aTemperatur,
                      BBTemperatur=aBBTemperatur,
                      WetterStatus=aStatus,
                      Ueberschrift=aUeberschrift,
                      CSVDatei=aCSVDatei,
                      rangemin=aMinMax[0],
                      rangemax=aMinMax[1],
                      MinTemperatur=aMinMax[2],
                      MaxTemperatur=aMinMax[3]
                      )
    return output


@route('/100')
def route_100():
    dn = "wetter_100_minmax.csv"
    aMinMax = db.refresh_100_MinMax(os.path.join(www, "daten", dn))
    return wetterMinMax('Die letzten 100 Werte', dn, aMinMax)

@route('/13m')
def route_13m():
    dn = "wetter_13m_minmax.csv"
    aMinMax = db.refresh_xxMonateMinMax(13, os.path.join(www, "daten", dn))
    return wetterMinMax('Die letzten 13 Monate', dn, aMinMax)


@route('/thermometer')
def route_thermometer():
    zeit, aTemperatur, aDruck, aFeuchte = db.letzterMesswert()
    print(aTemperatur)
    return wetterThermometer('Nf', aTemperatur)

@route('/07d')
def route_07d():
    dn = "wetter_07d.csv"
    aMinMax = db.refresh_xxTage(7, os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 7 Tage', dn, aMinMax)


@route('/28d')
def route_28d():
    dn = "wetter_28d.csv"
    aMinMax = db.refresh_xxTage(28, os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 4 Wochen', dn, aMinMax)


@route('/24h')
def route_24h():
    dn = 'wetter_24h.csv'
    aMinMax = db.refresh_24h(os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 24 Stunden', dn, aMinMax)


@route('/48h')
def route_48h():
    dn = 'wetter_48h.csv'
    aMinMax = db.refresh_48h(os.path.join(www, "daten", dn))
    return wetterLinie('Die letzten 48 Stunden', dn, aMinMax)

@route('/bb_24h')
def route_bb_24h():
    dn = "wetter_bb_24h.csv"
    aMinMax = brandenburgTempToCSV(1,os.path.join(www, "daten", dn))
    return wetterLinie_BB('BB Die letzten 24 Stunden', dn, aMinMax)

@route('/bb_48h')
def route_bb_48h():
    dn = "wetter_bb_48h.csv"
    aMinMax = brandenburgTempToCSV(2,os.path.join(www, "daten", dn))
    return wetterLinie_BB('BB Die letzten 48 Stunden', dn, aMinMax)


@route('/bb_thermometer')
def route_bb_thermometer():
    aTemp = brandenburgTemperatur()[0]
    aTemp = float(aTemp)
    # return wetterThermometer('BB', aTemp)
    return route_bb_07d()

@route('/bb_07d')
def route_bb_07d():
    dn = "wetter_bb_07d.csv"
    aMinMax = brandenburgTempToCSV(7,os.path.join(www, "daten", dn))
    return wetterLinie_BB('BB Die letzte Woche', dn, aMinMax)

@route('/bb_avg_07d')
def route_bb_avg_07d():
    return wetterWerte_BB('BB Die letzte Woche', 7)

@route('/bb_avg_28d')
def route_bb_avg_28d():
    return wetterWerte_BB('BB Die letzte Woche', 28)

@route('/bb_28d')
def route_bb_28d():
    dn = "wetter_bb_28d.csv"
    aMinMax = brandenburgTempToCSV(28,os.path.join(www, "daten", dn))
    return wetterLinie_BB('BB Die letzten 4 Wochen', dn, aMinMax)

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
    from bottle import run, debug, install
    debug(True)
    install(log_to_logger)
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
