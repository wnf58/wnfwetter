import geheim
import network
import wlan
import os
import zeit
import network,esp,json,time
from umqtt.simple import MQTTClient
import onewire,machine,ds18x20

ds = None

def getTemperatur():
    roms=ds.scan()
    ds.convert_temp()
    for rom in roms:
        return ds.read_temp(rom)
    return None

def getSendedaten():
    x = {'ID': esp.flash_id(),'IP' : network.WLAN().ifconfig()[0],'TIME': time.time(), 'TEMP': getTemperatur()}
    return json.dumps(x)

def initTemperatur():
    global ds
    ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(5)))
    roms=ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(rom,ds.read_temp(rom))


wlan=wlan.wlan_connect(geheim.WLAN_SSID,geheim.WLAN_PW)
print('Dateien: ')
ff=os.listdir();
ff.sort()
for f in ff:
    print ('        '+f)
print('Aktuelle Zeit: ',zeit.zeit())

initTemperatur()

client = MQTTClient(geheim.CLIENT_ID,geheim.BBB_IP)
client.connect()
while True:
    j = getSendedaten()
    print(j)
    client.publish('computer/esp1', j)
    time.sleep(5)
