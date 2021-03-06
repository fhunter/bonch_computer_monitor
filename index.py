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
import usage
import ansiblestats
import scratchstats
from PIL import Image
import StringIO

from bottle import HTTPError
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.types import DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

#Base = declarative_base()
#engine = create_engine('sqlite:///test.db', echo=False)
#
#app = bottle.Bottle()
#plugin = sqlalchemy.Plugin(
#    engine, # SQLAlchemy engine created with create_engine function.
#    Base.metadata, # SQLAlchemy metadata, required only if create=True.
#    keyword='db', # Keyword used to inject session database in a route (default 'db').
#    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
#    commit=True, # If it is true, plugin commit changes after route is executed (default True).
#    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
#)
#
#app.install(plugin)



#@app.get('/',sqlalchemy=dict(use_kwargs=True))
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
		userslog[i[0]]= temp + " " + i[1]
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
		ansible = ansiblestats.getansible(record[2])
		scratch = scratchstats.getscratch(record[2]) # time, full, free
		temptuple = record + (usage.getpowered(30,record[1]),usage.getusage(30,record[1]),ansible,scratch,'NaN')
		temp.append(temptuple)
	    displaydata[i]['values']=temp
	    displaydata[i]['total']=len(result)
	return dict(data=displaydata,date=datetime.datetime.now(),online=onlinecount,userslog=userslog)

@route('/computer1/<machine>')
@view('computer1')
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
	    popularity[j]=usage.getpopularity(j,ip)
	return dict(date=datetime.datetime.now(),machine=result,popularity=popularity,ip= ip,attr=machine,group=False)

@route('/image/<machine>/<date>')
def machinestats_image(machine, date):
	image = Image.new('RGB',(288,3))
	users, uptime = usage.getdetailedusage(date, machine)
	for j in xrange(0,288):
	    if j in uptime:
	        if j in users:
		    pass
		    image.putpixel((j,0),(0,128,0))
		    image.putpixel((j,1),(0,128,0))
	            #<td bgcolor=green>
	        else:
		    image.putpixel((j,0),(0,255,0))
		    image.putpixel((j,1),(0,255,0))
	            #<td bgcolor=lime>
	    else:
	       image.putpixel((j,0),(255,255,255))
	       image.putpixel((j,1),(255,255,255))
	        #<td>

	image_file = StringIO.StringIO()
	image.save(image_file, "PNG")
	return image_file.getvalue()

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
	    popularity[j]=usage.getpopularity(j,ip)
	return dict(date=datetime.datetime.now(),machine=result,popularity=popularity,attr=machine,group=False)


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
	       popularity[i[0]][j]=usage.getpopularity(j,i[1])
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
	failed = request.json['failed']
	ansiblestats.putansible(hostname, ok, change, unreachable, failed)
	return dict()

@route('/api/scratch',method='POST')
def acceptscratchdata():
	ip = request.environ.get("REMOTE_ADDR")
	hostname = request.environ.get("REMOTE_HOST")
	if hostname == None:
	    hostname = socket.gethostbyaddr(ip)[0]
	scratch_free = request.json['scratch_free']
	scratch_total = request.json['scratch_total']
	scratchstats.putscratch(hostname, scratch_total, scratch_free)
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
#app.run(server=bottle.CGIServer)

