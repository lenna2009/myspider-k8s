# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from viewspider.data.model import Lieping_companyjobs,Lieping_company,db,Maoyan_comments
from viewspider.items import *

class ViewspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class LiepinspiderPipeline(Lieping_company):
    def __init__(self):
        super().__init__()
    def process_item(self,item,spider):
        if isinstance(item,ViewspiderItem):
            try:
                data=Lieping_company(
                    company_name=item["company_name"],industry=item["industry"],company_industry=item["company_industry"],
                    field=item["field"],company_address=item["company_address"],staff=item["staff"],company_welfare=item["company_welfare"],
                    jobs=item["jobs"],capital=item["capital"],company_time=item["company_time"])
                db.session.add(data)
                db.session.commit()
            except Exception as e:
                print("添加数据失败company:",e.args)
        return item

class LiepinspiderJobsPipeline(Lieping_companyjobs):
    def __init__(self):
        super().__init__()

    def process_item(self, item, spider):
        if isinstance(item, ViewspiderJobItem):
            try:
                data = Lieping_companyjobs(
                    company_name=item["company_name"], industry=item["industry"], company_industry=item["company_industry"],staff=item["staff"],
                    job_title=item["job_title"], job_url=item["job_url"],job_salary=item["job_salary"], job_address=item["job_address"],
                    job_degree=item["job_degree"], job_years=item["job_years"], job_time=item["job_time"]
                )
                db.session.add(data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("添加数据失败jobs:", e.args)
        return item
class Maoyan_commentsPipeline(Maoyan_comments):
    def __init__(self):
        super().__init__()

    def process_item(self, item, spider):
        if isinstance(item, ViewspiderMaoyanItem):
            try:
                data = Maoyan_comments(
                nickName=item["nickName"],cityName = item["cityName"],content = item["content"],
                score = item["score"],startTime = item["startTime"])
                db.session.add(data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("添加数据失败jobs:", e.args)
        return item
