#! /usr/bin/python
# -*- coding: utf-8 -*-
import os


def get_strings_files(dir):
    """ 获取指定路径下所有文件路径包含values的文件
    """
    path = get_path(dir)
    if len(path) > 0:
        result = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                abspath = os.path.join(dirpath, f)
                if 'values' in abspath:
                    result.append(abspath)
        return result


def path_has_values(root):
    if len(root) > 0:
        result = []
        for (dirpath, dirnames, filenames) in os.walk(root):
            for f in filenames:
                abspath = os.path.join(dirpath, f)
                if 'values' in abspath:
                    items = dirpath.split(os.sep)
                    abspath = '/'.join(items[:-2])
                    if abspath not in result:
                        result.append(abspath)
        return result


def get_path(path):
    expand_path = os.path.expanduser(path)
    if not os.path.exists(expand_path):
        print "目录不存在"
        return ""
    else:
        return path
