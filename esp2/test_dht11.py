import machine,dht,time

t = dht.DHT11(machine.Pin(5))

t.measure()
#time.sleep_ms(750*2)
print(t.temperature())
print(t.humidity())