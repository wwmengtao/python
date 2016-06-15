#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3
tableName='M_T'

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
	#cursor.execute('create table IF NOT EXISTS %s (id varchar(20) primary key, name varchar(20))')
	cursor.execute('create table IF NOT EXISTS %s (id text, name text, PRIMARY KEY ( id, name) );'% tableName)
	# 关闭Cursor:
	cursor.close()
	# 关闭Connection:
	conn.close()

def insert(sqlite3Name):
	conn = sqlite3.connect(sqlite3Name)
	# 创建一个Cursor:
	cursor = conn.cursor()
	# 继续执行一条SQL语句，插入一条记录:
	cursor.execute('insert into %s values(?,?)'%tableName,("1", "Michael"))
	cursor.execute('insert into %s (id, name) values(?,?)'%tableName,("1", "Mike"))
	cursor.execute('insert into %s values ("2", "Smith")'%tableName)
	cursor.execute('insert into %s (id, name) values ("3", "Brown")'%tableName)
	cursor.execute('insert into %s values(?, ?)'%tableName, ("4", "Rose"))
	cursor.execute('insert or replace into %s values(?, ?)'%tableName, ("4", "Rose1"))
	# 通过rowcount获得本次操作插入的行数:
	print "cursor.rowcount:",cursor.rowcount
	#批量插入数据
	others = [("5","James"), ("6","Lemon"), ("7","Google")]
	cursor.executemany('insert into %s values(?, ?)'%tableName, others)
	# 通过rowcount获得本次操作插入的行数:
	print "cursor.rowcount:",cursor.rowcount
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
	cursor.execute('select * from %s where id=?'%tableName, ("1"))
	printResult(cursor,"id")
	cursor.execute('select * from %s where id=? and name=?'%tableName, ("1",'Mike'))		
	printResult(cursor,"id and name:")
	#查找数据表中全部内容并打印出来
	cursor.execute('select * from %s'%tableName)
	print "All of db:"
	print cursor.fetchall()
	#获取当前数据表总行数
	cursor.execute("SELECT COUNT(*) AS dbCount FROM %s"%tableName)
	dbcount=cursor.fetchone()
	print "Count of db:"
	print dbcount[0]
	cursor.close()
	cursor.close()
	conn.close()

def modify(sqlite3Name):
	conn = sqlite3.connect(sqlite3Name)
	cursor = conn.cursor()
	# 执行修改语句:
	cursor.execute('update %s set name="Smith_m" where id="2"')
	conn.commit()
	cursor.close()
	conn.close()

def delete(sqlite3Name):
	conn = sqlite3.connect(sqlite3Name)
	cursor = conn.cursor()
	# 执行删除语句:
	cursor.execute('delete from %s where id = 3')
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
	sqlite3Name='sqlite3Test.db'
	create(sqlite3Name)
	insert(sqlite3Name)
	query(sqlite3Name)
	#modify(sqlite3Name)
	#delete(sqlite3Name)