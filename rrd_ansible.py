""" Module for manipulating ansible statistics in RRD database files """

import os
from functools import lru_cache
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title
import rrd


@lru_cache(maxsize=128)
def graph(hostname, period):
    """ Produce graph for ansible data, over specified period. Period can be d/w/m/y """
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", "--title=Ansible %s" % title )
    j = 1
    for i in hostname:
        new_arglist = (
            "DEF:ok_%d=rrds/%s_ansible.rrd:ok:LAST" % (j,i),
            "DEF:change_%d=rrds/%s_ansible.rrd:change:LAST" % (j,i),
            "DEF:unreachable_%d=rrds/%s_ansible.rrd:unreachable:LAST" % (j,i),
            "DEF:failed_%d=rrds/%s_ansible.rrd:failed:LAST" % (j,i),
            "LINE2:ok_%d#00FF00:ok %s" % (j,i),
            "LINE2:change_%d#FFFF00:change %s" % (j,i),
            "LINE3:unreachable_%d#0000FF:unreachable %s" % (j,i),
            "LINE4:failed_%d#FF0000:failed %s" %(j,i),
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=ok_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)
    return test['image']

def insert(hostname, data, timestamp="N"):
    """ Insert data into RRD database file for ansible statistics """
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_ansible.rrd"
    rrdtool.update(rrdname, '%s:%s:%s:%s:%s' % (timestamp, data[0], data[1], data[2], data[3]))
    graph.cache_clear()

def exists(hostname):
    """ Vefiry if RRD database for specified hostname exists """
    rrdname = "rrds/" + hostname + "_ansible.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    """ Create RRD database for specified hostname """
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_ansible.rrd"
        rrd.create(rrdname, [["ok", 500],["change", 500], ["unreachable", 500], ["failed", 500]])
        return True
    return False

def last(hostname):
    """ Get last timestamp for ansible statistics for the hostname """
    rrdname = "rrds/" + hostname + "_ansible.rrd"
    last_time = rrd.last(rrdname)
    return last_time

def latest(hostname):
    """ Get last data for ansible statistics for the hostname """
    rrdname = "rrds/" + hostname + "_ansible.rrd"
    lastupdate = rrd.latest(rrdname, ["ok","change","unreachable","failed"])
    return lastupdate
