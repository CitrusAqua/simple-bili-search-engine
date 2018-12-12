#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
import jieba
import pickle
from time import time



from config import db_file
from config import err_file
from config import inverted_index_file
from config import pagerank_file


def intersection(a, b):
    return [e for e in a if e in b]


rank = {}
def take_rank(e):
    if e not in rank:
        return 0
    return rank[e]


if __name__ == '__main__':

    start = time()



    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    cat = ''
    query = []

    for arg in sys.argv[1:]:
        if arg.startswith('category:'):
            cat = arg[9:]
            continue
        seg_list = jieba.cut_for_search(arg)
        for w in seg_list:
            c.execute("SELECT id FROM word WHERE content = ?", (w,))
            result = c.fetchall()
            if len(result) != 0:
                query.append(result[0][0])

    invindex = dict()
    with open(inverted_index_file, "rb") as f:
        invindex = pickle.load(f)



    if cat != '':
        c.execute("SELECT av FROM video WHERE cat = ? OR cat_dtl = ?", (cat, cat))
    else:
        c.execute("SELECT av FROM video")

    result = c.fetchall()
    filtered = []
    for row in result:
        filtered.append(row[0])


    for w in query:
        if w not in invindex:
            filtered = []
            break
        filtered = intersection(filtered, invindex[w])


    with open(pagerank_file, "rb") as f:
        rank = pickle.load(f)


    filtered.sort(reverse=True, key=take_rank)


    end = time()
    elp = end - start
    elp_ms = elp * 1000

    print('')
    print('--------------------------Search Result--------------------------')
    print('')
    print(len(filtered), 'result(s) got in ', format(elp_ms, '.3f'), 'ms')

    if len(filtered) > 30:
        print("Top 30 search results are showed below.")

    print('')

    print("video\t\tpagerank\t\tcategory\t\t\ttitle\n")

    for a in filtered[:30]:
        c.execute("SELECT title, cat, cat_dtl FROM video WHERE av = ?", (a,))
        r = c.fetchall()[0]
        if a not in rank:
            rnk  =0
        else:
            rnk = rank[a]
        print("av"+str(a).ljust(8,' '), '\t', rnk, '\t', r[1], '\t', r[2].ljust(14,' '), '\t', r[0])

    conn.close()
