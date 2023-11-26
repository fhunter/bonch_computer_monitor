import datetime
from sqlalchemy.sql import func
from sqlalchemy import or_
from my_db import ComputerSession, Computer, UserSession

def get_active_users(db_session, machineid):
    computer = db_session.query(Computer).filter(Computer.machineid == machineid).first()
    usersloggedin = (db_session.query(UserSession)
                    .filter(UserSession.session_end.is_(None))
                    .filter(UserSession.computer == computer.id)
                    .all())
    return list({i.username for i in usersloggedin})

def get_sessions(db_session, machineid, start, end):
    now = datetime.datetime.now()
    computer = db_session.query(Computer).filter(Computer.machineid == machineid).first()
    sessions = (db_session.query(UserSession,
                                 func.coalesce(UserSession.session_end, now)
                                 .label("session_end_c"))
               .filter(UserSession.computer == computer.id)
               .filter(or_(UserSession.session_start.between(start,end),
                           func.coalesce(UserSession.session_end, now).between(start,end)))
               .all())
    return sessions

def clean_sessions(db_session): # check if any sessions are stale (close anything that is open on closed PCs
    time = datetime.datetime.now()
    # find all computers with more than 10 minutes since last report
    timedelta = datetime.timedelta(minutes = 10)
    computers = (db_session.query(Computer)
                .filter(Computer.last_report <= (time - timedelta))
                .all())
    for i in computers:
        sessions = (db_session.query(UserSession)
                   .filter(UserSession.computer == i.id)
                   .filter(UserSession.session_end.is_(None)).all())
        for j in sessions:
            j.session_end = i.last_report
    db_session.commit()

def close_session(db_session, machineid, user):
    computer = db_session.query(Computer).filter(Computer.machineid == machineid).first()
    sessions = (db_session.query(UserSession)
               .filter(UserSession.computer == computer.id)
               .filter(UserSession.username == user)
               .filter(UserSession.session_end.is_(None))
               .all())
    for i in sessions:
        i.session_end = computer.last_report
    db_session.commit()


def update_session(db_session, machineid, users_list):
#    # Логика:
#    1. проверить все открытые сессии по этому компьютеру, где пользователи не в users_list, закрыть их
#    2. если пользовательской сессии нет в списке открытых - открыть новую
    computer = db_session.query(Computer).filter(Computer.machineid == machineid).first()
    time = datetime.datetime.now()
    session = (db_session.query(UserSession)
              .filter(UserSession.computer == computer.id)
              .filter(UserSession.session_end.is_(None))
              .filter(UserSession.username.notin_(users_list))
              .all())
    for i in session:
        close_session(db_session, machineid, i.username)
    activesessions = (db_session.query(UserSession)
                     .filter(UserSession.computer == computer.id)
                     .filter(UserSession.session_end.is_(None))
                     .all())
    activeusers = [i.username for i in activesessions]
    remaining_users = list(set(users_list) - set(activeusers))
    for i in remaining_users:
        user = UserSession(username = i, session_start = time, computer = computer.id)
        db_session.add(user)
    db_session.commit()
