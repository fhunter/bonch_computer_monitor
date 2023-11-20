import os
import rrdtool
from period import period_conv
from functools import lru_cache

#rrdtool create termserver2_cpu.rrd \
#    --start $(date +%s --date="-2years") \
#    --step 900 \
#    DS:load:GAUGE:1200:0:5000 \
#    DS:loadavg:GAUGE:1200:0:5000 \
#    DS:cores:GAUGE:1200:0:5000 \
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
def graph1(hostname, period):
    test = rrdtool.graphv("-", "--start", period_conv(period), "-w 800", "--title=Load %s" % hostname,
                          "DEF:load=rrds/%s_cpu.rrd:load:MAX" % (hostname),
                          "CDEF:load100=load,100,/",
                          "LINE2:load#0000FF:load",
                          "CDEF:unavailable=load,UN,INF,0,IF",
                          "AREA:unavailable#f0f0f0",
                         )
    return test['image']

@lru_cache(maxsize=128)
def graph2(hostname, period):
    test = rrdtool.graphv("-", "--start", period_conv(period), "-w 800", "--title=Load %s" % hostname,
                          "DEF:cores=rrds/%s_cpu.rrd:cores:LAST" % (hostname),
                          "LINE2:cores#00FFFF:cores",
                          "CDEF:unavailable=cores,UN,INF,0,IF",
                          "AREA:unavailable#f0f0f0",
                         )
    return test['image']

@lru_cache(maxsize=128)
def graph3(hostname, period):
    test = rrdtool.graphv("-", "--start", period_conv(period), "-w 800", "--title=Load %s" % hostname,
                          "DEF:loadavg=rrds/%s_cpu.rrd:loadavg:LAST" % (hostname),
                          "LINE2:loadavg#FF00FF:loadavg",
                          "CDEF:unavailable=loadavg,UN,INF,0,IF",
                          "AREA:unavailable#f0f0f0",
                         )
    return test['image']

def insert(hostname, data, timestamp="N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    rrdtool.update(rrdname, '%s:%s:%s:%s' % (timestamp, data[0], data[1], data[2]))
    graph1.cache_clear()
    graph2.cache_clear()
    graph3.cache_clear()

def exists(hostname):
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_cpu.rrd"
        rrdtool.create(rrdname, '--start', '-2years',
                       '--step', '900',
                       'DS:load:GAUGE:1200:0:5000',
                       'DS:loadavg:GAUGE:1200:0:5000',
                       'DS:cores:GAUGE:1200:0:5000',
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

def last(hostname):
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    try:
        last = rrdtool.last(rrdname)
    except:
        return None
    return last

def latest(hostname):
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    try:
        info = rrdtool.info(rrdname)
        lastupdate = [info['last_update'], float(info['ds[load].last_ds']), float(info['ds[loadavg].last_ds'], float(info['ds[cores].last_ds']))]
        return lastupdate
    except:
        return None

