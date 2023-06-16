# vim: set fileencoding=utf-8 :
#import secret

""" Database access abstraction module """

import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///database_.sqlite3', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

def db_exec_sql(*params):
    raise Exception("Not implemented %s" % (params))

class Computer(Base):
    __tablename__ = 'computer'

    id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable = False)
    last_report = Column(DateTime, nullable = False, default=datetime.datetime.now())
    uptime = Column(Integer, nullable = False)
    ip = Column(String, nullable = False)
    machineid = Column(String, nullable = False)
    room = Column(Integer, ForeignKey('room.id'))

    def __repr__(self):
        return "<Computer(hostname='%s' machineid='%s' last_report='%s' uptime='%s' ip='%s' room='%s')>" % (
            self.hostname, self.machineid, self.last_report, self.uptime, self.ip, self.room)

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False, unique = True)

    def __repr__(self):
        return "<Room(name='%s')>" % (self.name,)

class ComputerSession(Base):
    __tablename__ = 'computer_session'

    id = Column(Integer, primary_key=True)
    session_start = Column(DateTime,nullable=False, default=datetime.datetime.now())
    session_end = Column(DateTime,nullable=True, default=None)
    computer = Column(Integer, ForeignKey('computer.id'))

    def __repr__(self):
        return "<ComputerSession(start='%s', end='%s', computer='%s')>" % (
                            self.session_start, self.session_end, self.computer)

class UserSession(Base):
    __tablename__ = 'user_session'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable = False)
    session_start = Column(DateTime,nullable=False, default=datetime.datetime.now())
    session_end = Column(DateTime,nullable=True, default=None)
    computer = Column(Integer, ForeignKey('computer.id'))
    
    def __repr__(self):
        return "<UserSession(start='%s', end='%s', computer='%s' username='%s')>" % (
                            self.session_start, self.session_end, self.computer, self.username)

#class User(Base):
#    __tablename__ = 'users'
#
#    id = Column(Integer, primary_key=True)
#    username = Column(String, unique=True, nullable =False)
#    fio = Column(String, nullable = False, default = "")
#    studnum = Column(String, nullable = False, default ="")
#    quota = relationship(
#        "Quota",
#        uselist = False,
#        back_populates="username",
#        cascade="all, delete-orphan")
#    queue = relationship("Queue", back_populates="username", cascade="all, delete-orphan")
#
#    def __repr__(self):
#        return "<User(username='%s', fio='%s', studnum='%s')>" % (
#                            self.username, self.fio, self.studnum)
#
#class Queue(Base):
#    __tablename__ = 'queue'
#    id = Column(Integer, primary_key=True)
#    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#    username = relationship("User", back_populates="queue")
#    password = Column(String,nullable=False)
#    date = Column(DateTime,nullable=False, default=datetime.datetime.now())
#    done = Column(Boolean, nullable=False, default=False)
#    resetedby = Column(String)
#
#    def __repr__(self):
#        return "<Queue(username='%s', password='%s', date='%s' done='%s' resetby='%s')>" % (
#                            self.user_id, self.password, self.date, self.done, self.resetedby)
#
#class Quota(Base):
#    __tablename__ = 'quota'
#    id = Column(Integer, primary_key=True)
#    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
#    username = relationship("User", back_populates="quota")
#    usedspace = Column(Integer, nullable=False, default=0)
#    softlimit = Column(Integer, nullable=False, default=0)
#
#    def __repr__(self):
#        return "<Quota(username='%s', used space='%s',  softlimit='%s')>" % (
#                            self.user_id, self.usedspace, self.softlimit)
#
#
Base.metadata.create_all(engine)
