#!/usr/bin/python
# coding=utf-8
import datetime
import bottle
import socket
from bottle import route, view, request, template, static_file, response, abort, redirect
from my_db import db_exec_sql


@route('/')
@view('mainpage')
def main():
	#result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines order by hostname")
	online = db_exec_sql("select count() from machines where (julianday('now')-julianday(lastupdate))*24*60 < 10")
	usersloggedin = db_exec_sql("select ip, users from users where (julianday('now')-julianday(time))*24*60 < 10 group by ip,users")
	userslog = dict()
	for i in usersloggedin:
	    if i[0] in userslog:
		temp=userslog[i[0]]
		userslog[i[0]]= temp + "," + i[1]
	    else:
		userslog[i[0]]= i[1]
	onlinecount=online[0][0]
	displaydata={}
	for i in ['a437','a439','a441','a443','a445','misc']:
	    displaydata[i]={}
	    displaydata[i]['name']=u"Аудитория "+i
	    displaydata[i]['link']=i
	    displaydata[i]['online']=0
	    room=(i, )
	    if i=='misc':
		 displaydata[i]['name']=u"Прочее"
	    	 result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines where room is NULL order by hostname")
	    else:
	    	 result = db_exec_sql("select id, ip, hostname, lastupdate, (julianday('now')-julianday(lastupdate))*24*60 from machines where room = ? order by hostname", room)
            displaydata[i]['values']=result
	    displaydata[i]['total']=len(result)
	return dict(data=displaydata,date=datetime.datetime.now(),online=onlinecount,userslog=userslog)

@route('/computer/<machine>')
@view('computer')
def machinestats(machine):
  	result = db_exec_sql("select hostname from machines where hostname like ?", (machine,))
	if len(result) > 0:
	    result = result[0]
	else:
	    result = None
	return dict(date=datetime.datetime.now(),machine=result)

@route('/group/<grp>')
@view('group')
def machinestats(grp):
	if grp in ['a437','a439','a441','a443','a445','misc']:
	    if grp == 'misc':
	    	 result = db_exec_sql("select hostname from machines where room is NULL order by hostname")
	    else:
	    	 result = db_exec_sql("select hostname from machines where room = ? order by hostname", (grp,))
	    if len(result) > 0:
	         result = result[0]
            else:
	         result = None
	return dict(date=datetime.datetime.now(),hosts=result)

@route('/api/data',method='POST')
def acceptdata():
	ip = request.environ.get("REMOTE_ADDR")
	hostname = request.environ.get("REMOTE_HOST")
	if hostname == None:
	    hostname = socket.gethostbyaddr(ip)[0]
	t = (ip, )
	res = db_exec_sql("select id from machines where ip = ?", t)
	if len(res) == 0:
		t = (ip, hostname, )
		result = db_exec_sql("insert into machines ( ip, hostname, lastupdate ) values ( ?, ?, (DATETIME('now')))", t)
	else:
		t = (hostname, ip, )
		result = db_exec_sql("update machines set hostname = ?, lastupdate = (DATETIME('now')) where ip = ?", t)
	# here goes the report
	reportedhostname=request.json['hostname']
	uptime=request.json['uptime']
	users=request.json['users']
	netspeed=request.json['netspeed']
	cpu=request.json['cpu']
	disks=request.json['disks']
	db_exec_sql("insert into hostnames (ip, hostname, time) values ( ?, ?, DATETIME('now'))", (ip, reportedhostname))
	db_exec_sql("insert into uptime (ip, time, uptime) values ( ?, DATETIME('now'), ?)", (ip, uptime))
	for i in users:
		db_exec_sql("insert into users (ip, time, users) values ( ?, DATETIME('now'), ?)", (ip, i))
	db_exec_sql("insert into network (ip, time, netspeed) values ( ?, DATETIME('now'), ?)", (ip, netspeed))
	db_exec_sql("insert into load (ip, time, cpuload, loadavg, cores) values ( ?, DATETIME('now'), ?, ?, ?)", (ip, cpu['load'], cpu['loadavg'],cpu['cores']))
	for i in disks:
		db_exec_sql("insert into diskspace (ip, time, volume, free, total) values ( ?, DATETIME('now'), ?, ?, ?)", (ip, i['volume'], i['free'], i['total']))
	return dict()

@route('/jarmon/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./jarmon/')
@route('/assets/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./assets/')
@route('/data/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./data/')

bottle.run(server=bottle.CGIServer)

