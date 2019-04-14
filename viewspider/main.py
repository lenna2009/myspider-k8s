from scrapy.cmdline import execute
import os
import sys
from viewspider.data.model import *
import time
import datetime
import redis
from urllib.parse import quote


try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print("错误：",e.args)

r = redis.Redis(host='redis',port=6379, decode_responses=True)

now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#url = "https://m.maoyan.com/mmdb/comments/movie/42964.json?_v_=yes&offset=0&startTime={}".format(quote(now_time))
urls = 'https://www.liepin.com/company/020-000/'
r.lpush("lp:url",urls)
print(r.llen("lp:url"))
print(r.lrange("lp:url",0,-1))
execute(["scrapy","crawl","liepin"])
#execute(["scrapy","crawl","maoyan"])
"""
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print("错误：",e.args)
"""