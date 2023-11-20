import datetime
from my_db import Computer, Room

def add_or_update(session, machineid, ip_addr, reportedhostname):
    computer = session.query(Computer).filter(Computer.machineid == machineid).filter(Computer.ip == ip_addr).filter(Computer.hostname == reportedhostname).first()
    if computer:
        computer.last_report = datetime.datetime.now()
        session.commit()
    else:
        room = session.query(Room).filter(Room.name == "Прочее").first()
        if not room:
            room = Room(name = "Прочее")
            session.add(Room)
        computer = Computer(hostname = reportedhostname, ip = ip_addr, machineid = machineid, room = room.id)
        session.add(computer)
        session.commit()
