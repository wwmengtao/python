# -*- coding: utf-8 -*-
import os
import xlrd
import xlwt
from datetime import date,datetime
 
def read_excel():
  # 打开文件
  filename = os.getcwd()+"\\test.xls"#\\t是转义，相当于\t
  print(filename)
  workbook = xlrd.open_workbook(filename)
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
 
if __name__ == '__main__':
  read_excel()