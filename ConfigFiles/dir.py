#! /usr/bin/python
# -*- coding: utf-8 -*-
import os


framework = "framework"
settings = "Settings"
others = "others"


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


def get_src_paths(root):
    result = []
    base_paths = path_has_values(root)
    for b in base_paths:
        result.append(b)
    return result


def get_lang(path):
    splited_path = path.split(os.sep)
    for s in splited_path:
        if s.find("values") is 0:
            return s


def get_module(path):
    frameworks_path = "/frameworks/base/core"
    settings_path = "/Settings/"
    if path.find(frameworks_path) > 0:
        return framework
    elif path.find(settings_path) > 0:
        return settings
    else:
        return others
