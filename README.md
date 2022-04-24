# wnfwetter
Wetterstation 
- mit BeagleBoneBlack und 
- esp8266 mit Temperaturfühler ds18b20

# Ordner esp1
- für esp mit schwarzem Kabel (nur Temperaturmessung)
- Mikropython bearbeitet mit Thonny

# Ordner esp2
- für esp mit schwarzem Kabel (Temperaturmessung und Luft)
- Mikropython bearbeitet mit Thonny

# Ordner bbb
- für BeagleBoneBlack
- Mosquito als MQTT-Broker
- MQTT-Client zum Sammeln der Temperaturen
- Bottle zur Anzeige der Temperaturen

# Voraussetzungen

$ sudo pip3 install paho-mqtt

im Programmordner esp1 bzw. esp2 die Datei geheim.py anlegen

WLAN_SSID = 'FRITZ!Box'
WLAN_PW = 'xxxx'
CLIENT_ID = 'wnf_esp1'

im Programmordner bbb die Datei geheim.py anlegen

BBB_IP = '192.168.1.100'
BBB_SUBSCRIBE = '/Sensor/3B1B3A'

# Update

auf dem Entwicklungsrechner
$ verkauf_wetter.py
$ ssh bone2013 

auf dem BBB
(nicht immer nötig)
$ sudo service wnf_wetter_speicher stop
$ sudo service wnf_wetter_speicher start

$ sudo service wnf_wetter_http stop
$ sudo service wnf_wetter_http start
 


# Literatur

https://www.thomaschristlieb.de/ein-python-script-mit-systemd-als-daemon-systemd-tut-garnicht-weh/