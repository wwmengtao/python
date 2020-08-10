# -*- coding: utf-8 -*-
import os
import xlrd
import xlwt
from datetime import date,datetime
from pathlib import Path
from xlutils.copy import copy

# 函数判断
def create_excel_sheet(fileName, sheetName):
  fileExist = False
  sheetExist = False
  global wb_xlrd
  global wb_xlwt
  global sheetRows
  # 1.首先判断文件是否存在
  try:
    wb_xlrd = xlrd.open_workbook(fileName)  # 打开工作簿
    fileExist = True
    wb_xlwt = copy(wb_xlrd)# 将xlrd对象拷贝转化为xlwt对象
  except Exception:
    print('文件不存在：'+fileName)
    wb_xlwt = xlwt.Workbook()  # 新建一个工作簿
  # 2.判断文件中对应的sheet是否存在
  try:
    st_xlrd = wb_xlrd.sheet_by_name(sheetName)  # 获取工作簿中名称为sheetName的表格
    sheetExist = True
    sheetRows = st_xlrd.nrows  # 获取表格中已存在的数据的行数
  except Exception:
    print('sheet不存在：'+sheetName)
    wb_xlwt.add_sheet(sheetName)  # 在工作簿中新建一个表格
    sheetRows = 0
  # 3.文件或者sheet不存在，那么保存
  if fileExist == False or sheetExist == False:
    wb_xlwt.save(fileName)
  return sheetRows

#获取excel中指定sheet名称的索引
def get_sheet_index(wb_xlrd, gSheetName):
  sheetIndex = -1;
  for i in range(0, len(wb_xlrd.sheet_names())):
    sheetName = wb_xlrd.sheet_names()[i]
    # print(sheetName)
    if sheetName==gSheetName:
      sheetIndex = i
      break;
  return sheetIndex

