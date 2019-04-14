from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql


app = Flask(__name__)
app.debug=True
app.secret_key='lenna'
#URI形式是：dialect+driver://username:password@host:port/database，该字符串中许多部分是可选的；
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@mysql:3306/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_ECHO']=True

db=SQLAlchemy(app)

class Lieping_company(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    company_name = db.Column(db.String(128))
    industry = db.Column(db.String(128))
    company_industry = db.Column(db.String(128))
    field = db.Column(db.String(128))
    company_address = db.Column(db.String(128))
    staff = db.Column(db.String(128))
    company_welfare = db.Column(db.String(128))
    jobs = db.Column(db.Integer())
    capital = db.Column(db.String(128))
    company_time = db.Column(db.String(128))
    #jobs_id = db.relationship("Lieping_companyjobs", backref='Lieping_company')


class Lieping_companyjobs(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    company_name = db.Column(db.String(128))
    industry = db.Column(db.String(128))
    company_industry = db.Column(db.String(128))
    staff = db.Column(db.String(128))
    job_title = db.Column(db.String(128))
    job_url = db.Column(db.String(128))
    job_salary = db.Column(db.String(128))
    job_address = db.Column(db.String(128))
    job_degree = db.Column(db.String(128))
    job_years = db.Column(db.String(128))
    job_time = db.Column(db.String(128))
    #company_id = db.Column(db.Integer, db.ForeignKey('lieping_company.id'))

class Maoyan_comments(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    nickName = db.Column(db.String(128))
    cityName = db.Column(db.String(128))
    content = db.Column(db.String(128))
    score = db.Column(db.String(128))
    startTime = db.Column(db.String(128))
