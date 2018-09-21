#!/usr/bin/python
# coding=utf-8
import settings
import datetime
import json
from my_db import db_exec_sql


def getansible(hostname):
	#CREATE TABLE ansible (id integer primary key autoincrement not null, hostname text, time datetime not null, ok integer not null, change integer not null, unreachable integer not null, failed integer not null);
	result = db_exec_sql("select (julianday('now') - julianday(time)), ok, change, unreachable, failed from ansible where (hostname = ?) ", (hostname,))
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

