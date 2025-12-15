""" Module for manipulating user count statistics in RRD database files """
import os
from functools import lru_cache
from pathlib import Path
import colorsys
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title
import rrd

def getcolor(num, number):
    """ produce spaced color on color wheel our of number colors """
    t = colorsys.hsv_to_rgb(num/number, 1, 1)
    t = [int(x*256) for x in t]
    t = [f"{{x:02x}}" for x in t]
    return "".join(t)

@lru_cache(maxsize=128)
def graph(hostname, period):
    """ Plot user count graph """
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period),
               "-w 800", "--title=User count %s" % title )
    j = 1
    length = len(hostname)
    for i in hostname:
        rrd_file = Path("rrds/%s_users.rrd" % i)
        if not rrd_file.exists():
            continue
        rrd_file = Path("rrds/%s_uptime.rrd" % i)
        if not rrd_file.exists():
            continue
        if j == 1:
            line = "AREA"
        else:
            line = "STACK"
        color = getcolor(j-1, length)
        new_arglist = (
            "DEF:users_%d=rrds/%s_users.rrd:users:MAX" % (j,i),
            "DEF:usersa_%d=rrds/%s_users.rrd:users:AVERAGE" % (j,i) ,
            "DEF:uptime_%d=rrds/%s_uptime.rrd:uptime:LAST" % (j,i) ,
            "CDEF:users_m_%d=users_%d,UN,0,users_%d,IF" % (j,j,j),
            f"{line}:users_m_{j}#{color}:Users max {i}"
#            "LINE2:usersa_%d#00FFFF:Users average %s" % (j,i),
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
    """ Plot load per user graph """
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period),
               "-w 800", "--title=CPU load per user %s" % title )
    j = 1
    for i in hostname:
        rrd_file = Path("rrds/%s_users.rrd" % i)
        if not rrd_file.exists():
            continue
        rrd_file = Path("rrds/%s_cpu.rrd" % i)
        if not rrd_file.exists():
            continue
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
    """ Insert data to users graph. data = number of users """
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_users.rrd"
    rrdtool.update(rrdname, '%s:%s' % (timestamp, data[0], ))
    graph.cache_clear()
    graph2.cache_clear()

def exists(hostname):
    """ Check if rrdfile exists """
    rrdname = "rrds/" + hostname + "_users.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    """ Create rrdfile if not exists """
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_users.rrd"
        rrd.create(rrdname, [["users", 5000],])
        return True
    return False

def last(hostname):
    """ Get last time when specific rrd file was updated """
    rrdname = "rrds/" + hostname + "_users.rrd"
    last_time = rrd.last(rrdname)
    return last_time

def latest(hostname):
    """ Get latest set of data for specific rrd file """
    rrdname = "rrds/" + hostname + "_users.rrd"
    lastupdate = rrd.latest(rrdname, ["users"])
    return lastupdate
