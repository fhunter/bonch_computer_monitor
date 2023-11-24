#!/usr/bin/python
# coding=utf-8
import settings
import datetime
from my_db import db_exec_sql, Session
import session_user
import session_pc



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

def getpopularity(period, machineid):
    """ Популярность компьютера и проведённое на нём время
        period - в днях
        возвращает массив из пар время в минутах, пользователь
    """
#    result = db_exec_sql("select users,count()*5 from users where (ip = ? ) and (julianday('now') - julianday(time)) <= ? group by users", (ip, period))
#    return result
# FIXME
    return []

def getusage(period, machineid):
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

def _normalise_time(time, start, end):
    """ Урезать time[0] до start и time[1] до end """
    time_new = [time[0],time[1]]
    if time[0] < start:
        time_new[0] = start
    if time[1] > end:
        time_new[1] = end
    return tuple(time_new)

def getpowered(period, machineid):
    """ Время во включенном состоянии компьютера за определённый период  period - в минутах"""
    session = Session()
    now = datetime.datetime.now()
    startoftoday = datetime.datetime(*now.timetuple()[:3])
    starttime = startoftoday - datetime.timedelta(days = period)
    endoftoday = datetime.datetime(*now.timetuple()[:3], 23, 59, 59)
    computers = session_pc.get_sessions(session,
                                        machineid,
                                        startoftoday - datetime.timedelta(days = period),
                                        endoftoday)
    times = [(i.ComputerSession.session_start, i.session_end_c) for i in computers]
    times = [_normalise_time(i, starttime, endoftoday) for i in times]
    times = [(i[1] - i[0]).total_seconds()/60 for i in times]
    return sum(times)
