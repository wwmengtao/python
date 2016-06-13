#! /usr/bin/python
# -*- coding: utf-8 -*-
import dir
import DBLab
from lxml import etree as ET
import config


def main():
    src = dir.get_src_paths(config.resources)
    for s in src:
        files = dir.get_strings_files(s)
        if files is None or len(files) == 0:
            continue
        grouped_files = group_file_by_language(files)
        merged_files = merge_file_by_language(grouped_files)
        module = dir.get_module(s)
        write_strings_to_database(merged_files, module)


def group_file_by_language(files):
    result = {}
    for f in files:
        if have_string(f):
            lang = dir.get_lang(f)
            if result.get(lang) is not None:
                result[lang].append(f)
            else:
                result[lang] = []
                result[lang].append(f)
    return result


def merge_file_by_language(grouped_files):
    merged_files = {}
    for (key, value) in grouped_files.items():
        for f in value:
            doc = ET.parse(f)
            if merged_files.get(key) is None:
                merged_files[key] = doc
            else:
                strings = doc.findall("string")
                for s in strings:
                    merged_files[key].getroot().append(s)
    return merged_files


def write_strings_to_database(merged_files, module):
    eng_doc = merged_files.get("values")
    for (key, value) in merged_files.items():
        if eng_doc is not None and key != "values":
            write_english_text_in_attrib(eng_doc, value)
            DBLab.create_table()
            DBLab.save_data(value, key, module)


def write_english_text_in_attrib(eng_doc, dest_doc):
    eng_strings = gene_name_text_dict(eng_doc)
    dest_strings = dest_doc.findall("string")
    for s in dest_strings:
        item_name = s.attrib.get("name")
        eng_text = eng_strings.get(item_name)
        if eng_text is not None:
            s.set(DBLab.cols_eng_text, eng_text)
    return dest_doc


def gene_name_text_dict(doc):
    result = {}
    strings = doc.findall("string")
    for s in strings:
        result[s.attrib.get("name")] = s.text
    return result


def have_string(f):
    xml_tree = ET.parse(f)
    root = xml_tree.getroot()
    strings = root.find("string")
    arrays = root.find("string-array")
    plurals = root.find("plurals")
    if strings is not None or arrays is not None or plurals is not None:
        return True
    return False


if __name__ == "__main__":
    main()
