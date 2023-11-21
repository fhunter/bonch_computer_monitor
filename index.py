#!/usr/bin/python3
# coding=utf-8
import datetime
import time
import glob
import json
import socket
import os.path
import bottle
from bottle import route, view, request, response, redirect
from my_db import db_exec_sql
from my_db import Session, Room, UserSession, ComputerSession, Computer
import usage

import rrd_uptime
import rrd_cpu
import rrd_users
import rrd_ansible
import rrd_scratch

import session_pc
import computer
import settings

bottle.debug(True)
app = application = bottle.Bottle()

@app.route(settings.PREFIX + '/')
@view('mainpage')
def main():
    session = Session()
    onlinecount = session.query(ComputerSession).filter(ComputerSession.session_end==None).count()
    usersloggedin = session.query(UserSession).filter(UserSession.session_end==None).all()
    rooms = session.query(Room).all()
    userslog = dict()
#    for i in usersloggedin:
#        if i[0] in userslog:
#            temp = userslog[i[0]]
#            userslog[i[0]] = temp + " " + i[1]
#        else:
#            userslog[i[0]] = i[1]
#    onlinecount = online[0][0]
    displaydata = {}
    timenow = datetime.datetime.now()
    for i in rooms:
        displaydata[i] = {}
        displaydata[i]['name'] = i.name
        displaydata[i]['link'] = i.name
        displaydata[i]['online'] = 0
#        room = (i, )
#        if i == 'misc':
#            displaydata[i]['name'] = u"Прочее"
#            result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines where room is NULL order by hostname")
#        else:
#            result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines where room = ? order by hostname", room)
        temp = []
        result = session.query(Computer).filter(Computer.room == i.id).all()
# 1 - ip, 2 - hostname, 3 - lastupdate, 4 - time since update, 5 - room
        for record in result:
            hostname = record.hostname
            if not hostname.endswith('.dcti.sut.ru'):
                hostname = hostname + '.dcti.sut.ru'
            ansible = rrd_ansible.latest(hostname)
            scratch = rrd_scratch.latest(hostname)
            time_since_update = (timenow - record.last_report).total_seconds()/60 # in minutes
            temptuple = (record.id, record.ip, hostname, record.last_report, time_since_update)
            temptuple = temptuple + (usage.getpowered(30, record.ip), usage.getusage(30, record.ip), ansible, scratch, 'NaN')
            temp.append(temptuple)
        displaydata[i]['values'] = temp
        displaydata[i]['total'] = len(result)
    return dict(data=displaydata, date=datetime.datetime.now(), online=onlinecount, userslog=userslog)

#@app.route(settings.PREFIX +'/computer2/<machine>/<period:re:[d,w,m,y]>')
#@app.route(settings.PREFIX +'/computer2/<machine>')
#@view('computer2')
#def machinestats3(machine,period = 'w'):
#    sessions_pc=session_pc.get_sessions(machine, time.time()-30*24*60*60, None)
#    sessions_user=[]
#    sessions_user_open=[]
#    return dict(date=datetime.datetime.now(), machine=machine, sessions_pc=sessions_pc, sessions_user=sessions_user, sessions_open=sessions_user_open, group=False, period=period)

@app.route(settings.PREFIX + '/debug/')
@view('debug')
def debugfunc():
    session = Session()
    usersloggedin = session.query(UserSession).all()
    rooms = session.query(Room).all()
    computers = session.query(ComputerSession).all()
    computer_list = session.query(Computer).all()
    graphs = glob.glob('rrds/*_ansible.rrd')
    graphs = [i.replace('rrds/','').replace('_ansible.rrd','') for i in graphs]
    return dict(users=usersloggedin, rooms= rooms, computers=computers, computer = computer_list, graphs=graphs)

@app.route(settings.PREFIX +'/computer/<machine>/<period:re:[d,w,m,y]>')
@app.route(settings.PREFIX +'/computer/<machine>')
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


