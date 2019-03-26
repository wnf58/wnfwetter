import ntptime,utime


def wlan_connect(ssid, password):
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        print('verbinden nach:', ssid)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
        ntptime.NTP_DELTA = 3155673600-3600
        print('Zeit einstellen')
        ntptime.settime()
    print('Netzwerk:', wlan.ifconfig()[0])
    return wlan

