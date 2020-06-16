#coding=UTF-8
import os
import requests
import xlrd
import xlwt
import opeExcel
import opeHTML
from lxml import etree
from lxml import html
from xlutils.copy import copy

def getCSDNAuthorInfo():
    #下列为CSDN博客页面的xpath，例如https://blog.csdn.net/luoshengyang/article/list/1
    type_xpath = "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/span/text()"
    title_xpath = "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/text()"
    link_xpath = "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/@href"
    publishDate_xpath = "//div[@class='info-box d-flex align-content-center']/p/span[@class='date']/text()"
    readerCount_xpath = "//div[@class='info-box d-flex align-content-center']/p//span[last()-1][@class='read-num']/text()"
    commentCount_xpath = "//div[@class='info-box d-flex align-content-center']/p//span[last()][@class='read-num']/text()"
    # 写入Excel文件的表头数据，即第一行数据
    headerData = [["文章类型", "文章标题", "文章链接", "发表日期", "阅读数", "评论数"], ]    
    # 博主名字
    author_name = input("请输入博主的名字: ")
    # 博主博文页数
    page_num = 999999
    # page_num = int(input("请输入博客页数: "))
    # Excel文件名称
    file_name = os.getcwd()+"\CSDN_articles.xls"

    opeExcel.create_excel_sheet(file_name, author_name)
    opeExcel.write_excel_xls_append(file_name, author_name, headerData)
    # 总体数组
    title_sum = []
    link_sum = []
    publishDate_sum = []
    type_sum = []
    readerCount_sum = []
    commentCount_sum = []
    for index in range(1, page_num + 1):
        # 拼接URL
        page_url = "https://blog.csdn.net/" + author_name + "/article/list/" + str(index)
        page_html = opeHTML.getEtreeHTML(page_url)
        # 博客文章的标题
        title_list = opeHTML.parseEtreeHTML(page_html, title_xpath)
        if len(title_list) == 0:
          break;
        # 博客文章的链接
        link_list = opeHTML.parseEtreeHTML(page_html, link_xpath)
        # 博客文章的发布日期
        publishDate_list = opeHTML.parseEtreeHTML(page_html, publishDate_xpath)
        # 博客文章的类型
        type_list = opeHTML.parseEtreeHTML(page_html, type_xpath)
        # 博客文章的阅读数
        readerCount_list = opeHTML.parseEtreeHTML(page_html, readerCount_xpath)
        # 博客文章的评论数
        commentCount_list = opeHTML.parseEtreeHTML(page_html, commentCount_xpath)
        # 将所有内容存放到一个总的数组中
        title_sum.extend(title_list)
        link_sum.extend(link_list)
        publishDate_sum.extend(publishDate_list)
        type_sum.extend(type_list)
        readerCount_sum.extend(readerCount_list)
        commentCount_sum.extend(commentCount_list)
        # #数据写入
        # opeExcel.write_excel_xls_append_6(file_name, author_name, 
        # type_list, title_list, link_list, publishDate_list, readerCount_list, commentCount_list)
        # allNumber = len(title_list) + allNumber
    if len(title_sum) > 0:
      #数据写入
      opeExcel.write_excel_xls_append_6(file_name, author_name, 
        type_sum, title_sum, link_sum, publishDate_sum, readerCount_sum, commentCount_sum)
      print(author_name + "文章获取完毕，共计文章数目:"+str(len(title_sum)))

def main_func():
    getCSDNAuthorInfo()

if __name__ == '__main__':
  main_func()