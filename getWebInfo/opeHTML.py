# -*- coding: utf-8 -*-
import os
import requests
import opeExcel
from lxml import etree
from lxml import html
HEADER_REQUEST = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}

def preHandleData(infoList):# 处理空格及换行问题
  postInfoList = []
  for i in range(0, len(infoList)):
    postInfoList.append(infoList[i].strip())#strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
  while "" in postInfoList:
    postInfoList.remove("")
  return postInfoList

def parseXpath(page_html, theXpath):
  infoList = page_html.xpath(theXpath)
  return preHandleData(infoList)

def parseUrl(page_url, theXpath):
  response = requests.get(page_url, headers=HEADER_REQUEST).content
  # 将HTML源码字符串转换尘土HTML对象
  page_html = etree.HTML(response)
  #解析出信息列表
  infoList = parseXpath(page_html, theXpath)
  for i in range(0, len(infoList)):
    print("parseUrl："+infoList[i])
  return infoList

def parseUrl_2(page_url, title_xpath, link_xpath):
  response = requests.get(page_url, headers=HEADER_REQUEST).content
  # 将HTML源码字符串转换尘土HTML对象
  page_html = etree.HTML(response)
  # 博客文章的标题
  title_list = parseXpath(page_html, title_xpath)
  # 博客文章的链接
  link_list = parseXpath(page_html, link_xpath)
  # print("csdn_article_title_list: " + str(len(csdn_article_title_list)))
  # print("csdn_article_link_list: " + str(len(csdn_article_link_list)))
  for i in range(0, len(title_list)):
    print("标题："+title_list[i])
    print("链接："+link_list[i])    
  return title_list, link_list

def parseUrlCSDN(page_url, type_xpath, title_xpath, link_xpath, publishDate_xpath, readerCount_xpath, commentCount_xpath):
  response = requests.get(page_url, headers=HEADER_REQUEST).content
  # 将HTML源码字符串转换尘土HTML对象
  page_html = etree.HTML(response)
  # 博客文章的标题
  title_list = parseXpath(page_html, title_xpath)
  # 博客文章的链接
  link_list = parseXpath(page_html, link_xpath)
  # 博客文章的发布日期
  publishDate_list = parseXpath(page_html, publishDate_xpath)
  # 博客文章的类型
  type_list = parseXpath(page_html, type_xpath)
  # 博客文章的阅读数
  readerCount_list = parseXpath(page_html, readerCount_xpath)
  # 博客文章的评论数
  commentCount_list = parseXpath(page_html, commentCount_xpath) 
  for i in range(0, len(title_list)):
    # print("类型："+type_list[i])    
    print("标题："+title_list[i])
    print("链接："+link_list[i])
    print("发布："+publishDate_list[i])
    print("阅读："+readerCount_list[i])
    print("评论："+commentCount_list[i]) 
  return type_list, title_list, link_list, publishDate_list, readerCount_list, commentCount_list

def parseCSDNHTML():
  page_url = "https://blog.csdn.net/innost/article/list/1"
  # 博客文章的标题
  title_xpath = "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/text()"
  link_xpath = "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/@href"
  publishDate_xpath = "//div[@class='info-box d-flex align-content-center']/p/span[@class='date']/text()"
  type_xpath = "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/span/text()"
  readerCount_xpath = "//div[@class='info-box d-flex align-content-center']/p//span[last()-1][@class='read-num']/text()"
  commentCount_xpath = "//div[@class='info-box d-flex align-content-center']/p//span[last()][@class='read-num']/text()"
  type_list, title_list, link_list, publishDate_list, readerCount_list, commentCount_list = parseUrlCSDN(page_url, 
    type_xpath, title_xpath, link_xpath, publishDate_xpath, readerCount_xpath, commentCount_xpath)
  
  print("title_list: " + str(len(title_list)))
  print("link_list: " + str(len(link_list)))
  print("publishDate_list: " + str(len(publishDate_list)))
  print("type_list: " + str(len(type_list)))
  print("readerCount_list: " + str(len(readerCount_list)))
  print("commentCount_list: " + str(len(commentCount_list)))

