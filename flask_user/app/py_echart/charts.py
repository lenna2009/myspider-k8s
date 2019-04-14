import numpy as np
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from pyecharts import Bar,Pie,Geo,Page
import pyecharts_snapshot
import echarts_china_provinces_pypkg
import echarts_china_cities_pypkg
import echarts_china_counties_pypkg
import echarts_countries_pypkg
page=Page()
def read_mysql_and_insert(dbname):
    try:
        engine = create_engine('mysql+pymysql://root:lenna520@localhost:3306/test?charset=utf8')
        conn = engine.connect()
        data = pd.read_sql_table(dbname, conn)
    except Exception as e:
        print(e.args)
    return data
"""
lieping_data=DataFrame(read_mysql_and_insert())
industry=lieping_data.groupby(by='company_industry').size()
data_sum=lieping_data.company_industry.count()
staff=lieping_data.groupby(by='staff').size()
print(staff)
##设置柱状图的主标题与副标题
bar = Bar("行业员工数目", "员工规模")
##添加柱状图的数据及配置项
bar.add("员工/人", staff.index[1:9], staff.values[1:9],is_label_show=True,title_pos='center',mark_line=["average"], mark_point=["max", "min"],xaxis_interval=0,center=[75,50])
##生成本地文件（默认为.html文件）
bar.render("lieping01.html")
pie = Pie("招聘行业", "行业占比",title_pos='center')
pie.add("行业",industry.index,industry.values ,is_legend_show=False,is_label_show=True)
pie.render('lieping02.html')
"""
maoyan_data=DataFrame(read_mysql_and_insert('maoyan_comments'))
maoyan_data=maoyan_data.dropna()
field = maoyan_data.groupby(by='cityName').size()
# "毒液评论地区分布",
geo = Geo("毒液评论地区分布","数据来源于猫眼",title_color="#fff",title_pos="center",width=1200,height=600,background_color="#404a59")
while True:
    field = field.sort_values(ascending=False)
    info = list(zip(field.index, field.values))
    attr, value = geo.cast(info)
    try:
        geo.add("", attr,value,visual_range=[0,200],visual_text_color="#fff",symbol_size=15,is_visualmap=True)
    except ValueError as e:
        e=str(e)
        e=e.split("No coordinate is specified for ")[1]
        field=field.drop(e)
    else:
        break
#geo.render('maoyan02.html')
page.add_chart(geo)

geo1 = Geo("毒液评论地区热力图分布","数据来源于猫眼",title_color="#fff",title_pos="center",width=1200,height=600,background_color="#404a59")
while True:
    field = field.sort_values(ascending=False)
    info = list(zip(field.index, field.values))[:50]
    attr, value = geo.cast(info)
    try:
        geo1.add("", attr, value, type="heatmap", is_visualmap=True, visual_range=[0, 50], visual_text_color='#fff',
                is_more_utils=True)
    except ValueError as e:
        e=str(e)
        e=e.split("No coordinate is specified for ")[1]
        print(e)
        field=field.drop(e)
    else:
        break
page.add_chart(geo1)

##设置柱状图的主标题与副标题
bar = Bar("评论城市排行", "热门城市")
##添加柱状图的数据及配置项
bar.add("城市/数量", field.index[:20], field.values[:20],is_label_show=True,title_pos='center',mark_line=["average"], mark_point=["max", "min"],xaxis_interval=0,center=[75,50],background_color="#404a59")
page.add_chart(bar)

page.render("maoyan.html")