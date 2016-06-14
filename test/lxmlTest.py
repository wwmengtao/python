#! /usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import tempfile
import shutil
from lxml import etree

#node_text:将xml节点内容(包括子节点内容输出)
def node_text(node):
    eleNodeName=etree.tostring(node,encoding='utf-8',pretty_print=False)#将元素text连同sub_element一起获取
    eleNodeName=eleNodeName.replace("<"+node.tag+">","")
    eleNodeName=eleNodeName.replace("</"+node.tag+">","")
    return eleNodeName.strip()

#node_text2:将xml节点内容(包括子节点内容输出)，消除子节点的标签
def node_text2(node):  
    result = ""  
    for text in node.itertext():  
        result = result + text  
    return result  

#parse_xml:将xml中内容完整打印出来
def parse_xml(filename):
    tree = etree.parse(filename)#将xml解析为树结构  
    root = tree.getroot()#获得该树的树根 
    for element in root:#这样便可以遍历根元素的所有子元素(这里是element元素)  
        print "eleName:",element.tag#用.tag得到该子元素的名称  
        for eleNode in element:#遍历element元素的所有子元素(这里是指element的author，title，volume，year等)  
            if eleNode.tag=="title":  
                eleNodeText=node_text(eleNode)
                #eleNodeText=node_text2(eleNode)
                print eleNode.tag,":",eleNodeText
            else:
                print eleNode.tag,":",eleNode.text#同样地，用.tag可以得到元素的名称，而.text可以得到元素的内容  
        mdate=element.get("mdate")#用.get("属性名")可以得到element元素相应属性的值  
        key=element.get("key")  
        print "mdate:",mdate  
        print "key:",key
        print ""#隔行分开不同的element元素

#parse_xml2：解析xml文件中特定节点信息
def parse_xml2(filename):
    tree = etree.parse(filename)#将xml解析为树结构  
    root = tree.getroot()#获得该树的树根 
    elements_root = root.findall("article")
    for s in elements_root:
        item_date = s.attrib.get("mdate")#或者s.get("mdate")
        item_key = s.get("key")
        print "item_date:",item_date
        print "item_key:",item_key

if __name__ == "__main__":

    #下列有多种获取当前目录下的data.xml文件路径的方法
    fileName=os.getcwd()+os.sep+"data.xml"
    #fileName=os.path.join(os.getcwd(),"data.xml")
    #fileName='E:/Bat_shell/Python/test/data.xml'#Windows或者Linux环境下，使用“/”作为目录分隔符最保险
    parse_xml(fileName)
    #parse_xml2(fileName)