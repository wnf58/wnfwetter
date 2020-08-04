import sqlite3
import time
import datetime
import os
from dateutil.relativedelta import *
import wnf_wetter_tools as T
import wnf_wetter_const as C

Datenbank = None


def verbinden():
    global Datenbank
    try:
        dn = T.iniGetDatenbank()
        if dn == '':
            return False
        Datenbank = sqlite3.connect(dn)
        cur = Datenbank.cursor()
        sql = """
        create table if not exists zeitgrad (
            id integer primary key autoincrement ,
        	zeit integer not null,
        	grad numeric not null
        );
            """
        cur.execute(sql)
        Datenbank.commit()
        sql = "select count(*) from pragma_table_info('zeitgrad') where name = 'druck'"
        cur.execute(sql)
        for row in cur:
            if row[0] == 0:
                sql = 'alter table zeitgrad add column druck numeric null'
                cur.execute(sql)
                sql = 'alter table zeitgrad add column feucht numeric null'
                cur.execute(sql)
                Datenbank.commit()
        return Datenbank

    except Exception as E:
        print('Exception beim Verbinden mit der Datenbank. (%s)' % dn)
        print(E)
        return None


def datenbankVerbinden():
    return verbinden()


def getConnection():
    return verbinden()


def getConCursor():
    con = verbinden()
    return con, con.cursor()


def getAnzahlMesswerte(aCursor):
    aSQL = "select count(*) from zeitgrad"
    aCursor.execute(aSQL)
    for row in aCursor:
        return row[0]
    return 0


def sqlOpen(aCursor, aSQL):
    aCursor.execute(aSQL)


def sqlDate(aDatum):
    return "'%s'" % aDatum


def dbCursorSQL(aSQL):
    # Falls über Nacht die Verbindung zur Datenbank verloren
    # gegangen ist, neu Verbinden
    global Datenbank
    if Datenbank is None:
        Datenbank = datenbankVerbinden()
    if Datenbank is None:
        return None
    cursor = Datenbank.cursor()
    cursor.execute(aSQL)
    return cursor


def dbCount(aSQL):
    cursor = dbCursorSQL(aSQL)
    if not cursor:
        return 0
    r = cursor.fetchone()
    if r:
        if len(r) == 1:
            return r[0]
        else:
            return 0
    else:
        return 0


def dbListTabelleAsRows(aSQL):
    cursor = dbCursorSQL(aSQL)
    if not cursor:
        return None
    return cursor.fetchall()


def letzterMesswert():
    try:
        aSQL = "SELECT zeit,grad,druck,feucht FROM zeitgrad ORDER BY ID DESC LIMIT 1"
        cursor = dbCursorSQL(aSQL)
        if not cursor:
            return 0, 0, 0, 0
        r = cursor.fetchone()
        if r:
            if len(r) == 4:
                return r[0], r[1], r[2], r[3]
            else:
                return 0, 0, 0, 0
        else:
            return 0, 0, 0, 0
    except:
        return 0, 0, 0, 0


def dbListZeitGradAsRows():
    try:
        aSQL = 'SELECT COUNT(*) FROM ZEITGRAD'
        anz = dbCount(aSQL)
        aSQL = "SELECT zeit,grad,druck,feucht FROM zeitgrad ORDER BY ID DESC  LIMIT 400"
        aKopf = ('Zeit', 'Temperatur', 'Luftdruck', 'Luftfeuchtigkeit')
        return anz, dbListTabelleAsRows(aSQL), aKopf
    except Exception as E:
        print('Fehler', E)
        return 0, (), ()


def refresh_xx(dn, aSQL):
    # Die Datei wird nur alle Minute neu geschrieben
    if os.path.exists(dn):
        if (time.time() - os.path.getmtime(dn) < 60):
            return
        os.remove(dn)
    print(dn)
    with open(dn, 'x') as out:
        s = 'Datum,Temperatur'
        out.write(s + '\n')
    rows = dbListTabelleAsRows(aSQL)
    alt1 = 100
    alt2 = 100
    if rows:
        # print(rows)
        for r in rows:
            # print(r[0])
            # 2009/07/12 12:34:56
            # s = '20070101,62,39'
            # s = "%s,%s" % (T.getDyGraphsDateTime(r[1]), "{0:.1f}".format(r[2]))
            # gleitender Durchschnitt
            if (alt2 != 100):
                x = (r[2] + alt1 + alt2) / 3
            else:
                x = r[2]
            if (alt2 != 100):
                s = "%s,%s" % (T.getDyGraphsDateTime(r[1]), "{0:.1f}".format(x))
                # print(s)
                with open(dn, 'a') as out:
                    out.write(s + '\n')
            alt2 = alt1
            alt1 = r[2]
    return


