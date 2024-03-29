PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE machines (id integer primary key autoincrement not null, ip text unique not null, hostname text,lastupdate datetime not null, room text default null);
CREATE TABLE hostnames (id integer primary key autoincrement not null, ip text not null, hostname text, time datetime not null);
CREATE TABLE uptime (id integer primary key autoincrement not null, ip text not null,  time datetime not null, uptime integer not null);
CREATE TABLE users (id integer primary key autoincrement not null, ip text not null,  time datetime not null, users text);
CREATE TABLE user_sessions (id integer primary key autoincrement not null, hostname text not null, starttime datetime not null, endtime datetime, users text);
CREATE TABLE host_sessions (id integer primary key autoincrement not null, hostname text not null, starttime datetime not null, endtime datetime);
CREATE UNIQUE INDEX hostnames_index on hostnames(ip, time);
CREATE INDEX load_index1 on load(ip, time);
CREATE INDEX users_index1 on users(ip, time);
COMMIT;
