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
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(aTimespamp))


def getDyGraphsDate(aDatum):
    # 2009/07/12 12:34:56
    aDatum = aDatum.split('-')
    aDatum = "%s/%s/%s 12:00:00" % (aDatum[0], aDatum[1], aDatum[2])
    # print(aDatum)
    return aDatum


def getDyGraphsMonth(aDatum):
    # 2009/07/12 12:34:56
    print(aDatum)
    aDatum = aDatum.split('-')
    print(aDatum)
    aDatum = "%s/%s/01 12:00:00" % (aDatum[1], aDatum[0])
    # print(aDatum)
    return aDatum


def calcLuftdruck(aLuftdruck, aTemperatur, aHoehenMeter):
    # https://rechneronline.de/barometer/
    """
    Der Temperaturgradient gibt an, wie schnell die Temperatur mit der Höhe fällt.
    Eine gute Schätzung bei normalem Wetter ist 0,0065 °C/Meter.
    Temperaturschätzung: Temperatur auf Meereshöhe = Temperatur + Temperaturgradient * Höhe
    Barometrische Höhenformel:
    Luftdruck auf Meereshöhe = Barometeranzeige / (1-Temperaturgradient*Höhe/Temperatur auf Meereshöhe in Kelvin)^(0,03416/Temperaturgradient)
    """
    aBarometeranzeige = aLuftdruck / 100
    aTemperaturgradient = 0.0065
    # Temperatur  auf Meereshöhe = Temperatur + Temperaturgradient * Höhe
    aTemp_0 = aTemperatur + aTemperaturgradient * aHoehenMeter
    print(aTemp_0)
    # Umrechnung in K
    aTemp_0 = aTemp_0 + 273.15
    # x = (1-Temperaturgradient*Höhe/Temperatur auf Meereshöhe in Kelvin)
    x = 1 - (aTemperaturgradient * aHoehenMeter) / aTemp_0
    # y = (0,03416/Temperaturgradient)
    y = (0.03416 / aTemperaturgradient)
    z = x ** y
    print(z)
    aLuftdruck = aBarometeranzeige / z
    aLuftdruck = int(aLuftdruck)
    return aLuftdruck


def calcLuftdruckNF(aLuftdruck, aTemperatur):
    return calcLuftdruck(aLuftdruck, aTemperatur, 340)


def getLuftdruckRec(aLuftdruck, aTemperatur):
    aLuftdruck = calcLuftdruck(aLuftdruck, aTemperatur, 340)
    if aLuftdruck < 980:
        s = 'sehr tief, stürmisch'
    elif aLuftdruck < 1000:
        s = 'tief, regnerisch'
    elif aLuftdruck < 1020:
        s = 'normal, wechselhaft'
    elif aLuftdruck < 1040:
        s = 'hoch, sonnig'
    else:
        s = 'sehr hoch, sehr trocken'
    return aLuftdruck, s


def main():
    aLuftdruck = 99070.0
    aTemperatur = 25
    print(getLuftdruckRec(aLuftdruck, aTemperatur))


if __name__ == "__main__":
    main()
