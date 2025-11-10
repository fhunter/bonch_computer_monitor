#!/usr/bin/python3
# coding=utf-8
""" Computer user and ansible monitoring web-app """
import datetime
import glob
import socket
import bottle
import requests
from bottle import view, request, response, redirect, static_file
from my_db import Session, Room, UserSession, ComputerSession, Computer
from sqlalchemy import desc, func, or_
import usage

import rrd_uptime
import rrd_cpu
import rrd_users
import rrd_ansible
import rrd_scratch

import session_pc
import session_user
import computer
import settings
from tpl_utils import period_to_days, expand_hostname
from utils import require_groups

bottle.debug(True)
app = application = bottle.Bottle()

@app.error(403)
def error403(error_m):
    e_message = "<html><head>"
    e_message += f"<meta http-equiv=\"refresh\" content=\"5; url='{settings.PREFIX}/'\" />"
    e_message += "</head><body><h1>Unauthorised, sorry</h1></body></html>"
    return e_message

@app.route(settings.PREFIX + '/')
@view('mainpage')
def main():
    """ Generate main page data """
    session = Session()
    session_pc.clean_sessions(session)
    session_user.clean_sessions(session)
    onlinecount = (session.query(ComputerSession)
                  .filter(ComputerSession.session_end.is_(None))
                  .count())
    rooms = session.query(Room).order_by(Room.name).all()
    userslog = dict()
    displaydata = {}
    timenow = datetime.datetime.now()

    # fetch data from gitea
    date = None
    try:
        data = requests.get("https://gitea.pivt.spbgut.ru/api/v1/repos/PIVT/bonch_ansible/branches/master", headers = {"accept": "application/json"}, timeout = 1)
        data = data.json()
        date = data["commit"]["timestamp"]
        date = datetime.datetime.fromisoformat(date)
    except:
        pass
    for i in rooms:
        displaydata[i] = {}
        displaydata[i]['name'] = i.name
        displaydata[i]['link'] = i.name
        displaydata[i]['online'] = 0
        temp = []
        result = (session.query(Computer)
                 .filter(Computer.room == i.id)
                 .group_by(Computer.hostname)
                 .having(func.max(Computer.first_report))
                 .order_by(Computer.hostname)
                 .all())
        for record in result:
            userslog[record.machineid] = session_user.get_active_users(session, record.machineid)
            hostname = expand_hostname(record.hostname)
            ansible = rrd_ansible.latest(hostname)
            scratch = rrd_scratch.latest(hostname)
            time_since_update = (timenow - record.last_report).total_seconds()/60 # in minutes
            computerdata = {
                "id": record.id,
                "ip": record.ip,
                "hostname": hostname,
                # Limit to seconds
                "last_report": datetime.datetime(*record.last_report.timetuple()[:6]),
                "since_update": time_since_update,
                "power_time": usage.getpowered(30, record.machineid),
                "usage_time": usage.getusage(30, record.machineid),
                "ansible": ansible,
                "scratch": scratch,
                "battery": 'NaN',
                "machineid": record.machineid
            }
            temp.append(computerdata)
        displaydata[i]['values'] = temp
        displaydata[i]['total'] = len(result)
    return dict(data=displaydata,
                date=timenow,
                repodate=date,
                online=onlinecount,
                userslog=userslog)

@app.route(settings.PREFIX + '/search/user/')
@view('search_user')
def search():
    return dict(startdate="1970-01-01", enddate="2077-12-31", username = "", computername = "")

@app.route(settings.PREFIX + '/search/user/', method='POST')
@view('search_user')
def search():
    session = Session()
    username = request.forms.getunicode('usernm')
    computername = request.forms.getunicode('computername')
    try:
        startdate = request.forms.getunicode('startdate')
        startdate = datetime.datetime.fromisoformat(startdate)
        enddate = request.forms.getunicode('enddate')
        enddate = datetime.datetime.fromisoformat(enddate)
    except:
        redirect(settings.PREFIX + "/search/user/")
    now = datetime.datetime.today()
    result = session.query(UserSession, Computer).join(Computer, Computer.id == UserSession.computer)
    result = result.filter(UserSession.username.like("%%%s%%" % username))
    result = result.filter(Computer.hostname.like("%%%s%%" % computername))
    result = result.filter(UserSession.session_start <= enddate)
    if enddate >= now:
        result = result.filter(or_(ComputerSession.session_end >=startdate, ComputerSession.session_end == None))
    else:
        result = result.filter(ComputerSession.session_end >= startdate)
    result = result.all()
    session.close()
    return dict(query=result, startdate=startdate.strftime("%Y-%m-%d"), enddate=enddate.strftime("%Y-%m-%d"), username = username, computername = computername)

