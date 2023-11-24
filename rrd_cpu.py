""" Module for manipulating cpu load statistics in RRD database files """
import os
from functools import lru_cache
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title


@lru_cache(maxsize=128)
def graph1(hostname, period):
    """ Produce graph for cpu load data, over specified period. Period can be d/w/m/y """
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", "--title=Load %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:load_%d=rrds/%s_cpu.rrd:load:MAX" % (j,i),
            "CDEF:load100_%d=load_%d,100,/" % (j,j),
            "LINE2:load_%d#0000FF:load %s" % (j, i),
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=load_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)
    return test['image']

@lru_cache(maxsize=128)
def graph2(hostname, period):
    """ Produce graph for number of cores, over specified period. Period can be d/w/m/y """
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", "--title=Load %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:cores_%d=rrds/%s_cpu.rrd:cores:LAST" % (j,i),
            "LINE2:cores_%d#00FFFF:cores %s" % (j,i),
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=cores_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)
    return test['image']

@lru_cache(maxsize=128)
def graph3(hostname, period):
    """ Produce graph for load average, over specified period. Period can be d/w/m/y """
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", "--title=Load %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:loadavg_%d=rrds/%s_cpu.rrd:loadavg:LAST" % (j,i),
            "LINE2:loadavg_%d#FF00FF:loadavg %s" % (j,i),
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=loadavg_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)

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
    return False

def last(hostname):
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    try:
        last_time = rrdtool.last(rrdname)
    except:
        return None
    return last_time

def latest(hostname):
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    try:
        info = rrdtool.info(rrdname)
        lastupdate = [info['last_update'],
                      float(info['ds[load].last_ds']),
                      float(info['ds[loadavg].last_ds'],
                      float(info['ds[cores].last_ds']))]
        return lastupdate
    except:
        return None