def write_sheet_value(st_xlwt, rows_rd, value):
  Length = len(value)  # 获取需要写入数据的行数
  for i in range(0, Length):
    for j in range(0, len(value[i])):
      st_xlwt.write(i + rows_rd, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入

 # path指的是excel文件的路径;value指的是数据,是一个嵌套列表
def write_excel_xls_append(path, sheetName, value):
    wb_xlrd = xlrd.open_workbook(path)  # 打开工作簿
    st_xlrd = wb_xlrd.sheet_by_name(sheetName)  # 获取工作簿中名称为sheetName的表格
    rows_rd = st_xlrd.nrows  # 获取表格中已存在的数据的行数
    wb_xlwt = copy(wb_xlrd)  # 将xlrd对象拷贝转化为xlwt对象
    sheetIndex = get_sheet_index(wb_xlrd, sheetName)
    st_xlwt = wb_xlwt.get_sheet(sheetIndex) 
    write_sheet_value(st_xlwt, rows_rd, value)
    wb_xlwt.save(path)  # 保存工作簿

#write_excel_xls_append_all是write_excel_xls_append的增强版，可以一次性写入多组数据
def write_excel_xls_append_2(path, sheetName, list1, list2):
    wb_xlrd = xlrd.open_workbook(path)  # 打开工作簿
    st_xlrd = wb_xlrd.sheet_by_name(sheetName)  # 获取工作簿中名称为sheetName的表格
    rows_rd = st_xlrd.nrows  # 获取表格中已存在的数据的行数
    wb_xlwt = copy(wb_xlrd)  # 将xlrd对象拷贝转化为xlwt对象
    sheetIndex = get_sheet_index(wb_xlrd, sheetName)
    st_xlwt = wb_xlwt.get_sheet(sheetIndex)
    for i in range(0, len(list1)): 
      value = [[list1[i], list2[i],],]
      write_sheet_value(st_xlwt, rows_rd, value)
      rows_rd = rows_rd + 1
    wb_xlwt.save(path)  # 保存工作簿

def write_excel_xls_append_3(path, sheetName, title_list, link_list, date_list):
    wb_xlrd = xlrd.open_workbook(path)  # 打开工作簿
    st_xlrd = wb_xlrd.sheet_by_name(sheetName)  # 获取工作簿中名称为sheetName的表格
    rows_rd = st_xlrd.nrows  # 获取表格中已存在的数据的行数
    wb_xlwt = copy(wb_xlrd)  # 将xlrd对象拷贝转化为xlwt对象
    sheetIndex = get_sheet_index(wb_xlrd, sheetName)
    st_xlwt = wb_xlwt.get_sheet(sheetIndex)
    for i in range(0, len(title_list)): 
      value = [[title_list[i], link_list[i], date_list[i],],]
      write_sheet_value(st_xlwt, rows_rd, value)
      rows_rd = rows_rd + 1
    wb_xlwt.save(path)  # 保存工作簿

def write_excel_xls_append_6(path, sheetName, type_list, title_list, link_list, publishDate_list, readerCount_list, commentCount_list):
    wb_xlrd = xlrd.open_workbook(path)  # 打开工作簿
    st_xlrd = wb_xlrd.sheet_by_name(sheetName)  # 获取工作簿中名称为sheetName的表格
    rows_rd = st_xlrd.nrows  # 获取表格中已存在的数据的行数
    wb_xlwt = copy(wb_xlrd)  # 将xlrd对象拷贝转化为xlwt对象
    sheetIndex = get_sheet_index(wb_xlrd, sheetName)
    st_xlwt = wb_xlwt.get_sheet(sheetIndex)
    print("/------print size------/")
    print("title_list: " + str(len(title_list)))
    print("link_list: " + str(len(link_list)))
    print("publishDate_list: " + str(len(publishDate_list)))
    print("readerCount_list: " + str(len(readerCount_list)))
    print("commentCount_list: " + str(len(commentCount_list)))
    for i in range(0, len(title_list)): 
      value = [["", title_list[i], link_list[i], publishDate_list[i], readerCount_list[i], commentCount_list[i],],]
      write_sheet_value(st_xlwt, rows_rd, value)
      rows_rd = rows_rd + 1
    wb_xlwt.save(path)  # 保存工作簿

def read_excel():
  # 打开文件
  filename = os.getcwd()+"\\test.xls"#\\t是转义，相当于\t
  # my_file = Path("/path/to/file")
  if os.path.exists(filename):
    print("存在："+filename)
  else:
    print("不存在："+filename)
    return
  workbook = xlrd.open_workbook(filename)#如果文件不存在则报错
  # 获取所有sheet
  # print workbook.sheet_names() #[u'sheet1', u'sheet2']
  sheet2_name = workbook.sheet_names()[1]
 
  # 根据sheet索引或者名称获取sheet内容
  sheet2 = workbook.sheet_by_index(1) # sheet索引从0开始
  sheet2 = workbook.sheet_by_name('sheet2')
 
  # sheet的名称，行数，列数
  print(sheet2.name,sheet2.nrows,sheet2.ncols)
 
  # 获取整行和整列的值（数组）
  rows = sheet2.row_values(3) # 获取第四行内容
  cols = sheet2.col_values(2) # 获取第三列内容
  print(rows)
  print(cols)
 
  # 获取单元格内容
  print(sheet2.cell(1,0).value)
  print(sheet2.cell_value(1,0))
  print(sheet2.row(1)[0].value)
   
  # 获取单元格内容的数据类型
  print(sheet2.cell(1,0).ctype)

  #1. 获取指定sheet名称的sheet在excel文件中的索引 
  sheetIndex = get_sheet_index(workbook, 'sheet3')
  # print("sheet索引: "+str(sheetIndex))
  if sheetIndex < 0:
    print("not index")

  wb_xlrd = xlrd.open_workbook(filename)  # 打开工作簿
  wb_xlwt = copy(wb_xlrd)  # 将xlrd对象拷贝转化为xlwt对象
  # try:
  #   st_xlwt = wb_xlwt.get_sheet('sheet5')  # 获取转化后工作簿中的第一个表格
  # except Exception:
  #   print('异常说明')
  #   wb_xlwt.add_sheet('sheet5')
  #   wb_xlwt.save(filename)
  try:
    wb_xlrd.sheet_by_name(sheetName)
  except Exception:
    print('异常说明')
  
  # write_excel_xls(file_name, author_name, [["文章类型", "文章标题", "文章链接", "发表日期", "阅读数", "评论数"], ])


def main_func():
  read_excel()
if __name__ == '__main__':
  main_func()  