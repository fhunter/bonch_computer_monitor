"""Module for manipulating cpu load statistics in RRD database files"""

import os
from functools import lru_cache
import rrdtool
from period import period_conv
from tpl_utils import get_graph_title, getcolor
import rrd


@lru_cache(maxsize=128)
def graph1(hostname, period):
    """Produce graph for cpu load data, over specified period. Period can be d/w/m/y"""
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", f"--title=Load {title} % (сумма по ядрам)")
    j = 1
    length = len(hostname)
    for i in hostname:
        if not exists(i):
            continue
        color = getcolor(j - 1, length)
        new_arglist = (
            f"DEF:load_{j}=rrds/{i}_cpu.rrd:load:MAX",
            f"CDEF:load100_{j}=load_{j},100,/",
            f"LINE2:load_{j}#{color}:load {i}",
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=load_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)
    return test["image"]


@lru_cache(maxsize=128)
def graph2(hostname, period):
    """Produce graph for number of cores, over specified period. Period can be d/w/m/y"""
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", f"--title=Количество ядер процессора: {title}")
    j = 1
    length = len(hostname)
    for i in hostname:
        if not exists(i):
            continue
        color = getcolor(j - 1, length)
        new_arglist = (
            f"DEF:cores_{j}=rrds/{i}_cpu.rrd:cores:LAST",
            f"LINE2:cores_{j}#{color}:cores {i}",
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=cores_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)
    return test["image"]


@lru_cache(maxsize=128)
def graph3(hostname, period):
    """Produce graph for load average, over specified period. Period can be d/w/m/y"""
    title, hostname = get_graph_title(hostname)
    arglist = ("-", "--start", period_conv(period), "-w 800", f"--title=Loadavg {title} - среднее количество процессов ожидающих исполнения")
    j = 1
    length = len(hostname)
    for i in hostname:
        if not exists(i):
            continue
        color = getcolor(j - 1, length)
        new_arglist = (
            f"DEF:loadavg_{j}=rrds/{i}_cpu.rrd:loadavg:LAST",
            f"LINE2:loadavg_{j}#{color}:loadavg {i}",
        )
        arglist = arglist + new_arglist
        j = j + 1
    if len(hostname) == 1:
        arglist = arglist + (
            "CDEF:unavailable=loadavg_1,UN,INF,0,IF",
            "AREA:unavailable#f0f0f0",
        )
    test = rrdtool.graphv(*arglist)

    return test["image"]


def insert(hostname, data, timestamp="N"):
    """Insert data to cpu graph. data = (load, loadavg, cores)"""
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    rrdtool.update(rrdname, f"{timestamp}:{data[0]}:{data[1]}:{data[2]}")
    graph1.cache_clear()
    graph2.cache_clear()
    graph3.cache_clear()


def exists(hostname):
    """Check if rrdfile exists"""
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    """Create rrdfile if not exists"""
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_cpu.rrd"
        rrd.create(rrdname, [["load", 5000], ["loadavg", 5000], ["cores", 5000]])
        return True
    return False


def last(hostname):
    """Get last time when specific rrd file was updated"""
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    last_time = rrd.last(rrdname)
    return last_time


def latest(hostname):
    """Get latest set of data for specific rrd file"""
    rrdname = "rrds/" + hostname + "_cpu.rrd"
    lastupdate = rrd.latest(rrdname, ["load", "loadavg", "cores"])
    if lastupdate:
        lastupdate = [lastupdate[0], *[float(i) for i in lastupdate[1:]]]
    return lastupdate
