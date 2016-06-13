#! /usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import tempfile
import shutil
from lxml import etree
def parse_xml(filename):
    tree = etree.parse(filename)#将xml解析为树结构  
    root = tree.getroot()#获得该树的树根  
    for article in root:#这样便可以遍历根元素的所有子元素(这里是article元素)  
        print "Element Name:",article.tag#用.tag得到该子元素的名称  
        for field in article:#遍历article元素的所有子元素(这里是指article的author，title，volume，year等)  
            print field.tag,":",field.text#同样地，用.tag可以得到元素的名称，而.text可以得到元素的内容  
        mdate=article.get("mdate")#用.get("属性名")可以得到article元素相应属性的值  
        key=article.get("key")  
        print "mdate:",mdate  
        print "key",key  
        print ""#隔行分开不同的article元素

if __name__ == "__main__":
    parse_xml(os.getcwd()+os.sep+"data.xml")    
