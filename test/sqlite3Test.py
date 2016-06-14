#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3

def create(sqlite3Name):
	#os.path.isfile('test.txt') #如果不存在就返回False 
	#os.path.exists(directory) #如果目录不存在就返回False
	if os.path.isfile(sqlite3Name):
		os.remove(sqlite3Name)
	# 连接到SQLite数据库
	# 数据库文件是test.db
	# 如果文件不存在，会自动在当前目录创建:
	conn = sqlite3.connect(sqlite3Name)
	# 创建一个Cursor:
	cursor = conn.cursor()
	# 执行一条SQL语句，创建user表:
	#cursor.execute('create table IF NOT EXISTS myTable (id varchar(20) primary key, name varchar(20))')
	cursor.execute('create table IF NOT EXISTS myTable (id text, name text, PRIMARY KEY ( id, name) );')
	# 关闭Cursor:
	cursor.close()
	# 关闭Connection:
	conn.close()

def insert(sqlite3Name):
	conn = sqlite3.connect(sqlite3Name)
	# 创建一个Cursor:
	cursor = conn.cursor()
	# 继续执行一条SQL语句，插入一条记录:
	cursor.execute('insert into myTable (id, name) values ("1", "Michael")')
	cursor.execute('insert into myTable (id, name) values ("1", "Mike")')
	cursor.execute('insert into myTable (id, name) values ("2", "Smith")')
	cursor.execute('insert into myTable (id, name) values ("3", "Brown")')
	cursor.execute('insert into myTable values(?, ?)', ("4", "Rose"))
	cursor.execute('insert or replace into myTable values(?, ?)', ("4", "Rose1"))
	# 通过rowcount获得插入的行数:
	print "cursor.rowcount:",cursor.rowcount
	cursor.close()
	# 提交事务:
	conn.commit()
	conn.close()

def printResult(cursor,tag):
	values = cursor.fetchall()# 获得查询结果集:
	for v in values:
		print tag,":",v

def query(sqlite3Name):
	conn = sqlite3.connect(sqlite3Name)
	cursor = conn.cursor()
	# 执行查询语句:
	cursor.execute('select * from myTable where id=?', ("1"))
	printResult(cursor,"id")
	cursor.execute('select * from myTable where id=? and name=?', ("1",'Mike'))		
	printResult(cursor,"id and name:")
	cursor.close()
	conn.close()

def modify(sqlite3Name):
	conn = sqlite3.connect(sqlite3Name)
	cursor = conn.cursor()
	# 执行修改语句:
	cursor.execute('update myTable set name="Smith_m" where id="2"')
	conn.commit()
	cursor.close()
	conn.close()

def delete(sqlite3Name):
	conn = sqlite3.connect(sqlite3Name)
	cursor = conn.cursor()
	# 执行删除语句:
	cursor.execute('delete from myTable where id = 3')
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
	sqlite3Name='sqlite3Test.db'
	create(sqlite3Name)
	insert(sqlite3Name)
	query(sqlite3Name)
	modify(sqlite3Name)
	delete(sqlite3Name)