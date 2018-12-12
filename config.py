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
    "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8",
    "Cookie": "pgv_pvi=1595419648; fts=1508473409; rpdid=oqwmxqlxqldoswqpmxixw; LIVE_BUVID=f64c0cd30f4e9d1a108daaaed17af750; LIVE_BUVID__ckMd5=4049a37a62f07cf3; buvid3=CB44F61D-0042-44B9-8F83-9C3D759F011F16834infoc; im_notify_type_896086=0; stardustvideo=1; CNZZDATA2724999=cnzz_eid%3D233565615-1508472596-https%253A%252F%252Fwww.google.com%252F%26ntime%3D1535877408; CURRENT_FNVAL=16; sid=ckl2pb4p; CURRENT_QUALITY=80; UM_distinctid=166cd0872e31d6-0c339a0528998c-b79183d-384000-166cd0872e55d6; _uuid=6E8B1EB8-5CEC-9110-9B34-EAE54ACE2A4D14003infoc; finger=edc6ecda; DedeUserID=896086; DedeUserID__ckMd5=2a904934164363dd; SESSDATA=ac382b68%2C1545139615%2C928645b1; bili_jct=bafb6cce250250fef1031d73de586121; BANGUMI_SS_22490_REC=258203; _dfcaptcha=e9450ce238e6cb41d394bb35405f05ba"
}


cache_folder = "./cache/"