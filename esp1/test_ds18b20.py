import onewire,machine,time,ds18x20

ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(5)))

roms=ds.scan()
ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(rom,ds.read_temp(rom))