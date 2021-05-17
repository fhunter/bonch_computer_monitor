# vim: set fileencoding=utf-8 :
import sqlite3
import secrets

def db_open():
	conn = sqlite3.connect("database.sqlite3",timeout=25)
	conn.execute('pragma foreign_keys = on')
	conn.execute('pragma journal_mode = wal')
	return conn

def db_exec_sql(*request):
	if len(request)<1:
		return None
	conn = db_open()
	cursor = conn.cursor()
	if len(request)==1:
		cursor.execute(request[0])
	else:
		cursor.execute(request[0],request[1])
	result=cursor.fetchall()
	conn.commit()
	conn.close()
	return result
	

