from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from ..email import send_mail
from . import auth
from .. import db
from ..datas import User

@auth.route('/login/',methods=['GET','POST'])
def login():
    from app.auth.forms import LoginForm
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('账户或者密码错误请重新输入')
    return render_template('login.html',form=form)
@auth.route('/register', methods=['GET', 'POST'])
def register():
    from app.auth.forms import RegistrationForm
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)  # 新添加一个用户到数据库中
        db.session.add(user)
        db.session.commit()
        token = user.confirmation_token()                            # 产生一个令牌
        send_mail(user.email, '请确认您的帐号', 'confirm', user=user, token=token)   # 发送邮件
        flash('有一封确认邮件已经发往您的邮箱，请登录邮箱确认')
        return redirect(url_for('auth.login'))    # 这一步一直有问题，无法重定向，直接跳到下面去了
    else:
        return render_template('register.html', form=form)
@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.login'))          # 重复点击邮箱的令牌
    if current_user.confirm(token):
        flash('感谢您的确认')
    else:
        flash('链接已经失效或者过期')
    return redirect(url_for('auth.login'))

@auth.before_app_request          # 用户已登陆、用户帐号还未确认、请求的的端点不在auth认证蓝本中
def before_request():
    if current_user.is_authenticated:
        current_user.ping()              # 在每次请求前刷新上次访问时间
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')      # 如果当前是匿名帐号活着已经确认，直接返回首页，否则显示未确认
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')

@auth.route('/resend_email')
@login_required
def resend_email():
    token = current_user.confirmation_token()
    send_mail(current_user.email, '确认您的帐号', 'confirm', user=current_user, token=token)
    flash('有一封确认邮件已经发往您的邮箱，请登录邮箱确认')
    return redirect(url_for('main.index'))

@auth.route('/editpassword/',methods=['GET','POST'])
@login_required
def edit_password():
    from app.auth.forms import ChangePasswordForm
    form=ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password=form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已修改')
            return 'you have change your word'
        else:
            return 'you have not change your word'
    return render_template('change_password.html', form=form)

@auth.route('/reset',methods=['GET','POST'])
def password_reset():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    from app.auth.forms import PasswordResetRequestForm
    form=PasswordResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            token=user.generate_reset_token()
            send_mail(user.email, 'Reset your password', 'restpasword_mail', user=user, token=token)  # 发送邮件
            flash('a reset mail to you')
    return render_template('reset_password.html',form=form)

#密码重置验证
@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset_confirm(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    from app.auth.forms import PasswordResetForm
    form=PasswordResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user.reset_password(token,form.password.data):
            flash('密码已修改')
            return 'you have  change your password'
        else:
            return 'you have not change your password'
    return render_template('reset_password.html',form=form)