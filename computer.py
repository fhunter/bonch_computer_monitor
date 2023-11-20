import datetime
from my_db import Computer

def add_or_update(session, machineid, ip_addr, reportedhostname):
    computer = session.query(Computer).filter(Computer.machineid == machineid).filter(Computer.ip == ip_addr).filter(Computer.hostname == reportedhostname).first()
    if computer:
        computer.last_report = datetime.datetime.now()
        session.commit()
    else:
        computer = Computer(hostname = reportedhostname, ip = ip_addr, machineid = machineid)
        session.add(computer)
        session.commit()
