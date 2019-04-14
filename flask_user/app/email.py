from threading import Thread
from flask_mail import Message
from flask import render_template,current_app
from . import mail
import os

def send_asynec_mail(app,msg):
    with app.app_context():
        mail.send(msg)

# 四个参数分别为(1.接收者邮箱地址 2.主题 3.模板 4.可变参数)
def send_mail(to,subject,template,**kwargs):
    app=current_app._get_current_object()
    msg = Message(subject=subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    #msg.body = render_template(template + '.txt', **kwargs)          # 文本内容
    msg.html = render_template(template + '.html', **kwargs)         # 文本渲染
    th=Thread(target=send_asynec_mail,args=[app,msg])
    th.start()
    return th
