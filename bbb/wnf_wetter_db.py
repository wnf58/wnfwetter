import sqlite3
import time
import os
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


def dbListZeitGradAsRows():
    try:
        aSQL = 'SELECT COUNT(*) FROM ZEITGRAD'
        anz = dbCount(aSQL)
        aSQL = "SELECT id,zeit,grad FROM zeitgrad ORDER BY ID DESC"
        aKopf = ('ID', 'Zeit', 'Temperatur')
        return anz, dbListTabelleAsRows(aSQL), aKopf
    except:
        return 0, (), ()

def refresh_xx(dn,aSQL):
    # Die Datei wird nur alle Minute neu geschrieben
    if os.path.exists(dn):
        if (time.time() - os.path.getmtime(dn)<60):
            return
        os.remove(dn)
    print(dn)
    with open(dn, 'x') as out:
        s = 'Datum,Temperatur'
        out.write(s + '\n')
    rows = dbListTabelleAsRows(aSQL)
    if rows:
        # print(rows)
        for r in rows:
            #print(r[0])
            # 2009/07/12 12:34:56
            #s = '20070101,62,39'
            s = "%s,%s" % (T.getDyGraphsDateTime(r[1]),"{0:.1f}".format(r[2]))
            # print(s)
            with open(dn, 'a') as out:
                out.write(s + '\n')
    return

def refresh_100(dn):
    aSQL = "SELECT id,zeit,grad FROM zeitgrad ORDER BY ID DESC LIMIT 100"
    refresh_xx(dn,aSQL)
    return

def refresh_24h(dn):
    t = time.time() - (24 * 60 * 60)
    # print(t)
    aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID DESC" % t
    refresh_xx(dn,aSQL)
    return

def refresh_Woche(dn):
    t = time.time() - (7 * 24 * 60 * 60)
    # print(t)
    aSQL = "SELECT id,zeit,grad FROM zeitgrad WHERE zeit > %d ORDER BY ID DESC" % t
    refresh_xx(dn,aSQL)
    return


def main():
    #refresh_100('/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_100.csv')
    #refresh_24h('/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_24h.csv')
    refresh_Woche('/home/wnf/Entwicklung/PycharmProjects/wnfwetter/bbb/www/daten/wetter_woche.csv')


if __name__ == '__main__':
    main()
