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
 

# 爬虫实战: 爬取CSDN博客的所有博客文章链接
 
# 第1页: https://blog.csdn.net/cnds123321/article/list/1
# 第2页: https://blog.csdn.net/cnds123321/article/list/2
# 第3页: https://blog.csdn.net/cnds123321/article/list/3
# 故可以得出公式: url="https://blog.csdn.net/"+author_name+"/article/list/"+page_index
# author_name指的是博主的名字,page_index指的是页码当前是第几页

def getCSDNAuthorInfo():
    # 请求头，以Chrome浏览器为例，可以在地址框中输入"about:version"，里面有header信息
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    # 博主名字
    author_name = input("请输入博主的名字: ")
    # 博主博文页数
    page_num = 999999
    # page_num = int(input("请输入博客页数: "))
    # Excel文件名称
    file_name = os.getcwd()+"\CSDN_articles.xls"
    # 写入表头数据
    headerData = [["文章类型", "文章标题", "文章链接", "发表日期", "阅读数", "评论数"], ]
    opeExcel.create_excel_sheet(file_name, author_name)
    opeExcel.write_excel_xls_append(file_name, author_name, headerData)
    # 循环每页
    allNumber = 0#文章总数
    for index in range(1, page_num + 1):
        # 拼接URL
        page_url = "https://blog.csdn.net/" + author_name + "/article/list/" + str(index)
        # 发送请求,获取响应
        response = requests.get(page_url, headers=header).content
        # 将HTML源码字符串转换尘土HTML对象
        page_html = etree.HTML(response)
        # 博客文章的标题
        title_list = html.fromstring(response.decode()).xpath(
            "//div[@class='article-item-box csdn-tracking-statistics']/h4/a/text()")
        if len(title_list) == 0:
            print(author_name + "文章获取完毕，共计文章数目:"+str(allNumber))
            allNumber = 0
            break;
        # 处理换行问题
        csdn_article_title_list = opeHTML.preHandleData(title_list)
        allNumber = allNumber + len(csdn_article_title_list)
        # 博客文章的类型
        type_list = page_html.xpath("//div[@class='article-item-box csdn-tracking-statistics']/h4/a/span/text()")
        csdn_article_type_list = opeHTML.preHandleData(type_list)
        # 博客文章的链接
        csdn_article_link_list = page_html.xpath("//div[@class='article-item-box csdn-tracking-statistics']//h4//a/@href")
        # 博客文章的发表日期
        publishDate_list = page_html.xpath(
          "//div[@class='info-box d-flex align-content-center']/p/span[@class='date']/text()")  
        csdn_article_publishDate_list = opeHTML.preHandleData(publishDate_list)
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

        # 将数据保存到excel表格中
        for i in range(0, len(csdn_article_title_list)):
          data = [["", csdn_article_title_list[i], csdn_article_link_list[i],
            csdn_article_publishDate_list[i], csdn_article_readerCount_list[i],
            csdn_article_commentCount_list[i]], ]
            # data = [["", csdn_article_title_list[i], csdn_article_link_list[i],
            #  "", "",
            #  ""], ]
            # print("正在保存: "+csdn_article_title_list[i]+"......")
          opeExcel.write_excel_xls_append(file_name, author_name, data)
    

def main_func():
    getCSDNAuthorInfo()

if __name__ == '__main__':
  main_func()