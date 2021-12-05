import os
import rrdtool

def graph(hostname):
    test = rrdtool.graphv("-", "--start", "-1m", "-w 800", "--title=User count %s" % hostname,
        "DEF:users=rrds/%s_users.rrd:users:MAX" % (hostname) ,
        "DEF:usersa=rrds/%s_users.rrd:users:AVERAGE" % (hostname) ,
        "DEF:uptime=rrds/%s_uptime.rrd:uptime:LAST" % (hostname) ,
        "CDEF:users_m=users,UN,0,users,IF",
        "LINE1:users_m#0000FF:Users max",
        "LINE2:usersa#00FFFF:Users average",
        "CDEF:unavailable=uptime,UN,INF,0,IF",
        "AREA:unavailable#f0f0f0",
        )
    return test['image']

def insert(hostname, data, timestamp="N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_users.rrd"
    rrdtool.update(rrdname, '%s:%s' % (timestamp, data[0], ))

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
    else:
        return False

def last(hostname):
    rrdname = "rrds/" + hostname + "_users.rrd"
    try:
        last = rrdtool.last(rrdname)
    except:
        return None
    return last

def latest(hostname):
    rrdname = "rrds/" + hostname + "_users.rrd"
    try:
        info = rrdtool.info(rrdname)
        lastupdate = [info['last_update'], info['ds[users].last_ds']]
        return lastupdate
    except:
        return None
