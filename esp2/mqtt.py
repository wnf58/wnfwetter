import network,esp,json,time
from umqtt.simple import MQTTClient 

def getSendedaten():
    x = {'ID': esp.flash_id(),'IP' : network.WLAN().ifconfig()[0],'TIME': time.time()}
    return json.dumps(x)

client = MQTTClient('wnf','192.168.80.106')
client.connect()
while True:
    j = getSendedaten()    
    print(j)
    client.publish('computer/esp1', j)
    time.sleep(3)