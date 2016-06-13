'''
Created on 2012-11-5

@author: lenovo6
'''
#! /usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, getopt
import fnmatch
from xml.dom import minidom
import xml.parsers.expat
from os.path import basename, isdir
from os import listdir
import xlwt as pycel
import os,re

############ XML Parser Start ############

class xml_parser_class:
    def writexls(self,source,worksheet,targetlocale_string,workrowMap):
        print(source)
        try:
            fsock = open(source, 'rb')
            xmldoc = minidom.parse(fsock)
            fsock.close()
            string_list = xmldoc.getElementsByTagName("string")
            row = workrowMap[targetlocale_string]
            #print("start = ",row)
            if string_list != None:
                #print(row)
                for stringItem in string_list:
                    try:
                        resid = stringItem.attributes["name"].value
                    except KeyError:
                        print("there is no name in ",source)
                        continue
                    source_string = ''
                    for item in stringItem.childNodes[0:]:
                        if item.nodeType == item.ELEMENT_NODE:
                            source_string +=getxliffString(item)
                        if item.nodeType == item.TEXT_NODE:
                            source_string += item.data
                    if 0 == source_string.find('@'):
                        continue
                    row = row+1
                    #print(resid)
                    try:
                        product = stringItem.attributes["product"].value
                        print(product)
                        worksheet.write(row,6,product.encode('utf-8'))
                    except KeyError:
                        #print("there is no basevalue")
                        product = ''
                    worksheet.write(row,0,resid.encode('utf-8'))
                    worksheet.write(row,3,source.encode('utf-8'))
                    worksheet.write(row,4,"string".encode('utf-8'))
                    worksheet.write(row,1,source_string.encode('utf-8'))
            arrayList_list = xmldoc.getElementsByTagName("string-array")
            if arrayList_list != None:
                #print(row)
                for arrayList in arrayList_list:
                    resid = arrayList.attributes["name"].value
                    #print(resid)
                    arrayItemlist = arrayList.getElementsByTagName("item")
                    for arrayItem in arrayItemlist:
                        source_string = ''
                        for item in arrayItem.childNodes[0:]:
                            if item.nodeType == item.ELEMENT_NODE:
                                source_string +=getxliffString(item)
                            if item.nodeType == item.TEXT_NODE:
                                source_string += item.data
                        if 0 == source_string.find('@'):
                            continue
                        row = row+1
                        worksheet.write(row,1,source_string.encode('utf-8'))
                        try:
                            product = arrayItem.attributes["product"].value
                            print(product)
                            worksheet.write(row,6,product.encode('utf-8'))
                        except KeyError:
                            product=''
                        worksheet.write(row,0,resid.encode('utf-8'))
                        worksheet.write(row,3,source.encode('utf-8'))
                        worksheet.write(row,4,"string-array".encode('utf-8'))

            plurals_list = xmldoc.getElementsByTagName("plurals")
            if plurals_list != None:
                #print(row)
                for plurals in plurals_list:
                    resid = plurals.attributes["name"].value
                    #print(resid)
                    pluralsItemlist = plurals.getElementsByTagName("item")
                    for pluralsItem in pluralsItemlist:
                        row = row+1
                        source_string = ''
                        try:
                            product = pluralsItem.attributes["product"].value
                            print(product)
                            worksheet.write(row,6,product.encode('utf-8'))
                        except KeyError:
                            product = ''
                        try:
                            itemName = pluralsItem.attributes["quantity"].value
                            print(itemName)
                            worksheet.write(row,5,itemName.encode('utf-8'))
                        except KeyError:
                            print("there is no itemName")
                        worksheet.write(row,0,resid.encode('utf-8'))
                        worksheet.write(row,3,source.encode('utf-8'))
                        worksheet.write(row,4,"plurals".encode('utf-8'))
                        for item in pluralsItem.childNodes[0:]:
                            if item.nodeType == item.ELEMENT_NODE:
                                source_string +=getxliffString(item)
                            if item.nodeType == item.TEXT_NODE:
                                source_string += item.data
                        worksheet.write(row,1,source_string.encode('utf-8'))
            #print("end = ",row)
            workrowMap[targetlocale_string] = row
        except IOError:
            sys.exit("Error opening file", source)

