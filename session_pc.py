import datetime
from my_db import ComputerSession, Computer


def get_sessions(db_session, machineid, start, end):
    # FIXME - reports all sessions
    computer = db_session.query(Computer).filter(Computer.machineid == machineid).first()
    sessions = db_session.query(ComputerSession).filter(Computer.machineid == computer.id).all()
    return sessions

def clean_sessions(db_session): # check if any sessions are stale
    time = datetime.datetime.now()
    # find all computers with more than 10 minutes since last report
    timedelta = datetime.timedelta(minutes = 10)
    computers = (db_session.query(Computer)
                .filter((time - Computer.last_report) >= timedelta)
                .all())
    for i in computers:
        sessions = (db_session.query(ComputerSession)
                   .filter(ComputerSession.computer == i.id)
                   .filter(ComputerSession.session_end.is_(None)).all())
        for j in sessions:
            j.session_end = i.last_report
    db_session.commit()

def close_session(db_session, machineid):
    computer = db_session.query(Computer).filter(Computer.machineid == machineid).first()
    sessions = (db_session.query(ComputerSession)
               .filter(ComputerSession.computer == computer.id)
               .filter(ComputerSession.session_end.is_(None))
               .all())
    for i in sessions:
        i.session_end = computer.last_report
    db_session.commit()

def update_session(db_session, machineid, uptime):
    # Логика:
    # 1. найти подходящий session с подходящим временем открытия по uptime.
    # 1.1. если есть - продлить или переоткрыть сессию.
    # 1.2. если нет - проверить открытые сессии,
    # 1.2. закрыть открытые по времени последнего отчёта, создать новую.
    computer = db_session.query(Computer).filter(Computer.machineid == machineid).first()
    time = datetime.datetime.now()
    uptimedelta_p = datetime.timedelta(seconds = uptime + 2.5*60)
    uptimedelta_n = datetime.timedelta(seconds = uptime - 2.5*60)
    session = (db_session.query(ComputerSession)
              .filter(ComputerSession.computer == computer.id)
              .filter((time - ComputerSession.session_start) < uptimedelta_p)
              .filter((time - ComputerSession.session_start) > uptimedelta_n)
              .first())
    if session:
        # Сессия существует, продлеваем/переоткрываем
        session.session_end = None
    else:
        # Сессии нет. Закрываем все, добавляем новую
        close_session(db_session, machineid)
        start = time - datetime.timedelta(seconds = uptime)
        session = ComputerSession(session_start = start, computer = computer.id)
        db_session.add(session)
    db_session.commit()
