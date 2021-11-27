import rrdtool

def graph(hostname):
    test = rrdtool.graphv("-", "--start", "-1y", "-w 800", "--title=Uptime %s" % hostname,
        "DEF:uptime=rrds/%s_uptime.rrd:uptime:LAST" % (hostname) ,
        "LINE1:uptime#0000FF:Uptime",
        "CDEF:unavailable=uptime,UN,INF,0,IF",
        "AREA:unavailable#f0f0f0",
        )
    return test['image']

def insert(hostname, data): #FIXME - implement
    return ""

def last(hostname): #FIXME - implement
    return -1
