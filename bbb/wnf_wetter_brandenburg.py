import json
import os
import urllib.request


def refresh_xx(dn, aWerte):
    aMinZ = 30
    aMaxZ = -20
    print(dn)
    with open(dn, 'x') as out:
        s = 'Datum,Temperatur'
        out.write(s + '\n')
    alt1 = 100
    alt2 = 100
    if aWerte:
        # print(aWerte)
        for r in aWerte:
            # print(r)
            # gleitender Durchschnitt
            aTemp = r['temperatur']
            if alt2 != 100:
                x = (aTemp + alt1 + alt2) / 3
            else:
                x = aTemp
            if alt2 != 100:
                aZeit = r['zeit']
                aZeit = aZeit.replace('-', '/')
                # print(aZeit)
                s = "%s,%s" % (aZeit, "{0:.1f}".format(x))
                # print(s)
                if aMinZ > aTemp:
                    aMinZ = aTemp
                if aMaxZ < aTemp:
                    aMaxZ = aTemp
                with open(dn, 'a') as out:
                    out.write(s + '\n')
            alt2 = alt1
            alt1 = aTemp
    aMinG = -20
    aMaxG = 30
    return aMinG, aMaxG, aMinZ, aMaxZ


def brandenburgTempToCSV(aTage, aDateiname):
    # Die Datei wird nur alle Minute neu geschrieben
    if os.path.exists(aDateiname):
        # if time.time() - os.path.getmtime(aDateiname) < 60:
        #    return
        os.remove(aDateiname)
    with urllib.request.urlopen('https://wetter.nfix.de/werte?tage=%s' % aTage) as url:
        data = json.load(url)
        # print(data)
        rec = data[0]
        # print(rec)
        werte = rec['werte']
        aMinMax = refresh_xx(aDateiname, werte)
    return aMinMax


def brandenburgTemperatur():
    try:
        with urllib.request.urlopen("https://wetter.nfix.de/aktuell") as url:
            data = json.load(url)
            rec = data[0]
            werte = rec['werte']
            temp = werte['temperatur']
            temp = str(temp)
    except Exception as E:
        print(E)
        temp = '?.?'
    return temp


def main():
    www = os.path.join(os.path.dirname(__file__), 'www')
    dn = "wetter_bb_24h.csv"
    print(brandenburgTemperatur())
    aMinMax = brandenburgTempToCSV(1, os.path.join(www, "daten", dn))
    print(aMinMax)

if __name__ == '__main__':
    main()
