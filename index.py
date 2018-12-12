#!/usr/bin/python
# -*- coding: utf-8 -*-


import sqlite3
import jieba
import pickle

from config import db_file
from config import err_file
from config import inverted_index_file



if __name__ == '__main__':

    conn = sqlite3.connect(db_file)

    c = conn.cursor()
    c.execute("SELECT av, title FROM video")
    result = c.fetchall()
    for row in result:
        seg_list = jieba.cut_for_search(row[1])
        for w in seg_list:
            try:
                c.execute("insert into word (content) values(?)", (w,))
            except:
                pass
            c.execute("select id from word where content = ?", (w,))
            word_id = c.fetchall()[0][0]
            try:
                c.execute("insert into video_word (av, word_id) values(?, ?)", (row[0], word_id))
            except:
                pass

    c.close()
    conn.commit()



    invindex = dict()

    c = conn.cursor()
    c.execute("SELECT av, word_id FROM video_word")
    result = c.fetchall()

    for row in result:
        if row[1] not in invindex:
            invindex[row[1]] = [row[0]]
        else:
            invindex[row[1]].append(row[0])


    with open(inverted_index_file, 'wb') as f:
        pickle.dump(invindex, f)


    conn.close()