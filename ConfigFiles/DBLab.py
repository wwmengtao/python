#! /usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3


database_name = "Data.db"
table_name = "LenovoStrings"
cols_name = "name"
cols_eng_text = "eng"
cols_text = "string_text"
cols_language = "language"
cols_module = "module"
insert_or_replace_row_count = 0


def create_table():
    con = get_connection()
    cur = con.cursor()
    cur.execute("create table IF NOT EXISTS LenovoStrings (name text, eng text, string_text text, language text, module text, PRIMARY KEY ( name, eng, language) );")
    con.close()


def save_data(doc, language, module):
    con = get_connection()
    cur = con.cursor()
    strings = doc.findall("string")
    for s in strings:
        english = s.attrib.get(cols_eng_text)
        if english is not None and s is not None and len(english) > 0 and len(s) == 0:
            save_string_into_db(cur, s, language, module)
    print("%d items insert or updated." % insert_or_replace_row_count, module)
    con.commit()
    con.close()


def save_string_into_db(cursor, element, lang, module):
    global insert_or_replace_row_count
    english = element.attrib[cols_eng_text]
    text = element.text
    language = lang
    name = element.attrib[cols_name]
    cursor.execute("INSERT OR REPLACE INTO LenovoStrings values(?, ?, ?, ?, ?)", (name, english.strip('"'), text, language, module))
    insert_or_replace_row_count += cursor.rowcount


def reuse_string(name, eng, language):
    con = get_connection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    eng = eng.strip('"')
    rows = cur.execute("select * from LenovoStrings where eng=? and language=?", (eng, language))
    result = None
    for r in rows:
        if result is None:
            result = {}
            fill_result(r, result)
        elif same_name or from_settings_or_frameworks(r):
            fill_result(r, result)
    return result


def same_name(r, result):
    return r[cols_name] == result.get(cols_name)


def from_settings_or_frameworks(r):
    from_other = r[cols_module] == dir.others
    return not from_other


def fill_result(r, result):
        result[cols_text] = r[cols_text]
        result[cols_module] = r[cols_module]


def get_connection():
    return sqlite3.connect(database_name)
