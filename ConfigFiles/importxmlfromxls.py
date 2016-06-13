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
import xlrd
import os,re
import shutil
import codecs

############ XML Parser Start ############
def createXmlFile(importFile):
    print("createXmlFile importFile= ",importFile)
    document = minidom.Document()  
    res = document.createElement("resources")
    res.setAttribute("xmlns:android", "http://schemas.android.com/apk/res/android")
    res.setAttribute("xmlns:xliff", "urn:oasis:names:tc:xliff:document:1.2")
    document.appendChild(res)
    wimportFile = open(importFile,'wb')
    try:
        document.writexml(wimportFile,encoding ="utf-8")  
        print("create file success = ",importFile)
    except UnicodeDecodeError:
        print("create file error = ",importFile)
    wimportFile.close()

def Indent(dom, node, indent = 0):
    # Copy child list because it will change soon
    children = node.childNodes[:]   
    # Main node doesn't need to be indented
    if indent:
        needInsert = True
        previousNode = node.previousSibling     
        if previousNode:
            if previousNode.nodeType == previousNode.TEXT_NODE:
                needInsert = False
        if needInsert:
            text = dom.createTextNode('\n' + '    ' * indent)
            node.parentNode.insertBefore(text, node)
    if children:
        # Append newline after last child, except for text nodes
        if children[-1].nodeType == node.ELEMENT_NODE:
            text = dom.createTextNode('\n' + '    ' * indent)
            node.appendChild(text)
        # Indent children which are elements
        for n in children:
            if n.nodeType == node.ELEMENT_NODE:
                Indent(dom, n, indent + 1)  

def addMapInsheet(sheet,fileMap):
    for rownum in range(sheet.nrows):
        targetFile = sheet.row_values(rownum)[3]
        if 0 == rownum:
            continue 
        if '' == targetFile: 
            continue      
        try:
            fileMap[targetFile] = fileMap[targetFile]+1
        except KeyError: 
            fileMap[targetFile] = 1
            
