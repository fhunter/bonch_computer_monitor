import rrdtool
import os


def graph(hostname):
    test = rrdtool.graphv("-", "--start", "-1d", "-w 800", "--title=Ansible %s" % hostname,
        "DEF:ok=rrds/%s_ansible.rrd:ok:LAST" % (hostname) ,
        "DEF:change=rrds/%s_ansible.rrd:change:LAST" % (hostname) ,
        "DEF:unreachable=rrds/%s_ansible.rrd:unreachable:LAST" % (hostname) ,
        "DEF:failed=rrds/%s_ansible.rrd:failed:LAST" % (hostname) ,
        "LINE1:ok#00FF00:ok",
        "LINE2:change#FFFF00:change",
        "LINE3:unreachable#0000FF:unreachable",
        "LINE4:failed#FF0000:failed",
        "CDEF:unavailable=ok,UN,INF,0,IF",
        "AREA:unavailable#f0f0f0",
        )
    return test['image']

def insert(hostname, data, timestamp = "N"):
    if not exists(hostname):
        create(hostname)
    rrdname = "rrds/" + hostname + "_ansible.rrd"
    rrdtool.update(rrdname, '%s:%s:%s:%s:%s' % (timestamp,data[0],data[1],data[2],data[3]))

def exists(hostname):
    rrdname = "rrds/" + hostname + "_ansible.rrd"
    return os.path.exists(rrdname)


def create(hostname):
    if not exists(hostname):
        rrdname = "rrds/" + hostname + "_ansible.rrd"
        rrdtool.create(rrdname, '--start', '-2years',
                       '--step', '900',
                       'DS:ok:GAUGE:1200:0:500',
                       'DS:change:GAUGE:1200:0:500',
                       'DS:unreachable:GAUGE:1200:0:500',
                       'DS:failed:GAUGE:1200:0:500',
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

def last(hostname): #FIXME - implement
    return -1
