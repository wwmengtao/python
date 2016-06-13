#! /usr/bin/python
# -*- coding: utf-8 -*-

import dir
import DBLab
from lxml import etree as ET
import os
import config


def main():
    reuse_string_from_db()


def reuse_string_from_db():
    missing_files = get_missing_files()
    reuse_result = get_reuse_files()
    for (key, value) in missing_files.items():
        lang = dir.get_lang(value)
        if lang == "values":
            continue
        missing_file = ET.parse(value)
        reuse_file = None
        reuse_file_path = reuse_result.get(key)
        if reuse_file_path is None:
            reuse_file = ET.parse('template.xml')
        else:
            print(reuse_file_path)
            reuse_file = ET.parse(reuse_file_path)
        missing_strings = missing_file.findall("string")
        reuse_string_in_miss(reuse_file, missing_strings, lang)
        save_reuse_file(reuse_file, value)


def reuse_string_in_miss(reuse_file, missing_strings, lang):
    for s in missing_strings:
        if len(s) == 0 and s.text is not None:
            name = s.attrib.get("name")
            is_reused = get_xmlelement_by_name(reuse_file, name)
            if not is_reused:
                eng = s.text
                result = DBLab.reuse_string(name, eng, lang)
                if result is not None:
                    s.text = result.get(DBLab.cols_text)
                    reuse_file.getroot().append(s)


def save_reuse_file(reuse_file, value):
    if reuse_file.find("string") is not None:
        save_path = reuse_file_save_path(value)
        save_path_dir = os.path.dirname(save_path)
        if not os.path.exists(save_path_dir):
            os.makedirs(save_path_dir)
        reuse_file.write(save_path, encoding="UTF-8")


def reuse_file_save_path(file_path):
    missing_file_path = config.get_miss_dir()
    reuse_result_path = config.get_reuse_result_dir()
    result = file_path.replace(missing_file_path, reuse_result_path)
    return result



def get_missing_files():
    missing_file_path = config.get_miss_dir()
    return get_files(missing_file_path)


def get_reuse_files():
    reuse_result_path = config.get_reuse_result_dir()
    return get_files(reuse_result_path)


def get_files(path):
    result = {}
    src = dir.get_src_paths(path)
    for s in src:
        files = dir.get_strings_files(s)
        for f in files:
            key = f.strip(path)
            result[key] = f
    return result


def get_xmlelement_by_name(element_tree, name):
    return element_tree.findall(".//*[@name='%s']" % name)


if __name__ == "__main__":
    main()
