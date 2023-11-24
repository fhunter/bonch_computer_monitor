""" Module for manipulating uptime statistics in RRD database files """
import os
from functools import lru_cache
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title


@lru_cache(maxsize=128)
def graph(hostname, period):
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", "--title=Uptime %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:uptime_%d=rrds/%s_uptime.rrd:uptime:LAST" % (j,i),
            "LINE1:uptime_%d#0000FF:Uptime %s" % (j, i),
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=uptime_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)

    return test['image']

def insert(hostname, data, timestamp="N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_uptime.rrd"
    rrdtool.update(rrdname, '%s:%s' % (timestamp, data[0]))
    graph.cache_clear()

def exists(hostname):
    rrdname = "rrds/" + hostname + "_uptime.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_uptime.rrd"
        rrdtool.create(rrdname, '--start', '-2years',
                       '--step', '900',
                       'DS:uptime:GAUGE:1200:0:315360000',
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
    rrdname = "rrds/" + hostname + "_uptime.rrd"
    try:
        last_time = rrdtool.last(rrdname)
    except:
        return None
    return last_time

def latest(hostname):
    rrdname = "rrds/" + hostname + "_uptime.rrd"
    try:
        info = rrdtool.info(rrdname)
        lastupdate = [info['last_update'], info['ds[uptime].last_ds']]
        return lastupdate
    except:
        return None
