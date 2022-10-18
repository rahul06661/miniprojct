from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "eward_database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .views import views
    from .auth import auth
    from .models import User,Member,Admin
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        print("_oo"*10)
        print(email)
        if Admin.query.get(int(email)) is not None:
            return Admin.query.get(int(email))
        if User.query.get(int(email)) is not None:
            return User.query.get(int(email))
        if Member.query.get(int(email)) is not None:
            return Member.query.get(int(email))
        return User.query.get(int(email))
        

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)          
        print('Created Database!')
