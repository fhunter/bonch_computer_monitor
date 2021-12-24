import os
import rrdtool


def graph(hostname, period):
    test = rrdtool.graphv("-", "--start", "-1m", "-w 800", "--title=Uptime %s" % hostname,
        "DEF:uptime=rrds/%s_uptime.rrd:uptime:LAST" % (hostname) ,
        "LINE1:uptime#0000FF:Uptime",
        "CDEF:unavailable=uptime,UN,INF,0,IF",
        "AREA:unavailable#f0f0f0",
        )
    return test['image']

def insert(hostname, data, timestamp="N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_uptime.rrd"
    rrdtool.update(rrdname, '%s:%s' % (timestamp, data[0]))

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
    else:
        return False


def last(hostname):
    rrdname = "rrds/" + hostname + "_uptime.rrd"
    try:
        last = rrdtool.last(rrdname)
    except:
        return None
    return last

def latest(hostname):
    rrdname = "rrds/" + hostname + "_uptime.rrd"
    try:
        info = rrdtool.info(rrdname)
        lastupdate = [info['last_update'], info['ds[uptime].last_ds']]
        return lastupdate
    except:
        return None
