# -*- coding: utf-8 -*-
import os
import requests
from lxml import etree
from lxml import html

def preHandleData(title_list):# 处理空格及换行问题
  csdn_article_title_list = []
  for i in range(0, len(title_list)):
    csdn_article_title_list.append(title_list[i].strip())#strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
  while "" in csdn_article_title_list:
    csdn_article_title_list.remove("")
  return csdn_article_title_list

def parseCSDNHTML():
  # response = requests.get('http://www.baidu.com')
  # # print(response.text)
  # print(response.content)
  # 请求头，以Chrome浏览器为例，可以在地址框中输入"about:version"，里面有header信息
  header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
  }
  page_url = "https://blog.csdn.net/innost/article/list/1"
  response = requests.get(page_url, headers=header).content
  # 将HTML源码字符串转换尘土HTML对象
  page_html = etree.HTML(response)
  # 博客文章的标题
  title_list = html.fromstring(response.decode()).xpath(
    "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/text()")
  # 处理换行问题
  csdn_article_title_list = preHandleData(title_list)
  # 博客文章的类型
  type_list = page_html.xpath("//div[@class='article-item-box csdn-tracking-statistics']/h4/a/span/text()")
  csdn_article_type_list = preHandleData(type_list)
  # 博客文章的链接
  link_list = page_html.xpath("//div[@class='article-item-box csdn-tracking-statistics']/h4/a/@href")
  csdn_article_link_list = preHandleData(link_list)
  # 博客文章的发表日期
  publishDate_list = page_html.xpath(
    "//div[@class='info-box d-flex align-content-center']/p/span[@class='date']/text()")  
  csdn_article_publishDate_list = preHandleData(publishDate_list)

  # 博客文章的阅读数
  csdn_article_readerCount_list = page_html.xpath(
    "//div[@class='info-box d-flex align-content-center']/p//span[last()-1][@class='read-num']/text()")
  # 博客文章的评论数
  csdn_article_commentCount_list = page_html.xpath(
    "//div[@class='info-box d-flex align-content-center']/p//span[last()][@class='read-num']/text()")
  print("csdn_article_title_list: " + str(len(csdn_article_title_list)))
  print("csdn_article_type_list: " + str(len(csdn_article_type_list)))
  print("csdn_article_link_list: " + str(len(csdn_article_link_list)))
  print("csdn_article_publishDate_list: " + str(len(csdn_article_publishDate_list)))
  print("csdn_article_readerCount_list: " + str(len(csdn_article_readerCount_list)))
  print("csdn_article_commentCount_list: " + str(len(csdn_article_commentCount_list)))
  # for i in range(0, 6):
  #   print("标题："+csdn_article_title_list[i])
  #   print("类型："+csdn_article_type_list[i])
  #   print("链接："+csdn_article_link_list[i])
  #   print("发布："+csdn_article_publishDate_list[i])
  #   print("阅读："+csdn_article_readerCount_list[i])
  #   print("评论："+csdn_article_commentCount_list[i])
  # for i in range(0, len(csdn_article_title_list)):
  #   data = [[csdn_article_type_list[i].text, csdn_article_title_list[i], csdn_article_link_list[i],
  #     csdn_article_publishDate_list[i].text, csdn_article_readerCount_list[i].text,
  #     csdn_article_commentCount_list[i].text], ]

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

def main_func():
  parseCSDNHTML()

if __name__ == '__main__':
  main_func()