""" Module for manipulating free and used space statistics on /scratch in RRD database files """
import os
from functools import lru_cache
import rrdtool
from period import period_conv

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

@lru_cache(maxsize=128)
def graph(hostname, period):
    test = rrdtool.graphv("-", "--start",
                        period_conv(period), "-w 800", "--title=/scratch %s" % hostname,
                        "DEF:free=rrds/%s_scratch.rrd:free:LAST" % (hostname) ,
                        "DEF:total=rrds/%s_scratch.rrd:total:LAST" % (hostname) ,
                        "LINE2:total#009F00:Total",
                        "LINE2:free#FF00FF:Free",
                        "CDEF:unavailable=total,UN,INF,0,IF",
                        "AREA:unavailable#f0f0f0",
    )
    return test['image']

def insert(hostname, data, timestamp = "N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    rrdtool.update(rrdname, '%s:%s:%s' % (timestamp,data[0],data[1]))
    graph.cache_clear()

def exists(hostname):
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_scratch.rrd"
        rrdtool.create(rrdname, '--start', '-2years',
            '--step', '900',
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
    return False

def last(hostname):
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    try:
        last_time = rrdtool.last(rrdname)
    except:
        return None
    return last_time

def latest(hostname):
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    try:
        info = rrdtool.info(rrdname)
        lastupdate = [info['last_update'],
                      int(info['ds[total].last_ds']),
                      int(info['ds[free].last_ds'])]
        return lastupdate
    except:
        return None