@app.route(settings.PREFIX +'/group/<grp>')
@view('group')
def machinestats(grp):
    session = Session()
    room  = session.query(Room).filter(Room.name == grp).first()
    result = []
    if not room:
        redirect(settings.PREFIX + "/")
#            result = db_exec_sql("select hostname,ip from machines where room = ? order by hostname", (grp,))
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
    return dict(date=datetime.datetime.now(), hosts=result, popularity=popularity, tabs=tabs2, recipes=recipes2, attr=room.name, group=True)

@app.route(settings.PREFIX +'/graph/<hostname>_<typ>')
@app.route(settings.PREFIX +'/graph/<hostname>_<typ>/<period:re:[d,w,m,y]>')
def graphs_func(hostname, typ, period = 'w'):
    result = "Error"
    age = 1000 # 16 minutes
    if   typ == "uptime":
        result = rrd_uptime.graph(hostname, period)
    elif typ == "cpu1":
        result = rrd_cpu.graph1(hostname, period)
    elif typ == "cpu2":
        result = rrd_cpu.graph2(hostname, period)
    elif typ == "cpu3":
        result = rrd_cpu.graph3(hostname, period)
    elif typ == "users":
        result = rrd_users.graph(hostname, period)
        age = 200 # 3 minutes
    elif typ == "lpu":
        result = rrd_users.graph2(hostname, period)
        age = 200 # 3 minutes
    elif typ == "scratch":
        result = rrd_scratch.graph(hostname, period)
    elif typ == "ansible":
        result = rrd_ansible.graph(hostname, period)
    response.set_header('Content-type', 'image/png')
    response.set_header('Cache-control', 'max-age=%s,public' % age)
    return result

@app.route(settings.PREFIX +'/api/ansible', method='POST')
def acceptansibledata():
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
    try:
        ok_value = request.json['ok']
        change_value = request.json['change']
        unreachable_value = request.json['unreachable']
        failed_value = request.json['failed']
        rrd_ansible.insert(hostname, [ok_value, change_value, unreachable_value, failed_value])
    except:
        pass
    return dict()

@app.route(settings.PREFIX +'/api/scratch', method='POST')
def acceptscratchdata():
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
    scratch_free = request.json['scratch_free']
    scratch_total = request.json['scratch_total']
    rrd_scratch.insert(hostname, [scratch_free, scratch_total])
    return dict()


@app.route(settings.PREFIX +'/api/data', method='POST')
def acceptdata():
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
#    temp = (ip_addr, )
    reportedhostname = request.json['hostname']
    machineid = request.json['machineid']
    uptime = request.json['uptime']
    users = request.json['users']
    cpu = request.json['cpu']
    rrd_uptime.insert(hostname, [uptime, ])
    rrd_cpu.insert(hostname, [cpu['load'], cpu['loadavg'], cpu['cores']])
    rrd_users.insert(hostname, [len(set(users)),])
    session = Session()
    computer.add_or_update(session, machineid, ip_addr, reportedhostname)
    return dict()
#    res = db_exec_sql("select id from machines where ip = ?", temp)
#    if len(res) == 0:
#        temp = (ip_addr, hostname, )
#        db_exec_sql("insert into machines ( ip, hostname, lastupdate ) values ( ?, ?, (DATETIME('now')))", temp)
#    else:
#        temp = (hostname, ip_addr, )
#        db_exec_sql("update machines set hostname = ?, lastupdate = (DATETIME('now')) where ip = ?", temp)
#    # here goes the report
#    db_exec_sql("insert into hostnames (ip, hostname, time) values ( ?, ?, DATETIME('now'))", (ip_addr, reportedhostname))
#    db_exec_sql("insert into uptime (ip, time, uptime) values ( ?, DATETIME('now'), ?)", (ip_addr, uptime))
#    for i in users:
#        db_exec_sql("insert into users (ip, time, users) values ( ?, DATETIME('now'), ?)", (ip_addr, i))
#    return dict()

if __name__ == '__main__':
    bottle.run(app,
        host='127.0.0.1',
        port=8086,
        reloader=True)
