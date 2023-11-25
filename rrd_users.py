""" Module for manipulating user count statistics in RRD database files """
import os
from functools import lru_cache
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title
import rrd


@lru_cache(maxsize=128)
def graph(hostname, period):
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period),
               "-w 800", "--title=User count %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:users_%d=rrds/%s_users.rrd:users:MAX" % (j,i),
            "DEF:usersa_%d=rrds/%s_users.rrd:users:AVERAGE" % (j,i) ,
            "DEF:uptime_%d=rrds/%s_uptime.rrd:uptime:LAST" % (j,i) ,
            "CDEF:users_m_%d=users_%d,UN,0,users_%d,IF" % (j,j,j),
            "LINE2:users_m_%d#0000FF:Users max %s" % (j,i),
            "LINE2:usersa_%d#00FFFF:Users average %s" % (j,i),
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

@lru_cache(maxsize=128)
def graph2(hostname, period):
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period),
               "-w 800", "--title=CPU load per user %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:users_%d=rrds/%s_users.rrd:users:MAX" % (j, i) ,
            "DEF:usersa_%d=rrds/%s_users.rrd:users:AVERAGE" % (j, i) ,
            "DEF:load_%d=rrds/%s_cpu.rrd:load:MAX" % (j, i),
            "CDEF:users_m_%d=users_%d,UN,0,users_%d,IF" % (j,j,j),
            "CDEF:loadperuser1_%d=load_%d,users_m_%d,/" % (j,j,j),
            "CDEF:loadperuser_%d=users_m_%d,1,GE,loadperuser1_%d,0,IF" % (j,j,j),
            "LINE2:loadperuser_%d#00FFFF:CPU load per user %s" % (j,i),
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=users_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)
    return test['image']

def insert(hostname, data, timestamp="N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_users.rrd"
    rrdtool.update(rrdname, '%s:%s' % (timestamp, data[0], ))
    graph.cache_clear()
    graph2.cache_clear()

def exists(hostname):
    rrdname = "rrds/" + hostname + "_users.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_users.rrd"
        rrdtool.create(rrdname, '--start', '-2years',
                       '--step', '900',
                       'DS:users:GAUGE:1200:0:5000',
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
    rrdname = "rrds/" + hostname + "_users.rrd"
    last_time = rrd.last(rrdname)
    return last_time

def latest(hostname):
    rrdname = "rrds/" + hostname + "_users.rrd"
    lastupdate = rrd.latest(rrdname, ["users"])
    return lastupdate
