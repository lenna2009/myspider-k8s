
from flask_login import UserMixin, AnonymousUserMixin,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request,url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
login_manager = LoginManager()

class Permission:
    #权限常量
    Follow=0x01
    Comment=0x02
    Write_Article=0x04
    Moderte_Comment=0x08
    Administrator=0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=True, unique=True)
    default = db.Column(db.Boolean, default=False)      # 只有一个角色的字段要设为True,其它都为False
    permissions = db.Column(db.Integer)                 # 不同角色的权限不同

    @staticmethod
    def insert_roles():
        roles={
            'User':(
                Permission.Follow|
                Permission.Comment|
                Permission.Write_Article,True),
            'Moderator':(
                Permission.Follow |
                Permission.Comment |
                Permission.Write_Article|
                Permission.Moderte_Comment,False),
            "Adminstrator":(
                0xff,False
            )
        }
        for i in roles:
            role=Role.query.filter_by(name=i).first()
            if role is None:
                role=Role(name=i)
                role.permissions=roles[i][0]
                role.default=roles[i][1]
                db.session.add(role)
            db.session.commit()
    def __repr__(self):
        return "(ID;{})-(用户名：{})-(编号：{})".format(self.id,self.name,self.permissions)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True, unique=True)     # 新建一个邮箱字段
    hash_password = db.Column(db.String(256))          # 模型中加入密码散列值
    confirmed = db.Column(db.Boolean, default=False)             # 邮箱令牌是否点击
    location = db.Column(db.String(64))     # 用户地址
    about_me = db.Column(db.Text())         # 用户介绍
    member_since = db.Column(db.DateTime, default=datetime.utcnow)             # 注册时间
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    @property
    def password(self):
        raise AttributeError('wrong read')

    @password.setter
    def password(self,password):
        self.hash_password=generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.hash_password,password)

    def confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})
    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'reset':self.id})
    def reset_password(self,token,newpassword):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('reset')!=self.id:
            return False
        self.password=newpassword
        db.session.add(self)
        db.session.commit()
        return True

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64),unique=True)

class Payorder(db.Model):
    __tablename__ = 'payorders'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64))
    uspay = db.Column(db.Float)
    cnhpay= db.Column(db.Float)
    payname = db.Column(db.String(64))
    bankaccount = db.Column(db.Integer)
    phone =db.Column(db.Integer)
    email = db.Column(db.String(64))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间
    product_id =db.Column(db.Integer, db.ForeignKey('product.id'))
    products = db.relationship('Product', backref=db.backref('payorder',lazy='dynamic'))

    def set_attr(self,attrs):
        for key,value in attrs.items():
            if hasattr(self,key) and key != id:
                setattr(self,key,value)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))