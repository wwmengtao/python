2020.06.14
1. csdn.py:获取CSDN某一个作者博客的内容
bug说明：由于获取博客文章信息的时候，文章类型(csdn_article_type_list)的长度和标题/链接长度会偶尔出现不一致，因此保存的时候文章类型统统为""

2. opeExcel.py：Excel文件的创建及读写操作
1)xlrd只能读excel表格，而xlwt只能用来创建文件并且写入内容
2)test.xls：用来解析excel表格使用的测试文档

3. opeHTML.py：用来解析HTML文件
1)*.html：用来解析HTML文件所使用的测试文档
2)函数解析
parseGityuanHTML：解析http://gityuan.com/archive/