def  writeXmlInSheet(sheet,fileMap,targetdir,importdir):
    print("writeXml targetdir= ",targetdir)
    for rownum in range(sheet.nrows):
        if 0 == rownum:
            continue 
        targetFile = sheet.row_values(rownum)[3]
        if '' == targetFile:
            continue
        if 0 == fileMap[targetFile]:
            continue
        else:
            print("writeXml targetFile= ",targetFile)
            importFile = targetFile.replace(targetdir,importdir)
            print("importFile =",importFile)
            if 0 == os.path.exists(importFile):
                print("there is no import file=",importFile)
                #open(importFile, "wb").write(rimportFile.read())
                mkimportdir = os.path.dirname(importFile)
                print("improt dir =",mkimportdir)
                if 0 == os.path.exists(mkimportdir):
                    os.makedirs(mkimportdir)
                #writefile = open(importFile, "wb")
                #writefile.write(rimportFile.read())
                #writefile.close()
                #shutil.copy(targetFile,mkimportdir)
                createXmlFile(importFile)
            try:
                rimportFile = open(importFile, 'rb')
                xmldoc = minidom.parse(rimportFile)
            except xml.parsers.expat.ExpatError: 
                print("XML declaration not well-formed:TargetFile,=",importFile)  
                rimportFile.close
                fileMap[targetFile] = 0    
                continue;           
            rimportFile.close            
            elementTable = {}
            arrayTable = {}
            pluralsTable = {}
            parseXml(xmldoc,elementTable,arrayTable,pluralsTable)
            
            #print("start1,",xmldoc.toxml('UTF-8'))
            #write one files
            for rownumItem in range(sheet.nrows):
                if 0 == fileMap[targetFile]:
                    break     
                if targetFile == sheet.row_values(rownumItem)[3]:
                    try:
                        source_value =  sheet.row_values(rownumItem)[2].encode('utf-8')
                    except AttributeError:
                        fileMap[targetFile] =  fileMap[targetFile]-1   
                        continue 
                    #print("string type =",sheet.row_values(rownumItem)[4])                   
                    if "string" == sheet.row_values(rownumItem)[4]:
                        fileMap[targetFile] =  fileMap[targetFile]-1                   
                        writeXml(elementTable,sheet.row_values(rownumItem),xmldoc)
                        continue                        
                    if "string-array" == sheet.row_values(rownumItem)[4]:
                        fileMap[targetFile] =  fileMap[targetFile]-1
                        arrayList_list = xmldoc.getElementsByTagName("string-array")
                        for arrayList in arrayList_list:
                            element = arrayList
                            resid = arrayList.attributes["name"].value
                            try:
                                product = arrayList.attributes["product"].value
                            except KeyError:
                                product = ''
                            if resid == sheet.row_values(rownumItem)[0] and product == sheet.row_values(rownumItem)[6]: 
                                break
                        root  = xmldoc.documentElement
                        try:
                            if 1 == arrayTable[sheet.row_values(rownumItem)[0],sheet.row_values(rownumItem)[6]]:
                                #print(element)
                                item_list = element.getElementsByTagName("item")
                                for item in item_list:
                                    for itemChild in item.childNodes[0:]:                        
                                        if itemChild.nodeType == itemChild.TEXT_NODE: 
                                            if 0 != itemChild.data.find('@'):    
                                                #print(item)                                
                                                element.removeChild(item)
                                            break
                                arrayTable[sheet.row_values(rownumItem)[0],sheet.row_values(rownumItem)[6]] = 0
                        except KeyError:
                            print("there is no value in import file,value=",sheet.row_values(rownumItem)[0])
                            arrayTable[sheet.row_values(rownumItem)[0],sheet.row_values(rownumItem)[6]] = 0
                            element = xmldoc.createElement("string-array")
                            element.setAttribute("name",sheet.row_values(rownumItem)[0].encode('utf-8'))
                            root.appendChild(element)
                            #root.appendChild(xmldoc.createTextNode("\n\t"))

                        child = xmldoc.createElement("item")
                        if None != sheet.row_values(rownumItem)[2] and '' != sheet.row_values(rownumItem)[2]:
                            textNode = xmldoc.createTextNode(sheet.row_values(rownumItem)[2].encode('utf-8'))
                        else:
                            textNode = xmldoc.createTextNode(sheet.row_values(rownumItem)[1].encode('utf-8'))
                        child.appendChild(textNode)
                        element.appendChild(child)
                        #element.appendChild(xmldoc.createTextNode("\n\t"))
                        continue
                    if "plurals" == sheet.row_values(rownumItem)[4]:
                        fileMap[targetFile] =  fileMap[targetFile]-1
                        pluralsList_list = xmldoc.getElementsByTagName("plurals")
                        for plurals in pluralsList_list:
                            element = plurals
                            resid = plurals.attributes["name"].value
                            try:
                                product = plurals.attributes["product"].value
                            except KeyError:
                                product = ''
                            if resid == sheet.row_values(rownumItem)[0] and product == sheet.row_values(rownumItem)[6]: 
                                break
                        root  = xmldoc.documentElement
                        try:
                            if 1 == pluralsTable[sheet.row_values(rownumItem)[0],sheet.row_values(rownumItem)[6]]:
                                root.removeChild(element)
                                pluralsTable[sheet.row_values(rownumItem)[0].encode('utf-8'),sheet.row_values(rownumItem)[6]] = 0
                                element = xmldoc.createElement("plurals")
                                element.setAttribute("name",sheet.row_values(rownumItem)[0].encode('utf-8'))
                                root.appendChild(element)
                                #root.appendChild(xmldoc.createTextNode("\n\t"))
                        except KeyError:
                            print("there is the element in import file,name =",sheet.row_values(rownumItem)[0])
                            pluralsTable[sheet.row_values(rownumItem)[0].encode('utf-8'),sheet.row_values(rownumItem)[6]] = 0
                            element = xmldoc.createElement("plurals")
                            element.setAttribute("name",sheet.row_values(rownumItem)[0].encode('utf-8'))
                            root.appendChild(element)
                            #root.appendChild(xmldoc.createTextNode("\n\t"))
 
                        child = xmldoc.createElement("item")
                        if None != sheet.row_values(rownumItem)[2] and '' != sheet.row_values(rownumItem)[2]:
                            textNode = xmldoc.createTextNode(sheet.row_values(rownumItem)[2].encode('utf-8'))
                        else:
                            textNode = xmldoc.createTextNode(sheet.row_values(rownumItem)[1].encode('utf-8'))
                        child.setAttribute("quantity",sheet.row_values(rownumItem)[5].encode('utf-8'))
                        child.appendChild(textNode)
                        element.appendChild(child)
                        #element.appendChild(xmldoc.createTextNode("\n\t"))
                        continue                
            #print("end1,",xmldoc.toxml('UTF-8'))
            domcopy = xmldoc.cloneNode(True)
            Indent(domcopy, domcopy.documentElement)
            wimportFile = file(importFile,'wb')
            writer = codecs.lookup('utf-8')[3](wimportFile)
            try:
                domcopy.writexml(writer, encoding = 'utf-8')
                print("save file success = ",importFile)
            except UnicodeDecodeError:
                print("save file error = ",importFile)
            domcopy.unlink()
            wimportFile.close()  
            
            rimportFile = open(importFile, 'rb')
            format0 = re.compile(r'&quot;')
            format0_string = format0.sub(r'"',rimportFile.read())    
            #format1 = re.compile(r'&lt;')
            #format1_string = format1.sub(r'<',format0_string)
            #format2 = re.compile(r'&gt;')
            #format2_string = format2.sub(r'>',format1_string)
            #format3 = re.compile(r'&amp;')
            #format3_string = format3.sub(r'&',format2_string)  
            format1 = re.compile(r'&lt;xliff:g&gt;(.*)&lt;/xliff:g&gt;')
            format1_string = format1.sub(r'<xliff:g>\1</xliff:g>',format0_string)
            format2 = re.compile(r'&lt;/xliff:g&gt;(.*)&lt;xliff:g&gt;')
            format2_string = format2.sub(r'</xliff:g>\1<xliff:g>',format1_string)
            format3 = re.compile(r'&lt;xliff:g(.*)&gt;(.*)&lt;/xliff:g&gt;')
            format3_string = format3.sub(r'<xliff:g\1>\2</xliff:g>',format2_string)
            format4 = re.compile(r'\&\"<xliff:g(.*)</xliff:g>\&\"')
            format4_string = format4.sub(r'\"<xliff:g\1</xliff:g>\"',format3_string)   
            format5 = re.compile(r'&gt;(.*)&lt;/xliff:g&gt;(.*)&lt;xliff:g')
            format5_string = format5.sub(r'>\1</xliff:g>\2<xliff:g',format4_string)   
        
            rimportFile.close()
            wimportFile = open(importFile ,  'wb')
            wimportFile.write(format5_string)
            wimportFile.close() 

