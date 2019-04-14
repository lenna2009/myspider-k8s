import os
import pymysql
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    #数据库配置
    DEBUG=True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_RECORD_QUERIES = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #邮箱配置
    SSL_DISABLE = False
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    MAIL_USERNAME = '15821812790@163.com'
    MAIL_PASSWORD =  'qwea2008'
    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = '15821812790@163.com'
    FLASKY_ADMIN = '15821812790@163.com'

    @staticmethod
    def init_app():
        pass

    # 调试坏境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root@localhost:3306/test?charset=utf8'
    SQLALCHEMY_ECHO = True

    # 生产坏境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/test?charset=utf8'
    SQLALCHEMY_ECHO = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}