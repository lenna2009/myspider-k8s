# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
import re
from w3lib.html import remove_tags

class ViewspiderItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor=TakeFirst()

class ViewspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    industry = scrapy.Field()
    company_industry = scrapy.Field()
    field = scrapy.Field()
    company_address = scrapy.Field()
    staff = scrapy.Field()
    company_welfare = scrapy.Field()
    jobs = scrapy.Field()
    capital = scrapy.Field()
    company_time = scrapy.Field()

class ViewspiderJobItem(scrapy.Item):
    company_name = scrapy.Field()
    industry = scrapy.Field()
    company_industry = scrapy.Field()
    staff = scrapy.Field()
    job_title = scrapy.Field()
    job_url = scrapy.Field()
    job_salary = scrapy.Field()
    job_address = scrapy.Field()
    job_degree = scrapy.Field()
    job_years = scrapy.Field()
    job_time = scrapy.Field()

class ViewspiderMaoyanItem(scrapy.Item):
    nickName = scrapy.Field()
    cityName = scrapy.Field()
    content = scrapy.Field()
    score = scrapy.Field()
    startTime = scrapy.Field()
