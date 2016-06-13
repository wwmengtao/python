#! /usr/bin/python
# -*- coding: utf-8 -*-
import dir
from lxml import etree as ET
import os
import shutil
import errno


compare_path = "/home/lixh11/localrepo/Translate/Trans_Pro/MoKuai/Source/Apps"
src_path = "/home/lixh11/下载/Resources_All/Apps"
dest_path = "/home/lixh11/PTBR_Reuse"
languages = "en,zh-rCN,pt-rBR"
isCreateOverlay = True


def main():
    if isCreateOverlay:
        create_overlay()
    else:
        copy_XML()


def copy_XML():
    target_dirs = get_src_paths(compare_path)
    for p in target_dirs:
        copyanything(src_path, p)


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def create_overlay():
    src = get_src_paths(compare_path)
    for s in src:
        files = dir.get_strings_files(s)
        if files is None or len(files) == 0:
            continue
        files_after_filter = filter_languages(files)
        for f in files_after_filter:
            move_res(f)


def get_src_paths(root):
    result = []
    base_paths = dir.path_has_values(root)
    for b in base_paths:
        if isCreateOverlay:
            result.append(b.replace(root, src_path))
        else:
            result.append(b.replace(root, dest_path))
    return result


def move_res(f):
    xml_tree = ET.parse(f)
    root = xml_tree.getroot()
    strings = root.find("string")
    arrays = root.find("string-array")
    plurals = root.find("plurals")
    if strings is not None or arrays is not None or plurals is not None:
        save_file = f.replace(src_path, dest_path)
        temp_path_items = save_file.split(os.sep)
        save_path = "/".join(temp_path_items[:-1])
        print(save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        xml_tree.write(save_file, xml_declaration=True, encoding="utf-8")


def filter_languages(files):
    lang_in_list = languages.split(",")
    lang_in_list = ["values-" + lang + "/" for lang in lang_in_list]
    files_after_filter = []
    for f in files:
        if "/values/" in f and f not in files_after_filter:
            files_after_filter.append(f)
        for l in lang_in_list:
            if l in f:
                files_after_filter.append(f)
    return files_after_filter


if __name__ == "__main__":
    main()
