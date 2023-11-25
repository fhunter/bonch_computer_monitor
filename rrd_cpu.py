""" Module for manipulating cpu load statistics in RRD database files """
import os
from functools import lru_cache
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title
import rrd


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
        rrd.create(rrdname, [["load", 5000],["loadavg", 5000], ["cores", 5000]])
        return True
    return False

def last(hostname):
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    last_time = rrd.last(rrdname)
    return last_time

def latest(hostname):
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    lastupdate = rrd.latest(rrdname, ["load","loadavg","cores"])
    if lastupdate:
        lastupdate = [lastupdate[0], *[float(i) for i in lastupdate[1:]]]
    return lastupdate
