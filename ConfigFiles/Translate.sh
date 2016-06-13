#!/bin/sh
#翻译工具源代码下载地址：
#repo init -u codenj:platform/manifest.git -b nj_tools;git commit -asm "将之前的翻译工具代码和新增的翻译工具代码分开存放";git push lenovo HEAD:refs/for/nj_tools

Miss(){
java -cp TranslateTool.jar com.trans.tool.TransMiss missing_translation.xml
}

Reuse(){
java -cp TranslateTool.jar com.trans.tool.TransReuse reuse_translation.xml
}

Import(){
java -cp TranslateTool.jar com.trans.tool.TransImport import_translation.xml
}

FileMerge(){
java -cp TranslateTool.jar com.trans.tool.TransFileMerge filenameFilter.xml
}

FileFilter(){
java -cp TranslateTool.jar com.trans.tool.TransFileFilter filenameFilter.xml
}

RmDupli(){
java -cp TranslateTool.jar com.trans.tool.TransRmDupli filenameFilter.xml	
}

Insert(){
java -cp TranslateTool.jar com.trans.tool.TransInsert insertTrans.xml
}

TransOnline()
{
#查询在线翻译词库
LuJing=\
/home/mengtao1/Desktop/Downloads/Temp
VALUES=$LuJing/;
rm -rf Source;rm Source.zip;
java -jar execute.jar get_string_source -r $VALUES
}
source /opt/androidsunjdk17.conf

Oprate=1
#命令选择执行
case "$Oprate" in
    1)Miss;;
    2)Reuse;;
    3)Import;;
    4)Miss;Reuse;;
    5)Reuse;Import;;
    8)Insert;;
    9)TransOnline;;
    A)FileMerge;;  
    B)FileFilter;;
    C)RmDupli;;
    D)
    file1=/home/mengtao1/localrepo/AIO_ROW/packages/apps/Settings/res/values-sr/arrays.xml
	file2=/home/mengtao1/localrepo/AIO_ROW/packages/apps/Settings/res/values-sr-rRS/arrays.xml
    java -cp TranslateTool.jar com.trans.tool.TransSrCytoLatin $file1 $file2;;
    E)python creatxlsfromxml.py;;
    F)python importxmlfromxls.py;;
esac















