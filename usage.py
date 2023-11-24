#!/usr/bin/python
# coding=utf-8
""" Функции учёта популярности компьютера (время и пользователи) """
import datetime
from my_db import Session
import session_user
import session_pc



def getpopularity(period, machineid):
    """ Популярность компьютера и проведённое на нём время
        period - в днях
        возвращает массив из пар время в минутах, пользователь
    """
    # FIXME
    return []

def getusage(period, machineid):
    """ Использование компьютера за определённый период (в минутах) """
    #FIXME
    return 0

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
    times = [int((i[1] - i[0]).total_seconds()/60) for i in times]
    return sum(times)
