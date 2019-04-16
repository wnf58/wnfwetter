import sqlite3
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