def parseXml(xmldoc,elementTable,arrayTable,pluralsTable):
    string_list = xmldoc.getElementsByTagName("string")
    for stringItem in string_list:
        try:
            elementTable[stringItem.attributes["name"].value,stringItem.attributes["product"].value] = stringItem
        except KeyError:
            elementTable[stringItem.attributes["name"].value,''] = stringItem
    stringarray_list = xmldoc.getElementsByTagName("string-array")
    for stringarrayItem in stringarray_list:
        try:
            arrayTable[stringarrayItem.attributes["name"].value,stringarrayItem.attributes["product"].value] = 1
        except KeyError:
            arrayTable[stringarrayItem.attributes["name"].value,''] = 1
    plurals_list = xmldoc.getElementsByTagName("plurals")
    for pluralsItem in plurals_list:
        try:
            pluralsTable[pluralsItem.attributes["name"].value,pluralsItem.attributes["product"].value] = 1
        except KeyError:
            pluralsTable[pluralsItem.attributes["name"].value,''] = 1
       
                        
def  writeXml(elementTable,rowValues,xmldoc):
    try:
        stringItem = elementTable[rowValues[0],rowValues[6]]         
        #print('There is same value,need replace value =',rowValues[0])
        if None !=rowValues[2] and ''!=rowValues[2]:
           childList = stringItem.childNodes 
           for Item in childList[0:]: 
               stringItem.removeChild(Item)
           textNode = xmldoc.createTextNode(rowValues[2].encode('utf-8'))      
           stringItem.appendChild(textNode)
    except KeyError:
        #print('There is no same value,need add value =',rowValues[0])
        root  = xmldoc.documentElement
        element = xmldoc.createElement( "string" )
        if None == rowValues[2] or '' == rowValues[2]:
            value = rowValues[1].encode('utf-8')
        else:
            value = rowValues[2].encode('utf-8')
        textNode = xmldoc.createTextNode(value)
        element.setAttribute("name",rowValues[0].encode('utf-8'))
        if None !=rowValues[6] and ''!=rowValues[6]:
            element.setAttribute("product",rowValues[6].encode('utf-8'))
        element.appendChild(textNode)
        root.appendChild(element) 

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
        reload(sys)
        sys.setdefaultencoding('utf-8')    
        '''create a workbook '''   
        configPath = os.path.abspath(os.path.join(os.curdir,"pythonconfig.xml"))
        print("configPath = ",configPath);
        configFile = open(configPath, 'rb') 
        configxmldoc = minidom.parse(configFile)  
        configFile.close()
        targetdir = getValueByTagName(configxmldoc,"targetdir")
        print("targetdir="+targetdir)
        sourcelocale = getValueByTagName(configxmldoc,"sourcelocale")
        outdir =  getValueByTagName(configxmldoc,"outdir")
        print("outdir="+outdir)
        if None == sourcelocale:
            sourceXlsPath = outdir + os.path.sep + "out.xls"
        else:
            sourceXlsPath = outdir + os.path.sep + "out_"+sourcelocale+".xls" 
        importdir = getValueByTagName(configxmldoc,"importdir")
        print("importdir="+importdir)
        
        targetlocale_list = configxmldoc.getElementsByTagName("targetlocale")
        workbook = xlrd.open_workbook(sourceXlsPath) 

        if (None != targetlocale_list) and (0!=len(targetlocale_list)):           
            for  targetlocaleItem in targetlocale_list:
                for item in targetlocaleItem.childNodes[0:]: 
                    if item.nodeType == item.TEXT_NODE:
                        targetlocale_string = item.data
                        print("targetlocaleItem="+targetlocale_string)
                        break
                try:
                    print("targetlocaleItem=1"+targetlocale_string)
                    sheet = workbook.sheet_by_name(targetlocale_string.encode('utf-8'))                              
                    fileMap ={}
                    addMapInsheet(sheet,fileMap)
                    writeXmlInSheet(sheet,fileMap,targetdir,importdir) 
                except:
                    print("targetlocaleItem=2"+targetlocale_string)
                    continue
        else:
            for sheet in workbook.sheets()[0:]:
                fileMap ={}
                addMapInsheet(sheet,fileMap)
                writeXmlInSheet(sheet,fileMap,targetdir,importdir)   
############------Program starts here---------------------------------
if __name__ == "__main__":
    main()
############------Program starts here---------------------------------
