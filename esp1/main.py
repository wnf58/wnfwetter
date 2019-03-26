import geheim
import network
import wlan
import os
import zeit
import network,esp,json,time
from umqtt.simple import MQTTClient

def getSendedaten():
    x = {'ID': esp.flash_id(),'IP' : network.WLAN().ifconfig()[0],'TIME': time.time()}
    return json.dumps(x)

wlan=wlan.wlan_connect(geheim.WLAN_SSID,geheim.WLAN_PW)
print('Dateien: ')
ff=os.listdir();
ff.sort()
for f in ff:
    print ('        '+f)
print('Aktuelle Zeit: ',zeit.zeit())
client = MQTTClient(geheim.CLIENT_ID,geheim.BBB_IP)
client.connect()
while True:
    j = getSendedaten()
    print(j)
    client.publish('computer/esp2', j)
    time.sleep(5)
