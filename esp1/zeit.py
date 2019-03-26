import utime

def zeit():
    t=utime.localtime()
    return '%02d:%02d:%02d' % (t[3],t[4],t[5])

def datum():
    t=utime.localtime()
    return '%02d.%02d.%04d' % (t[2],t[1],t[0])
    

