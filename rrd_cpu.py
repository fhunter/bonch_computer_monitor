import rrdtool

def graph(hostname):
    test = rrdtool.graphv("-", "--start", "-1y", "-w 800", "--title=Load %s" % hostname,
        "DEF:load=rrds/%s_cpu.rrd:load:LAST" % (hostname) ,
        "DEF:cores=rrds/%s_cpu.rrd:cores:LAST" % (hostname) ,
        "DEF:loadavg=rrds/%s_cpu.rrd:loadavg:LAST" % (hostname) ,
        "LINE1:load#0000FF:load",
        "LINE2:cores#00FFFF:cores",
        "LINE3:loadavg#FF00FF:loadavg",
        "CDEF:unavailable=load,UN,INF,0,IF",
        "AREA:unavailable#f0f0f0",
        )
    return test['image']

def insert(hostname, data): #FIXME - implement
    return ""

def last(hostname): #FIXME - implement
    return -1