def getxliffString(element):
    source_string = ''
    hasId = True
    try:
        id = element.attributes["id"].value
    except KeyError:
        id = ''
        hasId = False
    for liffitem in element.childNodes[0:]:
        if liffitem.nodeType == liffitem.TEXT_NODE:
            if (hasId):
                source_string = "<xliff:g id="+'"'+id+'"'+">"+liffitem.data+"</xliff:g>"
            else:
                source_string = "<xliff:g>"+liffitem.data+"</xliff:g>"
    print(source_string)
    return source_string

class file_traverse_class:
    def file_traverse(self,rootDir,worksheepMap,workrowMap,locales):
        parser = xml_parser_class()
        for  parent, dirnames, filenames  in  os.walk(rootDir):
            for  filename  in  filenames:
                #print  ( " parent is: "   +  parent)
                #print  ( " filename is: "   +  filename)
                absoutePath = os.path.join(parent, filename)
                #print  ( " filename with full path : "   +  absoutePath)
                for targetlocale_string in locales:
                    #print("targetlocaleItem=",targetlocale_string)
                    targetlocale_string = targetlocale_string.strip()
                    if 'en' == targetlocale_string:
                        folderName = "values"+os.path.sep+filename
                    else:
                        folderName = "values-"+targetlocale_string+os.path.sep+filename
                    #print(folderName);
                    if (absoutePath.endswith(folderName)):
                        #print("find=",targetlocale_string)
                        worksheet = worksheepMap[targetlocale_string]
                        sheeprow = parser.writexls(absoutePath,worksheet,targetlocale_string,workrowMap)
                        #print("sheep row =",sheeprow)

def getValueByTagName(configxmldoc,Tagname):
    print("Tagname = ",Tagname)
    Tagnamelist = configxmldoc.getElementsByTagName(Tagname)

    if Tagnamelist == None:
        return None

    for TagnameItem in Tagnamelist:
        for item in TagnameItem.childNodes[0:]:
            if item.nodeType == item.TEXT_NODE:
                source_string = item.data
                return source_string
    return None


def main():
        '''create a workbook '''
        configPath = os.path.abspath(os.path.join(os.curdir,"pythonconfig.xml"))
        print("configPath = ",configPath);
        configFile = open(configPath, 'rb')
        configxmldoc = minidom.parse(configFile)
        configFile.close()
        targetdir = getValueByTagName(configxmldoc,"targetdir")
        print("targetdir="+targetdir)
        outdir =  getValueByTagName(configxmldoc,"outdir")
        print("outdir="+outdir)
        sourcelocale = getValueByTagName(configxmldoc,"sourcelocale")
        # targetlocale_list = configxmldoc.getElementsByTagName("targetlocale")
        locales =  getValueByTagName(configxmldoc,"locales").split(',')

        workbook = pycel.Workbook(encoding='utf-8')
        worksheepMap ={}
        workrowMap = {}
        for targetlocale_string in locales:
            targetlocale_string = targetlocale_string.strip()
            worksheet = workbook.add_sheet(targetlocale_string.encode('utf-8'))
            worksheet.write(0,0,"Resource_ID")
            worksheet.write(0,1,"Source_Value")
            #worksheet.write(0,2,"Base_Value")
            worksheet.write(0,2,"Target_Value")
            worksheet.write(0,3,"File_Path")
            worksheet.write(0,4,"String_Type")
            worksheet.write(0,5,"Item_Name")
            worksheet.write(0,6,"product")
            worksheepMap[targetlocale_string]= worksheet
            workrowMap[targetlocale_string] = 1

        traverse = file_traverse_class()
        traverse.file_traverse(targetdir,worksheepMap,workrowMap,locales)

        if None == sourcelocale:
            out_file = outdir + os.path.sep + "out.xls"
        else:
            out_file = outdir + os.path.sep + "out_"+sourcelocale+".xls"
        print("\nOutput is saved to:", out_file)
        workbook.save(out_file)


############------Program starts here---------------------------------
if __name__ == "__main__":
    main()
############------Program starts here---------------------------------
