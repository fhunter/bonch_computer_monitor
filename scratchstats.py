#!/usr/bin/python
# coding=utf-8
import settings
import datetime
import json
from my_db import db_exec_sql


def getscratch(hostname):
        #CREATE TABLE scratch (id integer primary key autoincrement not null, hostname text unique not null, time datetime not null, total real not null, free real not null);
	result = db_exec_sql("select (julianday('now') - julianday(time)), total, free from scratch where (hostname = ?) ", (hostname,))
	if len(result)==0:
	    return None
	else:
	    return result[0]

def putscratch(hostname,total, free):
        #CREATE TABLE scratch (id integer primary key autoincrement not null, hostname text unique not null, time datetime not null, total real not null, free real not null);
	res = db_exec_sql("select id from scratch where hostname = ?", (hostname,))
	if len(res) == 0:
		t = (hostname, total, free, )
		result = db_exec_sql("insert into scratch ( hostname, total, free, time ) values ( ?, ?, ?, (DATETIME('now')))", t)
	else:
		t = (total, free, hostname)
		result = db_exec_sql("update scratch set total = ?, free= ?, time = (DATETIME('now')) where hostname = ?", t)

