from flask import Flask,request,make_response,render_template,session,redirect,url_for,flash,abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from flask_login import LoginManager
from flask_moment import Moment
from config import config
from app.datas import db,login_manager
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'           # login_view设置登陆页面的端点

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app()

    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint, static_folder='static', template_folder='templates')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
