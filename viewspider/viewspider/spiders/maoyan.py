# -*- coding: utf-8 -*-
import scrapy
from datetime import timedelta
import datetime
import json
from urllib.parse import quote
from viewspider.items import *
from scrapy_redis.spiders import RedisSpider

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    redis_key = 'maoyan:url'
    allowed_domains = ['maoyan.com']
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        # 修改这里的类名为当前类名
        super(MaoyanSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://m.maoyan.com/mmdb/comments/movie/42964.json?_v_=yes&offset=0&startTime={}".format(quote(now_time))
        yield scrapy.Request(url, callback=self.parse)
    def parse(self, response):
        item=ViewspiderMaoyanItem()
        next_time=response.body.decode("utf8")
        cmts=json.loads(next_time).get('cmts',"未找到")
        for cmt in cmts:
            item['nickName'] = cmt.get("nickName",None)
            item["cityName"] = cmt.get("cityName",None)
            item["content" ] = cmt.get("content",None)
            item["score"]  = cmt.get("score",None)
            item["startTime"] = cmt.get("startTime", None)
        yield item
        start_time=cmts[14].get("startTime",None)
        end_time = "2018-11-09 00:00:00"
        if start_time:
            start_time=datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")+timedelta(seconds=-10)
            start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
            if start_time > end_time:
                url = "https://m.maoyan.com/mmdb/comments/movie/42964.json?_v_=yes&offset=15&startTime={}".format(quote(start_time))
                yield scrapy.Request(url, callback=self.parse)

