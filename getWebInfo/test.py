#coding=UTF-8
import os
import requests
import xlrd
import xlwt
import opeExcel
from lxml import etree
from lxml import html
from xlutils.copy import copy

def main_func():
  file_name = os.getcwd()+"\\abc.xls"
  sheetName = 'sheet10'
  sheetRows = opeExcel.create_excel_sheet(file_name, sheetName)
  print('sheetRows:'+str(sheetRows))

if __name__ == '__main__':
  main_func()