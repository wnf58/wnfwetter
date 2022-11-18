import json
import urllib.request


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
    print(brandenburgTemperatur())


if __name__ == '__main__':
    main()
