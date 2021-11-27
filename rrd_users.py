import rrdtool

def graph(hostname):
    test = rrdtool.graphv("-", "--start", "-1y", "-w 800", "--title=User count %s" % hostname,
        "DEF:users=rrds/%s_users.rrd:users:MAX" % (hostname) ,
        "DEF:usersa=rrds/%s_users.rrd:users:AVERAGE" % (hostname) ,
        "CDEF:users_m=users,UN,0,users,IF",
        "LINE1:users_m#0000FF:Users max",
        "LINE2:usersa#00FFFF:Users average",
#        "CDEF:unavailable=users,UN,INF,0,IF",
#        "AREA:unavailable#f0f0f0",
        )
    return test['image']

def insert(hostname, data): #FIXME - implement
    return ""

def last(hostname): #FIXME - implement
    return -1
