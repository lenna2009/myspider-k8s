FROM python
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install  -i https://pypi.douban.com/simple/ flask
RUN pip3 install  -i https://pypi.douban.com/simple/ flask_sqlalchemy
RUN pip3 install  -i https://pypi.douban.com/simple/ pymysql
RUN pip3 install  -i https://pypi.douban.com/simple/ scrapy
RUN pip3 install  -i https://pypi.douban.com/simple/ scrapy_redis
RUN pip3 install  -i https://pypi.douban.com/simple/ fake_useragent
RUN pip3 install  -i https://pypi.douban.com/simple/ w3lib
RUN pip3 install  -i https://pypi.douban.com/simple/ redis

