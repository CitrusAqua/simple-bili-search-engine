#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os
import shutil

from config import prog_file
from config import db_file
from config import cache_folder

if __name__ == '__main__':

    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(
        '''
        create table video (
            av integer primary key,
            title varchar(160) not null,
            cat varchar(6),
            cat_dtl varchar(20)
        )
        '''
    )
    cursor.execute(
        '''
        create table ref (
            av integer references video(av),
            ref_av integer references video(av),
            primary key (av, ref_av)
        )
        '''
    )

    cursor.execute(
        '''
        create table word (
            id integer primary key autoincrement,
            content varchar(40) not null unique
        )
        '''
    )
    cursor.execute(
        '''
        create table video_word (
            av integer references video(av),
            word_id integer references word(id),
            primary key (av, word_id)
        )
        '''
    )

    #cursor.execute('create table invindex (id int primary key, cont varchar(160))')

    cursor.close()
    conn.commit()

    with open(prog_file, "w") as f:
        f.write('0')

    if os.path.exists(cache_folder):
        shutil.rmtree(cache_folder)
    os.makedirs(cache_folder)