from flask import render_template, flash, redirect, url_for,request
from flask_login import login_user, logout_user, login_required, current_user
from ..email import send_mail
from . import main
from .. import db
from ..datas import *
import pymysql

@main.route('/',methods=['GET','POST'])
def index():
    from .forms import PayorderForm
    form=PayorderForm(request.form)
    products = db.session.query(Product).all()
    form.product_id.choices=[(p.id,p.product)for p in products]
    if request.method =="POST":
        try:
            orders=Payorder()
            #form.populate_obj(orders)
            orders.set_attr(form.data)
            db.session.add(orders)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e.args)
        return redirect(url_for('main.index'))
    return render_template('index.html',form=form)
@main.route('/datas',methods=['GET','POST'])
def get_data():
    m=request.form.get('account',None)
    return m

@main.route('/pays',methods=['GET','POST'])
@login_required
def pays():
    from .forms import PayorderForm
    form=PayorderForm()
    products = db.session.query(Product).all()
    form.product_id.choices=[(p.id,p.product) for p in products]
    if form.validate_on_submit():
        orders=Payorder()
        form.populate_obj(orders)
        db.session.add(orders)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('test.html',form=form)

@main.route('/profile/<username>',methods=['GET','POST'])
@login_required
def profile(username):
    from .forms import Profile
    form=Profile()
    user=User.query.filter_by(username=current_user.username).first()
    if user:
        form.email.data=user.email
        form.username.data=user.username
        form.confirmed.data=user.confirmed
        form.location.data=user.location
        form.about_me.data=user.about_me
        form.last_since.data=user.last_seen
        form.member_since.data=user.member_since
    return render_template('users.html',form=form)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    from .forms import EdietProfile
    form=EdietProfile()
    if form.validate_on_submit():
        current_user.location=form.location.data
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('you have update your profile')
        return redirect(url_for('main.profile',username=current_user.username))
    form.location.data=current_user.location
    form.username.data=current_user.username
    form.about_me.data=current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route("/liepingchart")
@login_required
def show_chart():
    return render_template("py_echart/ender.html",)

@main.route("/payorders")
@login_required
def pay_orders():
    """
    cnn = pymysql.connect(host="www.circlefx.cn", user="liuyuan", password="liuyuan1234", db="wordpress", port=3306,charset='utf8')
    cur = cnn.cursor()
    sql = "select * from dlhz ORDER BY id DESC"
    cur.execute(sql)
    datas = cur.fetchall()
    cnn.commit()
    cnn.close()
    #return render_template("payorders.html",items=datas)
    """
    return render_template("lieping01.html")
@main.route("/payorders01")
@login_required
def pay_orders01():
    """
    cnn = pymysql.connect(host="www.circlefx.cn", user="liuyuan", password="liuyuan1234", db="wordpress", port=3306,charset='utf8')
    cur = cnn.cursor()
    sql = "select * from dlhz ORDER BY id DESC"
    cur.execute(sql)
    datas = cur.fetchall()
    cnn.commit()
    cnn.close()
    #return render_template("payorders.html",items=datas)
    """
    return render_template("lieping02.html")


@main.route("/payorders02")
@login_required
def pay_orders02():
    return render_template("maoyan.html")
