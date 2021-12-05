import time
from my_db import db_exec_sql


def get_sessions(hostname, start, end):
    #CREATE TABLE host_sessions (id integer primary key autoincrement not null, hostname text not null, starttime datetime not null, endtime datetime);
    result = db_exec_sql("select hostname, starttime, endtime from host_sessions where hostname = ? and starttime > ?", (hostname, start))
    return []

def clean_sessions(): # check if any sessions are stale
    pass

def close_session(hostname):
    db_exec_sql("update host_sessions set endtime = ? where hostname = ? and endtime = NULL", (time.time(), hostname,))

def update_session(hostname, uptime):
    result = db_exec_sql("select host_sessions where hostname = ? and endtime = NULL", (hostname,))
    if len(result) == 0:
        # No records - open one
        #db_exec_sql("insert into host_sessions 
        pass
    else:
        pass
    pass
