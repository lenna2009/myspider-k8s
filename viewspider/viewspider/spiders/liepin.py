# -*- coding: utf-8 -*-
import scrapy
import re
from viewspider.items import *
from w3lib.html import remove_tags
from scrapy_redis.spiders import RedisSpider

class LiepinSpider(RedisSpider):
    name = 'liepin'
    #allowed_domains = ['liepin.com']
    redis_key = 'lp:url'
    """
    def start_requests(self):
        start_urls = 'https://www.liepin.com/company/020-000/'
        yield scrapy.Request(url=start_urls,callback=self.parse)
    """
    def parse(self, response):
        company_urls=response.css(".short-dd ul li")
        for per_company in company_urls:
            urls=per_company.css("div.sub-industry a")
            industry =per_company.css("span::text").extract_first("")
            for url in urls:
                per_url=url.css("a::attr(href)").extract_first("")
                company_industry = url.css("a::text").extract_first("")
                yield scrapy.Request(url=per_url,callback=self.toal_company,meta={"industry":industry,"company_industry":company_industry})

    def toal_company(self, response):
        industry=response.meta.get("company_industry")
        company_industry=response.meta.get("industry")
        per_totalpage=response.css(".addition::text").extract_first("")
        if per_totalpage:
            total_page=int(re.findall("\d+",per_totalpage)[0])
            base_url=response.url
            for page in range(total_page):
                url=base_url+"pn{}/".format(page)
                yield scrapy.Request(url,callback=self.parse1,meta={"industry":industry,"company_industry":company_industry})
        else:
            yield scrapy.Request(response.url, callback=self.parse1,meta={"industry":industry,"company_industry":company_industry})

    def parse1(self, response):
        industry=response.meta.get("company_industry")
        company_industry=response.meta.get("industry")
        companys_urls=response.css("div.company-list div.list-item")
        for company in companys_urls:
            company_url=company.css("a::attr(href)").extract_first("")
            yield scrapy.Request(company_url,callback=self.per_page,meta={"industry":industry,"company_industry":company_industry})

    def per_page(self,response):
        item = ViewspiderItem()
        item_job=ViewspiderJobItem()
        company_name=response.css(".name-and-welfare h1::text").extract_first("")
        item["company_name"]=company_name
        industry=response.meta.get("company_industry")
        item["industry"] = industry
        company_industry=response.meta.get("industry")
        item["company_industry"] = company_industry
        field=response.css("a.comp-summary-tag-dq::text").extract_first("")
        item["field"] = field
        company_address=response.css(".new-compintro li::text").extract_first("")
        item["company_address"] = company_address
        staff = response.css(".comp-summary-tag > a:nth-child(2)::text").extract_first("")
        item["staff"] = staff
        company_welfare=response.css(".comp-tag-box ul li span::text").extract()
        item["company_welfare"] = ";".join(company_welfare)
        capital=response.css(".new-compdetail > li:nth-child(3)::text").extract_first("")
        item["capital"] = capital
        company_time=response.css(".new-compdetail > li:nth-child(2)::text").extract_first("")
        item["company_time"] = company_time
        jobs = response.css("h2.job-title small::text").extract_first("")
        jobs = int(re.findall("\d+", jobs)[0])
        item["jobs"] = jobs
        yield item
        if jobs != 0:
            company_jobs = response.css("ul.sojob-list li")
            for job in company_jobs:
                item_job["company_name"] = company_name
                item_job["industry"] = industry
                item_job["company_industry"] = company_industry
                item_job["staff"] = staff
                job_title=job.css("div.job-info a.title::text").extract_first("").strip()
                item_job["job_title"] = job_title
                job_url=job.css("div.job-info a.title::attr(href)").extract_first("")
                item_job["job_url"] = job_url
                job_salary= job.css("div.job-info p.condition span.text-warning::text").extract_first("")
                item_job["job_salary"] = job_salary
                job_address=job.css("div.job-info p.condition span:nth-child(2)::text").extract_first("")
                item_job["job_address"] = job_address
                job_degree=job.css("div.job-info p.condition span:nth-child(3)::text").extract_first("")
                item_job["job_degree"] = job_degree
                job_years=job.css("div.job-info p.condition span:nth-child(4)::text").extract_first("")
                years=re.findall("\d+",job_years)
                if years != []:
                    item_job["job_years"] = int(re.findall("\d+",job_years)[0])
                else:
                    item_job["job_years"]=0
                job_time=job.css("p.time-info time:nth-child(1)::attr(title)").extract_first("")
                item_job["job_time"] = job_time
                yield item_job

        """
        item_loader = ViewspiderItemLoader(item=ViewspiderItem(), response=response)
        item_loader.add_css("company_name",".name-and-welfare h1::text")
        item_loader.add_value("industry",response.meta.get("industry"))
        item_loader.add_value("company_industry",response.meta.get("company_industry"))
        item_loader.add_css("field","a.comp-summary-tag-dq::text")
        item_loader.add_css("company_address",".new-compintro li::text")
        item_loader.add_css("staff",".comp-summary-tag > a:nth-child(2)::text")
        item_loader.add_css("company_welfare",".comp-tag-box ul li span::text")
        item_loader.add_css("jobs","h2.job-title small::text")
        item_loader.add_css("capital",".new-compdetail > li:nth-child(3)::text")
        item_loader.add_css("company_time",".new-compdetail > li:nth-child(2)::text")
        jobs = response.css("h2.job-title small::text").extract_first("")
        jobs=int(re.findall("\d+",jobs)[0])
   
        """
