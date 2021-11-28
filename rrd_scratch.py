import rrdtool
import os

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
    test = rrdtool.graphv("-", "--start", "-1d", "-w 800", "--title=/scratch %s" % hostname,
                        "DEF:free=rrds/%s_scratch.rrd:free:LAST" % (hostname) ,
                        "DEF:total=rrds/%s_scratch.rrd:total:LAST" % (hostname) ,
                        "LINE1:total#0000FF:Total",
                        "LINE1:free#0000FF:Free",
                        "CDEF:unavailable=total,UN,INF,0,IF",
                        "AREA:unavailable#f0f0f0",
    )
    return test['image']

def insert(hostname, data, timestamp = "N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    rrdtool.update(rrdname, '%s:%s:%s' % (timestamp,data[0],data[1]))

def exists(hostname):
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_scratch.rrd"
        rrdtool.create(rrdname, '--start', '-2years',
            '--step 900',
            'DS:free:GAUGE:1200:0:10995116277760',
            'DS:total:GAUGE:1200:0:10995116277760',
            'RRA:AVERAGE:0.5:1:1200',
            'RRA:AVERAGE:0.5:6:1200',
            'RRA:AVERAGE:0.5:24:1200',
            'RRA:MIN:0.5:1:1200',
            'RRA:MIN:0.5:6:1200',
            'RRA:MIN:0.5:24:1200',
            'RRA:MAX:0.5:1:1200',
            'RRA:MAX:0.5:6:1200',
            'RRA:MAX:0.5:24:1200',
            'RRA:LAST:0.5:1:1200',
            'RRA:LAST:0.5:6:1200',
            'RRA:LAST:0.5:24:1200'
          )
        return True
    else:
        return False

def last(hostname): #FIXME - implement
    return -1