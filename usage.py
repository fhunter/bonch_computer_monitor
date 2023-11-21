#!/usr/bin/python
# coding=utf-8
import settings
import datetime
from my_db import db_exec_sql


#def getdetailedusage(day,ip):
#    """ Использование компьютера за определённый период """
#    users_result = db_exec_sql("select time,users from users where (ip = ?) and (date(time) = date(?)) order by time ",(ip, day))
#    """ Время во включенном состоянии компьютера за определённый период  period - в днях"""
#    uptime_result = db_exec_sql("select time,cpuload from load where (ip = ?) and (date(time) = date(?)) order by time ",(ip, day))
#    users = {}
#    uptime = {}
#    for i,j in users_result:
#        time = datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S')
#        hour = time.hour
#        minute = time.minute
#        time = hour*60 + minute
#        time = time/5
#        if time in users:
#            users[time].append(j)
#        else:
#        users[time]=[j,]
#    for i,j in uptime_result:
#        time = datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S')
#        hour = time.hour
#        minute = time.minute
#        time = hour*60 + minute
#        time = time/5
#        uptime[time]=j
#    return users,uptime

def getpopularity(period, ip):
    """ Популярность компьютера и проведённое на нём время
        period - в днях
        возвращает массив из пар время в минутах, пользователь
    """
#    result = db_exec_sql("select users,count()*5 from users where (ip = ? ) and (julianday('now') - julianday(time)) <= ? group by users", (ip, period))
#    return result
# FIXME
    return []

def getusage(period,ip):
    """ Использование компьютера за определённый период """
    #FIXME
#    #result = db_exec_sql("select count() from users where (ip = ?) and (julianday('now') - julianday(time)) <= ? group by time",(ip, period))
#    result = db_exec_sql("select count() from users where (ip = ?) and (julianday('now') - julianday(time)) <= ?",(ip, period))
#    return result[0][0]*5
    return 0

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


def getpowered(period,ip):
    """ Время во включенном состоянии компьютера за определённый период  period - в днях"""
    #FIXME
#    result = db_exec_sql("select count() from uptime where (ip = ?) and (julianday('now') - julianday(time)) <= ?",(ip, period))
#    return result[0][0]*5
    return 0

