import os
import configparser
import socket
import time
import wnf_wetter_const as C


def _error(s):
    print('ERROR: %s' % s)


def iniGetString(aSection, aKey):
    try:
        ini = configparser.ConfigParser()
        dn = os.path.join(os.path.dirname(__file__), C.INIDATEINAME)
        ini.read(dn)
        config = ini[aSection]
        if config:
            s = config.get(aKey)
            if s:
                return s
            else:
                return ''
        else:
            return ''
    except Exception as E:
        # _error(E.args)
        _error('In der Inidatei %s ist kein Wert in Section [%s] für Schlüssel %s festgelegt.' % (
        C.INIDATEINAME, aSection, aKey))
        return ''


def iniGetSectionDatenbank(aKey):
    return iniGetString('Datenbank', aKey)


def iniGetDatenbank():
    return iniGetSectionDatenbank('DB_Name')


def iniGetSectionBottle(aKey):
    return iniGetString('Bottle', aKey)


def iniGetBottlePort():
    return int(iniGetSectionBottle('Port'))


def getHostname():
    return socket.gethostname()


def getHHMMSS():
    return time.strftime("%H:%M:%S")


def getDatumHHMMSS():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def getDyGraphsDateTime(aTimespamp):
    # 2009/07/12 12:34:56
    return time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(aTimespamp))