@app.route(settings.PREFIX + '/search/computer/')
@view('search_computer')
def search():
    return dict(startdate="1970-01-01", enddate="2077-12-31", computername = "")

@app.route(settings.PREFIX + '/search/computer/', method='POST')
@view('search_computer')
def search():
    session = Session()
    computername = request.forms.getunicode('computername')
    try:
        startdate = request.forms.getunicode('startdate')
        startdate = datetime.datetime.fromisoformat(startdate)
        enddate = request.forms.getunicode('enddate')
        enddate = datetime.datetime.fromisoformat(enddate)
    except:
        redirect(settings.PREFIX + "/search/computer/")
    now = datetime.datetime.now()
    result = session.query(ComputerSession, Computer).join(Computer, Computer.id == ComputerSession.computer)
    result = result.filter(Computer.hostname.like("%%%s%%" % computername))
    result = result.filter(ComputerSession.session_start <= enddate)
    if enddate >= now:
        result = result.filter(or_(ComputerSession.session_end >=startdate, ComputerSession.session_end == None))
    else:
        result = result.filter(ComputerSession.session_end >= startdate)
    result = result.all()
    session.close()
    return dict(query=result, startdate=startdate.strftime("%Y-%m-%d"), enddate=enddate.strftime("%Y-%m-%d"), computername = computername)

@app.route(settings.PREFIX + '/debug/')
@view('debug')
def debugfunc():
    """ Debug function for data """
    session = Session()
    usersloggedin = session.query(UserSession).all()
    rooms = session.query(Room).all()
    computers = (session.query(ComputerSession)
                .order_by(ComputerSession.session_end)
                .order_by(ComputerSession.session_start)
                .all())
    computer_list = session.query(Computer).all()
    graphs = glob.glob('rrds/*_ansible.rrd')
    graphs = [i.replace('rrds/','').replace('_ansible.rrd','') for i in graphs]
    return dict(users=usersloggedin,
                rooms= rooms,
                computers=computers,
                computer = computer_list,
                graphs=graphs)

@app.route(settings.PREFIX + '/termload/')
@view('termload')
def termserverstatus():
    """ Shows cpu load and user count on terminal servers """
    servers = []
    session = Session()
    result = (session.query(Computer)
             .filter(Computer.hostname.in_(settings.TERMSERVRES))
             .group_by(Computer.hostname)
             .having(func.max(Computer.first_report))
             .order_by(Computer.hostname)
             .all())
    for record in result:
        t = {'name': record.hostname}
        t["users"] = len(session_user.get_active_users(session, record.machineid))
        t["load"] = rrd_cpu.last(record.hostname + ".dcti.sut.ru")
        servers.append(t)
    return dict(servers=servers)

@app.route(settings.PREFIX +'/computer/edit/<machineid>', method='POST')
@require_groups(settings.ALLOWED_GROUPS)
@view('edit')
def machineedit(machineid):
    searchkey = request.forms.getunicode('room')
    session = Session()
    result = session.query(Computer).filter(Computer.machineid == machineid).first()
    if not result:
        redirect(settings.PREFIX + "/")
    room = session.query(Room).filter(Room.id == int(searchkey)).first()
    if not room:
        redirect(settings.PREFIX + "/")
    result.room = int(searchkey)
    session.commit()
    room = session.query(Room).filter(Room.id == result.room).first()
    rooms = session.query(Room).all()
    return dict(machineid=machineid,room=room, rooms=rooms, computer = result)

@app.route(settings.PREFIX +'/computer/edit/<machineid>')
@require_groups(settings.ALLOWED_GROUPS)
@view('edit')
def machineedit(machineid):
    session = Session()
    result = session.query(Computer).filter(Computer.machineid == machineid).first()
    if not result:
        redirect(settings.PREFIX + "/")
    room = session.query(Room).filter(Room.id == result.room).first()
    rooms = session.query(Room).all()
    return dict(machineid=machineid,room=room, rooms=rooms, computer = result)

