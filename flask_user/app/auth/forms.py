from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,BooleanField,ValidationError,TextAreaField,SelectField
from wtforms.validators import Required,Length,Email,EqualTo,Regexp
from app.datas import *

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username=StringField('username', validators=[Required(), Length(1, 64)])
    password=PasswordField('password',validators=[Required(),EqualTo('password2',message='password must match')])
    password2=PasswordField('Confrim password',validators=[Required()])
    submit=SubmitField('提交')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already use')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('password',validators=[Required()])
    remember_me=BooleanField('keep me logged in')
    submit=SubmitField('登陆')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[Required(),
                                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('New Password',
                             validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')