def parseTestHTML():
  #文章链接：https://www.jianshu.com/p/1575db75670f
  filename = os.getcwd()+"\\test.html"
  fp = open(filename, 'rb')
  html = fp.read().decode('utf-8')
  tree = etree.HTML(html)
  #1. 匹配包含某属性的所有的属性值//@lang
  print(tree.xpath('//@code'))
  #2. 选取若干路径|,这个符号用于在一个xpath中写多个表达式用，用|分开，每个表达式互不干扰
  print(tree.xpath('//div[@id="testid"]/h2/text() | //li[@data]/text()')) #多个匹配条件
  #3. child：选取当前节点的所有子元素
  print(tree.xpath('//div[@id="testid"]/child::ul/li/text()')) #child子节点定位
  #>>['84', '104', '223']
  print(tree.xpath('//div[@id="testid"]/child::*')) #child::*当前节点的所有子元素
  #>>[<Element h2 at 0x21bd148>, <Element ol at 0x21bd108>, <Element ul at 0x21bd0c8>]
  #定位某节点下为ol的子节点下的所有节点
  print(tree.xpath('//div[@id="testid"]/child::ol/child::*/text()'))
  #>>['1', '2', '3']
  #5. attribute：选取当前节点的所有属性
  print(tree.xpath('//div/attribute::id')) #attribute定位id属性值
  #>>['testid', 'go']
  print(tree.xpath('//div[@id="testid"]/attribute::*')) #定位当前节点的所有属性
  #>>['testid', 'first']

def parseCSDNTestHTML():
  filename = os.getcwd()+"\\csdn_test.html"
  fp = open(filename, 'rb')
  html = fp.read().decode('utf-8')
  page_html = etree.HTML(html)
  #"//div[@class='info-box d-flex align-content-center']/p/span[@class='date']")
  # 博客文章的阅读数
  csdn_article_readerCount_list = page_html.xpath(
    "//div[@class='info-box d-flex align-content-center']/p//span[last()-1][@class='read-num']/text()")
  # 博客文章的评论数
  csdn_article_commentCount_list = page_html.xpath(
    "//div[@class='info-box d-flex align-content-center']/p//span[last()][@class='read-num']/text()")
  print("csdn_article_readerCount_list: " + csdn_article_readerCount_list[0])
  print("csdn_article_commentCount_list: " + csdn_article_commentCount_list[0])  


def parseGityuanHTML():#http://gityuan.com/archive/
  #网页信息
  page_url = "http://gityuan.com/archive/"
  title_xpath = "//div[@class='post-preview']/a/text()"
  link_xpath = "//div[@class='post-preview']/a/@href"
  # Excel文件名称
  file_name = os.getcwd()+"\Gityuan_articles.xls"
  author_name = "Gityuan"
  # 写入表头数据
  headerData = [["文章标题", "文章链接",], ]
  opeExcel.create_excel_sheet(file_name, author_name)
  opeExcel.write_excel_xls_append(file_name, author_name, headerData)
  #解析url中的标题和链接
  title_list, link_list = parseUrl_2(page_url, title_xpath, link_xpath)  
  #Gityuan的网站返回的都是不带"http://gityuan.com"的链接信息
  for i in range(0, len(link_list)):
    link_list[i] = "http://gityuan.com" + link_list[i]
  # 将数据保存到excel表格中
  opeExcel.write_excel_xls_append_all(file_name, author_name, title_list, link_list)
#解析特定URL网页标题和链接信息并返回


def parseLightMoon():#http://light3moon.com/1986/12/20/%E6%96%87%E7%AB%A0%E7%B4%A2%E5%BC%95/
  #网页信息
  page_url = "http://light3moon.com/1986/12/20/%E6%96%87%E7%AB%A0%E7%B4%A2%E5%BC%95/"
  title_xpath = "//div[@class='article-content']/p/a/text()"
  link_xpath = "//div[@class='article-content']/p/a/@href"
  #Excel文件名称
  file_name = os.getcwd()+"\LightMoon_articles.xls"
  author_name = "LightMoon"
  # 写入表头数据
  headerData = [["文章标题", "文章链接",], ]
  opeExcel.create_excel_sheet(file_name, author_name)
  opeExcel.write_excel_xls_append(file_name, author_name, headerData)
  #解析url中的标题和链接
  title_list, link_list = parseUrl_2(page_url, title_xpath, link_xpath)   
  # 将数据保存到excel表格中
  opeExcel.write_excel_xls_append_all(file_name, author_name, title_list, link_list)


def main_func():
  parseCSDNHTML()

if __name__ == '__main__':
  main_func()