@app.route(settings.PREFIX +'/computer/<machineid>/<period:re:[d,w,m,y]>')
@app.route(settings.PREFIX +'/computer/<machineid>')
@view('computer')
def machinestats2(machineid,period = 'w'):
    """ Output stats for specific computer """
    session = Session()
    result = session.query(Computer).filter(Computer.machineid == machineid).first()
    if not result:
        redirect(settings.PREFIX + "/")
    hostname = expand_hostname(result.hostname)
    days = period_to_days(period)
    popularity = usage.getpopularity(days, machineid)
    samehostname = (session.query(Computer)
            .filter(Computer.hostname == result.hostname)
            .order_by(Computer.last_report)
            .all())
    return dict(date=datetime.datetime.now(),
                machine=hostname,
                popularity=popularity,
                attr=machineid,
                group=False,
                period=period,samehost=samehostname)


@app.route(settings.PREFIX +'/group/<grp>/<period:re:[d,w,m,y]>')
@app.route(settings.PREFIX +'/group/<grp>')
@view('group')
def machinestats(grp, period = 'w'):
    """ Output stats for specific group """
    session = Session()
    room  = session.query(Room).filter(Room.name == grp).first()
    if not room:
        redirect(settings.PREFIX + "/")
    result = (session.query(Computer)
             .filter(Computer.room == room.id)
             .order_by(Computer.hostname)
             .all())
    popularity = {}
    days = period_to_days(period)
    for i in result:
        hostname = expand_hostname(i.hostname)
        popularity[i.hostname] = usage.getpopularity(days, i.machineid)
    return dict(date=datetime.datetime.now(),
                hosts=result,
                popularity=popularity,
                attr=room.name,
                period=period,
                group=True)

@app.route(settings.PREFIX +'/graph/<grp:re:[i,g]>/<hostname>_<typ>')
@app.route(settings.PREFIX +'/graph/<grp:re:[i,g]>/<hostname>_<typ>/<period:re:[d,w,m,y]>')
def graphs_func(hostname, typ, grp, period = 'w'):
    """ Output graph for specific group """
    result = "Error"
    if grp == "g":
        session = Session()
        room  = session.query(Room).filter(Room.name == hostname).first()
        if not room:
            return result
        result = (session.query(Computer)
                 .filter(Computer.room == room.id)
                 .order_by(Computer.hostname)
                 .all())
        hostname = [room.name,]
        for i in result:
            host = expand_hostname(i.hostname)
            hostname.append(host)
        hostname = tuple(hostname)
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
    """ Accept ansible data """
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
    try:
        ok_value = request.json['ok']
        tmp = request.json.get('change',None)
        if tmp is None:
            tmp = request.json['changed']
        change_value = tmp
        unreachable_value = request.json['unreachable']
        failed_value = request.json['failed']
        rrd_ansible.insert(hostname, [ok_value, change_value, unreachable_value, failed_value])
    except BaseException:
        pass
    return dict()

@app.route(settings.PREFIX +'/api/scratch', method='POST')
def acceptscratchdata():
    """ Accept scratch data """
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
    """ Accept all remaining data """
    ip_addr = request.environ.get("REMOTE_ADDR")
    hostname = request.environ.get("REMOTE_HOST")
    if hostname is None:
        hostname = socket.gethostbyaddr(ip_addr)[0]
    reportedhostname = request.json['hostname']
    machineid = request.json['machineid']
    uptime = request.json['uptime']
    users = request.json['users']
    cpu = request.json['cpu']
    rrd_uptime.insert(hostname, [uptime, ])
    rrd_cpu.insert(hostname, [cpu['load'], cpu['loadavg'], cpu['cores']])
    rrd_users.insert(hostname, [len(set(users)),])
    session = Session()
    computer.add(session, machineid, ip_addr, reportedhostname)
    session_pc.update_session(session, machineid, uptime)
    session_user.update_session(session, machineid, users)
    computer.update(session, machineid, ip_addr, reportedhostname)
    # FIXME update uptime and ansible tables here (do we need them?)
    return dict()

@app.route(settings.PREFIX + r'/<filename:re:.*\.css>')
def send_css(filename):
    """ Send css files """
    return static_file(filename, root='./files/', mimetype='text/css')

@app.route(settings.PREFIX + r'/<filename:re:.*\.js>')
def send_js(filename):
    """ Send js files """
    return static_file(filename, root='./files/', mimetype='text/javascript')

if __name__ == '__main__':
    bottle.run(app,
        host='127.0.0.1',
        port=8086,
        reloader=True)
