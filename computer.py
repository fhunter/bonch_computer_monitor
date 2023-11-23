""" Computer registration module"""

import datetime
from my_db import Computer, Room

def add(db_session, machineid, ip_addr, reportedhostname):
    """ Register computer in database by machineid, ip and hostname """
    computer = (db_session.query(Computer)
               .filter(Computer.machineid == machineid)
               .filter(Computer.ip == ip_addr)
               .filter(Computer.hostname == reportedhostname)
               .first())
    if not computer:
        room = db_session.query(Room).filter(Room.name == "Прочее").first()
        if not room:
            room = Room(name = "Прочее")
            db_session.add(Room)
        computer = Computer(hostname = reportedhostname,
                            ip = ip_addr,
                            machineid = machineid,
                            room = room.id)
        db_session.add(computer)
        db_session.commit()

def update(db_session, machineid, ip_addr, reportedhostname):
    """ Update computer's record in database by machineid, ip and hostname """
    computer = (db_session.query(Computer)
               .filter(Computer.machineid == machineid)
               .filter(Computer.ip == ip_addr)
               .filter(Computer.hostname == reportedhostname)
               .first())
    if computer:
        computer.last_report = datetime.datetime.now()
        db_session.commit()
