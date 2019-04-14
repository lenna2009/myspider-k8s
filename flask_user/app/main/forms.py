from flask_wtf import FlaskForm,Form
from wtforms import SubmitField,StringField,PasswordField,BooleanField,ValidationError,TextAreaField,SelectField
from wtforms.validators import Required,Length,Email,EqualTo,Regexp
from app.datas import *

class Profile(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username=StringField('username', validators=[Required(), Length(1, 64)])
    confirmed=BooleanField('confirmed')
    location = StringField('location', validators=[Required(), Length(1, 64)])
    about_me=TextAreaField('about me')
    member_since=StringField('member_since', validators=[Required(), Length(1, 64)])
    last_since = StringField('last_since', validators=[Required(), Length(1, 64)])

class EdietProfile(FlaskForm):
    username=StringField('username', validators=[Required(), Length(1, 64)])
    location = StringField('location', validators=[Required(), Length(1, 64)])
    about_me=TextAreaField('about me')
    submit=SubmitField('提交')

class PayorderForm(FlaskForm):
    account = StringField('Account', validators=[Required(), Length(1, 64)])
    product_id = SelectField('product',coerce = int)
    uspay = StringField('Ushpay', validators=[Required(), Length(1, 64)])
    cnhpay= StringField('Cnhpay', validators=[Required(), Length(1, 64)])
    payname = StringField('Payname', validators=[Required(), Length(1, 64)])
    bankaccount = StringField('BankAccount', validators=[Required(), Length(1, 64)])
    phone = StringField('Phone', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit=SubmitField('submit')



