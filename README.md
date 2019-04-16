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

# Literatur

https://www.thomaschristlieb.de/ein-python-script-mit-systemd-als-daemon-systemd-tut-garnicht-weh/