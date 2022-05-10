#!/usr/bin/python
# coding=utf-8
import datetime
import time
import json
import socket
import os.path
import bottle
from bottle import route, view, request, response
from my_db import db_exec_sql
import usage

import rrd_uptime
import rrd_cpu
import rrd_users
import rrd_ansible
import rrd_scratch

import session_pc


@route('/')
@view('mainpage')
def main():
        #result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines order by hostname")
    online = db_exec_sql("select count() from machines where (julianday('now')-julianday(lastupdate))*24*60 < 10")
    usersloggedin = db_exec_sql("select ip, users from users where (julianday('now')-julianday(time))*24*60 < 10 group by ip,users")
    userslog = dict()
    for i in usersloggedin:
        if i[0] in userslog:
            temp = userslog[i[0]]
            userslog[i[0]] = temp + " " + i[1]
        else:
            userslog[i[0]] = i[1]
    onlinecount = online[0][0]
    displaydata = {}
    for i in ['a425', 'a437', 'a439', 'a441', 'a443', 'a445', 'p4n', 'misc']:
        displaydata[i] = {}
        displaydata[i]['name'] = u"Аудитория "+i
        displaydata[i]['link'] = i
        displaydata[i]['online'] = 0
        room = (i, )
        if i == 'misc':
            displaydata[i]['name'] = u"Прочее"
            result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines where room is NULL order by hostname")
        else:
            result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines where room = ? order by hostname", room)
        temp = []
        for record in result:
            ansible = rrd_ansible.latest(str(record[2]))
            scratch = rrd_scratch.latest(str(record[2]))
            temptuple = record + (usage.getpowered(30, record[1]), usage.getusage(30, record[1]), ansible, scratch, 'NaN')
            temp.append(temptuple)
        displaydata[i]['values'] = temp
        displaydata[i]['total'] = len(result)
    return dict(data=displaydata, date=datetime.datetime.now(), online=onlinecount, userslog=userslog)

#@route('/computer2/<machine>/<period:re:[d,w,m,y]>')
#@route('/computer2/<machine>')
#@view('computer2')
#def machinestats3(machine,period = 'w'):
#    sessions_pc=session_pc.get_sessions(machine, time.time()-30*24*60*60, None)
#    sessions_user=[]
#    sessions_user_open=[]
#    return dict(date=datetime.datetime.now(), machine=machine, sessions_pc=sessions_pc, sessions_user=sessions_user, sessions_open=sessions_user_open, group=False, period=period)

@route('/computer/<machine>/<period:re:[d,w,m,y]>')
@route('/computer/<machine>')
@view('computer')
def machinestats2(machine,period = 'w'):
    result = db_exec_sql("select hostname, ip from machines where hostname like ?", (machine,))
    if len(result) > 0:
        ip_addr = result[0][1]
        result = result[0][0]
    else:
        result = None
        ip_addr = ""
    popularity = {}
    for j in [7, 14, 30, 60, 90, 180]:
        popularity[j] = usage.getpopularity(j, ip_addr)
    return dict(date=datetime.datetime.now(), machine=result, popularity=popularity, attr=machine, group=False, period=period)


@route('/group/<grp>')
@view('group')
def machinestats(grp):
    if grp in ['a425', 'a437', 'a439', 'a441', 'a443', 'a445', 'p4n', 'misc']:
        if grp == 'misc':
            result = db_exec_sql("select hostname,ip from machines where room is NULL order by hostname")
        else:
            result = db_exec_sql("select hostname,ip from machines where room = ? order by hostname", (grp,))
    tabs = []
    recipes = {}
    popularity = {}
    for i in result:
        popularity[i[0]] = {}
        for j in [7, 14, 30, 60, 90, 180]:
            popularity[i[0]][j] = usage.getpopularity(j, i[1])
    for i in result:
        if os.path.isdir("/var/www/rrds/"+i[0]):
            temp = []
            temp.append(i[0])
            temp2 = []
            for j in ["cpu", "memory", "load", "users", "uptime"]:
                recipe_name = i[0]+"_"+j
                temp2.append(recipe_name)
                recipes[recipe_name] = {}
                recipes[recipe_name]["title"] = j + " on " + i[0]
            temp.append(temp2)
            tabs.append(temp)
    tabs2 = json.dumps(tabs)
    recipes2 = json.dumps(recipes)
    return dict(date=datetime.datetime.now(), hosts=result, popularity=popularity, tabs=tabs2, recipes=recipes2, attr=grp, group=True)

@route('/graph/<hostname>_<typ>')
@route('/graph/<hostname>_<typ>/<period:re:[d,w,m,y]>')
def graphs(hostname, typ, period = 'w'):
    result = "Error"
    if   typ == "uptime":
        result = rrd_uptime.graph(hostname, period)
    elif typ == "cpu":
        result = rrd_cpu.graph(hostname, period)
    elif typ == "users":
        result = rrd_users.graph(hostname, period)
    elif typ == "scratch":
        result = rrd_scratch.graph(hostname, period)
    elif typ == "ansible":
        result = rrd_ansible.graph(hostname, period)
    response.set_header('Content-type', 'image/png')
    return str(result)

@route('/api/ansible', method='POST')
def acceptansibledata():
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
    #CREATE TABLE ansible (id integer primary key autoincrement not null, hostname text, time datetime not null, ok integer not null, change integer not null, unreachable integer not null, failed integer not null);
    ok_value = request.json['ok']
    change_value = request.json['change']
    unreachable_value = request.json['unreachable']
    failed_value = request.json['failed']
    rrd_ansible.insert(hostname, [ok_value, change_value, unreachable_value, failed_value])
    return dict()

@route('/api/scratch', method='POST')
def acceptscratchdata():
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
    scratch_free = request.json['scratch_free']
    scratch_total = request.json['scratch_total']
    rrd_scratch.insert(hostname, [scratch_free, scratch_total])
    return dict()


@route('/api/data', method='POST')
def acceptdata():
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
    temp = (ip_addr, )
    res = db_exec_sql("select id from machines where ip = ?", temp)
    if len(res) == 0:
        temp = (ip_addr, hostname, )
        db_exec_sql("insert into machines ( ip, hostname, lastupdate ) values ( ?, ?, (DATETIME('now')))", temp)
    else:
        temp = (hostname, ip_addr, )
        db_exec_sql("update machines set hostname = ?, lastupdate = (DATETIME('now')) where ip = ?", temp)
    # here goes the report
    reportedhostname = request.json['hostname']
    uptime = request.json['uptime']
    users = request.json['users']
    cpu = request.json['cpu']
    db_exec_sql("insert into hostnames (ip, hostname, time) values ( ?, ?, DATETIME('now'))", (ip_addr, reportedhostname))
    db_exec_sql("insert into uptime (ip, time, uptime) values ( ?, DATETIME('now'), ?)", (ip_addr, uptime))
    rrd_uptime.insert(hostname, [uptime, ])
    rrd_cpu.insert(hostname, [cpu['load'], cpu['loadavg'], cpu['cores']])
    rrd_users.insert(hostname, [len(set(users)),])
    for i in users:
        db_exec_sql("insert into users (ip, time, users) values ( ?, DATETIME('now'), ?)", (ip_addr, i))
    return dict()

bottle.run(server=bottle.CGIServer)
