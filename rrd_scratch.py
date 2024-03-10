""" Module for manipulating free and used space statistics on /scratch in RRD database files """
import os
from functools import lru_cache
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title
import rrd


@lru_cache(maxsize=128)
def graph(hostname, period):
    """ Plot graph of free and total values for scratch """
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", "--title=/scratch %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:free_%d=rrds/%s_scratch.rrd:free:LAST" % (j, i) ,
            "DEF:total_%d=rrds/%s_scratch.rrd:total:LAST" % (j,i) ,
            "LINE2:total_%d#009F00:Total %s" % (j, i),
            "LINE2:free_%d#FF00FF:Free %s" % (j, i),
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=total_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)
    return test['image']

def insert(hostname, data, timestamp = "N"):
    """ Insert data to scratch graph. data = (free, total) """
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    rrdtool.update(rrdname, '%s:%s:%s' % (timestamp,data[0],data[1]))
    graph.cache_clear()

def exists(hostname):
    """ Check if rrdfile exists """
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    """ Create rrdfile if not exists """
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_scratch.rrd"
        rrd.create(rrdname, [["free", 10995116277760],["total", 10995116277760]])
        return True
    return False

def last(hostname):
    """ Get last time when specific rrd file was updated """
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    last_time = rrd.last(rrdname)
    return last_time

def latest(hostname):
    """ Get latest set of data for specific rrd file """
    rrdname = "rrds/" + hostname + "_scratch.rrd"
    lastupdate = rrd.latest(rrdname, ["total","free"])
    if lastupdate:
        lastupdate = [lastupdate[0], *[int(i) for i in lastupdate[1:]]]
    return lastupdate
