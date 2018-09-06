#!/usr/bin/python
# coding=utf-8
import settings
import datetime
import bottle
import socket
import os.path
import json
import glob
import re
from bottle import route, view, request, template, static_file, response, abort, redirect
from my_db import db_exec_sql


@route('/graph.js')
def graphjs():
        isgroup=request.query.getunicode("isgroup",False)
	attribute=request.query.getunicode("attribute","_")
	text = """
if(typeof(jarmon) === 'undefined') {
        var jarmon = {};
}
"""
	text = text + """
jarmon.TAB_RECIPES_STANDARD = [
	['Система',	['cpu','memory','load']],
	['Сеть',	['interface']],
	['Диски',	[]],
	['Нагрузка',	['users','load']],
]

jarmon.CHART_RECIPES_COLLECTD = {
}
"""
	return text

def getpopularity(period, ip):
	""" Популярность компьютера и проведённое на нём время
	    period - в днях
	    возвращает массив из пар время в минутах, пользователь
	"""
	result = db_exec_sql("select users,count()*5 from users where (ip = ? ) and (julianday('now') - julianday(time)) <= ? group by users", (ip, period))
	return result

def getusage(period,ip):
	""" Использование компьютера за определённый период """
	#result = db_exec_sql("select count() from users where (ip = ?) and (julianday('now') - julianday(time)) <= ? group by time",(ip, period))
	result = db_exec_sql("select count() from users where (ip = ?) and (julianday('now') - julianday(time)) <= ?",(ip, period))
	return result[0][0]*5

def getansible(hostname):
	#CREATE TABLE ansible (id integer primary key autoincrement not null, hostname text, time datetime not null, ok integer not null, change integer not null, unreachable integer not null, failed integer not null);
	result = db_exec_sql("select time, ok, change, unreachable, failed from ansible where (hostname = ?) ", (hostname,))
	if len(result)==0:
	    return None
	else:
	    return result[0]

def putansible(hostname,ok,change,unreachable,failed):
	#CREATE TABLE ansible (id integer primary key autoincrement not null, hostname text, time datetime not null, ok integer not null, change integer not null, unreachable integer not null, failed integer not null);
	res = db_exec_sql("select id from ansible where hostname = ?", (hostname,))
	if len(res) == 0:
		t = (hostname, ok, change, unreachable, failed, )
		result = db_exec_sql("insert into ansible ( hostname, ok, change, unreachable, failed, time ) values ( ?, ?, ?, ?, ?, (DATETIME('now')))", t)
	else:
		t = (ok, change, unreachable, failed, hostname)
		result = db_exec_sql("update ansible set ok = ?, change= ?, unreachable = ?, failed = ?, time = (DATETIME('now')) where hostname = ?", t)


def getpowered(period,ip):
	""" Время во включенном состоянии компьютера за определённый период  period - в днях"""
	result = db_exec_sql("select count() from load where (ip = ?) and (julianday('now') - julianday(time)) <= ?",(ip, period))
	return result[0][0]*5

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
	    temp = []
	    for record in result:
		ansible = getansible(record[2])
		temptuple = record + (getpowered(30,record[1]),getusage(30,record[1]),ansible)
		temp.append(temptuple)
	    displaydata[i]['values']=temp
	    displaydata[i]['total']=len(result)
	return dict(data=displaydata,date=datetime.datetime.now(),online=onlinecount,userslog=userslog)

@route('/computer/<machine>')
@view('computer')
def machinestats(machine):
  	result = db_exec_sql("select hostname, ip from machines where hostname like ?", (machine,))
	if len(result) > 0:
	    ip = result[0][1]
	    result = result[0][0]
	else:
	    result = None
	    ip = ""
	popularity={}
	for j in [7,14,30,60,90,180]:
	    popularity[j]=getpopularity(j,ip)
	return dict(date=datetime.datetime.now(),machine=result,popularity=popularity,attr=machine,group=False)

def getrrds(host, target):
	retval = []
	if target == "cpu":
    	    #        ['data/a43908.dcti.sut.ru/df-tmp/df_complex-free.rrd','0','df_complex-free.rrd','unit', ],
	    files = glob.glob("/var/www/rrds/"+host+"/cpu-[0-9]/cpu-*.rrd")
	    for i in files:
		path = re.sub("^/var/www","",i)
	        tempval = [path,"0",path,"%"]
	        retval.append(tempval)
	elif target == "memory":
	    pass
	elif target == "load":
	    pass
	elif target == "users":
	    pass
	elif target == "uptime":
	    pass
	else:
	    pass
	return retval

@route('/group/<grp>')
@view('group')
def machinestats(grp):
	if grp in ['a437','a439','a441','a443','a445','misc']:
	    if grp == 'misc':
	    	 result = db_exec_sql("select hostname,ip from machines where room is NULL order by hostname")
	    else:
	    	 result = db_exec_sql("select hostname,ip from machines where room = ? order by hostname", (grp,))
	tabs=[]
	recipes={}
	popularity={}
	for i in result:
	    popularity[i[0]]={}
	    for j in [7,14,30,60,90,180]:
	       popularity[i[0]][j]=getpopularity(j,i[1])
	for i in result:
	    if os.path.isdir("/var/www/rrds/"+i[0]):
		temp=[]
		temp.append(i[0])
		temp2=[]
		for j in ["cpu", "memory", "load", "users", "uptime"]:
			recipe_name = i[0]+"_"+j
			temp2.append(recipe_name)
			recipes[recipe_name]= { }
			recipes[recipe_name]["title"]=j+" on " + i[0]
			recipes[recipe_name]["data"]=getrrds(i[0],j)
			recipes[recipe_name]["options"]="jQuery.extend(true, {}, jarmon.Chart.BASE_OPTIONS, jarmon.Chart.STACKED_OPTIONS)"
		temp.append(temp2)
		tabs.append(temp)
        tabs=json.dumps(tabs)
        recipes=json.dumps(recipes)
	return dict(date=datetime.datetime.now(),hosts=result,popularity=popularity,tabs=tabs,recipes=recipes,attr=grp,group=True)

@route('/api/ansible',method='POST')
def acceptansibledata():
	ip = request.environ.get("REMOTE_ADDR")
	hostname = request.environ.get("REMOTE_HOST")
	if hostname == None:
	    hostname = socket.gethostbyaddr(ip)[0]
	#CREATE TABLE ansible (id integer primary key autoincrement not null, hostname text, time datetime not null, ok integer not null, change integer not null, unreachable integer not null, failed integer not null);
	ok = request.json['ok']
	change = request.json['change']
	unreachable = request.json['unreachable']
	failed = request.json['unreachable']
	putansible(hostname, ok, change, unreachable, failed)
	return dict()
	

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
	cpu=request.json['cpu']
	db_exec_sql("insert into hostnames (ip, hostname, time) values ( ?, ?, DATETIME('now'))", (ip, reportedhostname))
	db_exec_sql("insert into uptime (ip, time, uptime) values ( ?, DATETIME('now'), ?)", (ip, uptime))
	for i in users:
		db_exec_sql("insert into users (ip, time, users) values ( ?, DATETIME('now'), ?)", (ip, i))
	db_exec_sql("insert into load (ip, time, cpuload, loadavg, cores) values ( ?, DATETIME('now'), ?, ?, ?)", (ip, cpu['load'], cpu['loadavg'],cpu['cores']))
	return dict()

bottle.run(server=bottle.CGIServer)

