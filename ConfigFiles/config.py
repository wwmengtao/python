#! /usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import tempfile
import shutil
from lxml import etree


resources = "/e/Bat_shell/Python/ConfigFiles/translation"


def get_miss_dir():
    miss_reources_dir = get_missing_xml().find('outdir').text
    miss_reources_dir = miss_reources_dir.strip()
    return miss_reources_dir


def get_missing_xml():
    return etree.parse('missing_translation.xml')


def get_reuse_result_dir():
    reuse_result_dir = get_reuse_xml().find('outdir').text
    reuse_result_dir = reuse_result_dir.strip()
    return os.path.join(reuse_result_dir, 'src')


def get_reuse_xml():
    return etree.parse('reuse_translation.xml')


def get_languages():
    langs = get_reuse_xml().find('locales').text.split(',')
    langs = ['values-' + l for l in langs]
    have_valuesen = False
    index = 0
    for i in range(len(langs)):
        if langs[i] == 'values-en':
            index = i
            have_valuesen = True
            break
    if have_valuesen:
        langs.pop(index)
        langs.append('values')
    return langs


def get_temp_path():
    tempdir = os.path.join(tempfile.gettempdir(), 'mergefiles')
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)
    os.makedirs(tempdir)
    return tempdir


def is_find_miss_use_english():
    doc = get_missing_xml()
    baselocale = doc.find('baselocale').text
    return baselocale is None or baselocale == "en"


def main():
    print(is_find_miss_use_english())


if __name__ == "__main__":
    main()
