#!/usr/bin/python
# -*- coding: utf-8 -*-

prog_file = 'curSegment'
db_file = 'data.db'
err_file = 'err.log'
pagerank_file = "pagerank.dat"
inverted_index_file = "index.dat"

avcount = 37795222
segment = 1000
biliav = "https://www.bilibili.com/video/av"

headers = {
    "Host": "www.bilibili.com",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8"
}


cache_folder = "./cache/"
