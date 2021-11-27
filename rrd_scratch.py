import rrdtool

#rrdtool create termserver2_scratch.rrd \
#    --start $(date +%s --date="-2years") \
#    --step 900 \
#    DS:free:GAUGE:1200:0:10995116277760 \
#    DS:total:GAUGE:1200:0:10995116277760 \
#    RRA:AVERAGE:0.5:1:1200 \
#    RRA:AVERAGE:0.5:6:1200 \
#    RRA:AVERAGE:0.5:24:1200 \
#    RRA:MIN:0.5:1:1200 \
#    RRA:MIN:0.5:6:1200 \
#    RRA:MIN:0.5:24:1200 \
#    RRA:MAX:0.5:1:1200 \
#    RRA:MAX:0.5:6:1200 \
#    RRA:MAX:0.5:24:1200 \
#    RRA:LAST:0.5:1:1200 \
#    RRA:LAST:0.5:6:1200 \
#    RRA:LAST:0.5:24:1200

def graph(hostname):
    test = rrdtool.graphv("-", "--start", "-1y", "-w 800", "--title=/scratch %s" % hostname,
        "DEF:free=rrds/%s_scratch.rrd:free:LAST" % (hostname) ,
        "DEF:total=rrds/%s_scratch.rrd:total:LAST" % (hostname) ,
        "LINE1:total#0000FF:Total",
        "LINE1:free#0000FF:Free",
        "CDEF:unavailable=total,UN,INF,0,IF",
        "AREA:unavailable#f0f0f0",
        )
    return test['image']

def insert(hostname, data): #FIXME - implement
    return ""

def last(hostname): #FIXME - implement
    return -1
