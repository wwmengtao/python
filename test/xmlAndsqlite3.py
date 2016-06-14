#! /usr/bin/python
# -*- coding: utf-8 -*-
#node_text:将xml节点内容(包括子节点内容输出)
import os.path
import tempfile
import shutil
from lxml import etree
import re
import sqlite3
import sqlite3Test

# 将正则表达式编译成Pattern对象	
pattern_string_s = re.compile('<string.*?>')#匹配<string name=""...>内容
pattern_string_e = re.compile('</string.*>')#匹配</string>

#re_string:使用正则表达式消除etree.tostring引入的附加信息
def re_string(str,pattern_string):
	pattern = re.compile(pattern_string)
	match = pattern.search(str)
	if match:
		string_match=match.group(0)
		str=str.replace(string_match,"");
	return str

def node_text(node):
	global pattern_string_s
	global pattern_string_e
	eleNodeName=etree.tostring(node,encoding='utf-8',pretty_print=False)#将元素text连同sub_element一起获取
	eleNodeName=re_string(eleNodeName,pattern_string_s)
	eleNodeName=re_string(eleNodeName,pattern_string_e)
	return eleNodeName.strip()#移除字符串头尾指定的字符(默认为空格)

def parseXmlAndSave(fileName):
	sqlite3Name='sqlite3Xml.db'
	sqlite3Test.create(sqlite3Name)
	conn = sqlite3.connect(sqlite3Name)
	cursor = conn.cursor()
	tree = etree.parse(fileName)#将xml解析为树结构
	root = tree.getroot()#获得该树的树根 
	elements_root = root.findall("string")
	for s in elements_root:
		item_name = s.attrib.get("name")#或者s.get("name")
		item_text = node_text(s)
		print item_name,":",item_text
		cursor.execute('insert or replace into myTable values(?, ?)', (item_name, item_text))
	cursor.close()
	# 提交事务:
	conn.commit()
	conn.close()		

if __name__ == '__main__':
	fileName="E:/Bat_shell/Python/translation_mini/Settings/res/values/strings.xml"
	parseXmlAndSave(fileName)