def refresh_MinMaxMonth(dn, aSQL):
    # Die Datei wird nur alle Minute neu geschrieben
    if os.path.exists(dn):
        if (time.time() - os.path.getmtime(dn) < 60):
            return
        os.remove(dn)
    print(dn)
    with open(dn, 'x') as out:
        s = 'Datum,TempMin,TempMax'
        out.write(s + '\n')
    rows = dbListTabelleAsRows(aSQL)
    if rows:
        # print(rows)
        for r in rows:
            # print(r)
            # 2009/07/12 12:34:56
            # s = '20070101,62,39'
            # s = "%s,%s" % (T.getDyGraphsDateTime(r[1]), "{0:.1f}".format(r[2]))
            # gleitender Durchschnitt
            aMax = r[2]
            aMin = r[1]
            s = "%s,%s,%s" % (T.getDyGraphsMonth(r[0]), "{0:.1f}".format(aMin), "{0:.1f}".format(aMax))
            print(s)
            with open(dn, 'a') as out:
                out.write(s + '\n')
    return

def refresh_MinMaxDate(dn, aSQL):
    # Die Datei wird nur alle Minute neu geschrieben
    if os.path.exists(dn):
        if (time.time() - os.path.getmtime(dn) < 60):
            return
        os.remove(dn)
    print(dn)
    with open(dn, 'x') as out:
        s = 'Datum,TempMin,TempMax'
        out.write(s + '\n')
    rows = dbListTabelleAsRows(aSQL)
    if rows:
        # print(rows)
        for r in rows:
            # print(r)
            # 2009/07/12 12:34:56
            # s = '20070101,62,39'
            # s = "%s,%s" % (T.getDyGraphsDateTime(r[1]), "{0:.1f}".format(r[2]))
            # gleitender Durchschnitt
            aMax = r[2]
            aMin = r[1]
            s = "%s,%s,%s" % (T.getDyGraphsDate(r[0]), "{0:.1f}".format(aMin), "{0:.1f}".format(aMax))
            print(s)
            with open(dn, 'a') as out:
                out.write(s + '\n')
    return


def refresh_100(dn):
    # t = time.time() - (24 * 60 * 60)
    # aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID DESC LIMIT 100" % t
    aSQL = "SELECT id,zeit,grad FROM zeitgrad ORDER BY ID DESC LIMIT 100"
    refresh_xx(dn, aSQL)
    return


def refresh_100_MinMax(dn):
    # t = time.time() - (24 * 60 * 60)
    # aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID DESC LIMIT 100" % t
    aSQL = """
SELECT
date(zeit,'unixepoch') as Datum,
min(grad) as Minimum,
max(grad) as Maximum, 
max(grad) - min(grad) as Differenz,
count(*) as Anzahl 
FROM zeitgrad
GROUP BY date(zeit,'unixepoch')
ORDER BY zeit DESC
LIMIT 100
    """
    refresh_MinMaxDate(dn, aSQL)
    return


def refresh_24h(dn):
    t = time.time() - (26 * 60 * 60)
    # print(t)
    aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID" % t
    refresh_xx(dn, aSQL)
    return


def refresh_48h(dn):
    t = time.time() - (50 * 60 * 60)
    # print(t)
    aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID" % t
    refresh_xx(dn, aSQL)
    return


def refresh_Woche(dn):
    t = time.time() - (7 * 24 * 60 * 60)
    # print(t)
    aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID" % t
    refresh_xx(dn, aSQL)
    return


def refresh_xxTage(aTage, dn):
    t = time.time() - (aTage * 24 * 60 * 60)
    # print(t)
    aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID" % t
    refresh_xx(dn, aSQL)
    return


def refresh_xxMonateMinMax(aMonate, dn):
    t = datetime.datetime.now() + relativedelta(months=-aMonate)
    print(t)
    aSQL = """
        SELECT
        strftime("%%m-%%Y", zeit,'unixepoch') as 'Monat', 
        min(grad) as Minimum,
        max(grad) as Maximum, 
        max(grad) - min(grad) as Differenz,
        count(*) as Anzahl 
        FROM zeitgrad
        WHERE zeit > %d
        GROUP BY strftime("%%m-%%Y", zeit,'unixepoch')
        ORDER BY zeit DESC
        LIMIT 100
        """
    aSQL = aSQL % t.timestamp()
    refresh_MinMaxMonth(dn, aSQL)
    return


def main():
    print(T.iniGetDatenbank())
    # refresh_100('/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_100.csv')
    # refresh_24h('/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_24h.csv')
    # refresh_Woche('/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_woche.csv')
    # print(letzterMesswert())
    # print(dbListZeitGradAsRows())
    refresh_100_MinMax('/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_100_minmax.csv')
    #refresh_xxMonateMinMax(13, '/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_minmax.csv')


if __name__ == '__main__':
    main()
