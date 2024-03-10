# vim: set fileencoding=utf-8 :
#import secret

""" Database access abstraction module """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

engine = create_engine('sqlite:///database_.sqlite3', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Computer(Base):
    """ Computer representation table """
    __tablename__ = 'computer'

    id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable = False)
    first_report = Column(DateTime, nullable = False, default=func.now())
    last_report = Column(DateTime, nullable = False, default=func.now())
    ip = Column(String, nullable = False)
    machineid = Column(String, nullable = False)
    room = Column(Integer, ForeignKey('room.id'))

    def __repr__(self):
        tmpl = "<Computer(hostname='%s' machineid='%s' "
        tmpl = tmpl + "first_report='%s' last_report='%s' "
        tmpl = tmpl + "ip='%s' room='%s')>"
        return tmpl % (
            self.hostname, self.machineid, self.first_report, self.last_report, self.ip, self.room)

class Uptime(Base):
    """ Uptime table """
    __tablename__ = 'uptime'
    id = Column(Integer, primary_key=True)
    last_report = Column(DateTime, nullable = False, default=func.now())
    uptime = Column(Integer, nullable = False)
    computer = Column(Integer, ForeignKey('computer.id'))

    def __repr__(self):
        return "<Uptime(last_report='%s' computer='%s' uptime='%s')>" % (
            self.last_report, self.computer, self.uptime)



class Room(Base):
    """ Room list table """
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False, unique = True)

    def __repr__(self):
        return "<Room(name='%s')>" % (self.name,)

class ComputerSession(Base):
    """ Computer run times table """
    __tablename__ = 'computer_session'

    id = Column(Integer, primary_key=True)
    session_start = Column(DateTime,nullable=False, default=func.now())
    session_end = Column(DateTime,nullable=True, default=None)
    computer = Column(Integer, ForeignKey('computer.id'))

    def __repr__(self):
        return "<ComputerSession(start='%s', end='%s', computer='%s')>" % (
                            self.session_start, self.session_end, self.computer)

class UserSession(Base):
    """ User login times table """
    __tablename__ = 'user_session'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable = False)
    session_start = Column(DateTime,nullable=False, default=func.now())
    session_end = Column(DateTime,nullable=True, default=None)
    computer = Column(Integer, ForeignKey('computer.id'))

    def __repr__(self):
        return "<UserSession(start='%s', end='%s', computer='%s' username='%s')>" % (
                            self.session_start, self.session_end, self.computer, self.username)

Base.metadata.create_all(engine)
