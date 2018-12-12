#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import re
import time
import sqlite3
import threadpool


from config import prog_file
from config import db_file
from config import avcount
from config import segment
from config import biliav
from config import headers
from config import err_file
from config import cache_folder


request_interval = 0



video_cmds = []
ref_cmds = []

def getVideo(av):

    url = biliav + str(av)

    try:

        s = requests.Session()
        s.mount('https://', HTTPAdapter(max_retries=5))
        res = s.get(url, headers=headers).text


        soup = BeautifulSoup(res)

        err = soup.find("div", {"class": "error-body"})
        if err is not None:
            print(av, "Not exist.")
            return

        with open(cache_folder + str(av) + ".html", "w", encoding="utf-8") as f:
            f.write(res)

        title = soup.find("h1")['title']
        span = soup.find("span", {"class": "a-crumbs"})
        c = span.find_all("a", {"target": "_blank"})
        cat = c[0].text
        cat_dtl = c[1].text

        video_cmds.append((av, title, cat, cat_dtl))

        rel = soup.find_all("div", {"class": "pic-box"})
        for e in rel:
            pattern = re.compile(r'av\d+')
            href = e.a['href']
            ref_av = pattern.findall(href)[0][2:]
            ref_cmds.append((av, ref_av))

        print(av, title)

    except:
        print(av, "Error")
        with open(err_file, "a") as f:
            f.write("Failed when fetching av" + str(av)+'\n')



if __name__ == '__main__':

    curSeg = int()
    with open(prog_file, "r") as f:
        curSeg = int(f.read())

    try:

        conn = sqlite3.connect(db_file)

        pool = threadpool.ThreadPool(12)

        seg_count = avcount/segment
        for i in range(curSeg, int(seg_count)):

            threqs = threadpool.makeRequests(
                getVideo,
                range(i*segment+1, (i+1)*segment+1)
                )
            for req in threqs:
                pool.putRequest(req)

            pool.wait()

            print("Commiting...")

            cursor = conn.cursor()

            for e in video_cmds:
                try:
                    cursor.execute(
                        '''
                        insert into video (av, title, cat, cat_dtl)
                        values (?, ?, ?, ?)
                        ''',
                        e)
                except Exception as e:
                    with open(err_file, "a") as f:
                        f.write("Error occured when inserting into table video\n\t" +
                            str(e) +
                            "\n\tIn segment " + str(curSeg) + '\n')
            for e in ref_cmds:
                try:
                    cursor.execute('insert into ref (av, ref_av) values (?, ?)', e)
                except Exception as e:
                    with open(err_file, "a") as f:
                        f.write("Error occured when inserting into table ref\n\t" +
                            str(e) +
                            "\n\tIn segment " + str(curSeg) + '\n')

            cursor.close()
            conn.commit()

            print("Segment", curSeg, "Done.")

            video_cmds = []
            ref_cmds = []

            curSeg += 1

            with open(prog_file, "w") as f:
                f.write(str(curSeg))

    except Exception as e:
        print(e)

    finally:
        conn.close()

