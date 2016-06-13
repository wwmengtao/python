#! /usr/bin/python
# -*- coding: utf-8 -*-


import os
import os.path
import re
import config
from lxml import etree as ET


def get_strings_files(path):
    """ 获取指定路径下所有文件路径包含alues的文件

    path --> 需要查找的路径
    """
    path = os.path.expanduser(path)
    result = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for f in filenames:
            abspath = os.path.join(dirpath, f)
            if 'values' in abspath:
                result.append(abspath)
    return result


def get_lang_in_dir(dirname):
    """ 根据路径获取该语言的简写方式

    /res/values-cs/strings.xml  -->  /values-cs

    --dirname   文件的绝对路径
    """
    m = re.search('/values.*/', dirname)
    return m.group(0)


def write_string_to_db():
    resources_dir = config.resources
    trees = merge_strings_files(resources_dir)
    for key, value in trees.items():
        lang = key.strip('/')
        strings = [s for s in value.findall('string') if len(s) == 0]
        for s in strings:
            pass


def merge_strings_files(overlay):
    """ 将指定的资源按照语言合并到一个xml文件中，方便写入数据库

    将资源文件按照语言，例如中文的就全部合并到values-zh-rCN目录下的
    strings.xml文件中
    """
    trees = {}
    ET.register_namespace('xliff', "urn:oasis:names:tc:xliff:document:1.2")
    files = get_strings_files(overlay)
    for f in files:
        lang = get_lang_in_dir(f)
        xml_tree = ET.parse(f)
        if lang in trees:
            root = trees[lang].getroot()
            for child in xml_tree.getroot():
                root.append(child)
        else:
            trees[lang] = xml_tree
    return trees


def main():
    write_string_to_db()


if __name__ == "__main__":
    main()
