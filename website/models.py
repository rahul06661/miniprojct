from turtle import update
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    member_id=db.Column(db.String(150),db.ForeignKey('member.id'))
    email=db.Column(db.String(120),unique=True)
    name=db.Column(db.String(100))
    age=db.Column(db.Integer)
    gender= db.Column(db.String(1))   
    phone = db.Column(db.String(20))  
    blood_group=db.Column(db.String(3))
    ward = db.Column(db.Integer)
    Houseno=db.Column(db.Integer)
    password=db.Column(db.String(100))

class Member(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120))
    name=db.Column(db.String(100))
    age=db.Column(db.Integer)   
    gender= db.Column(db.String(1))
    phone = db.Column(db.String(20))
    blood_group=db.Column(db.String(3))
    ward = db.Column(db.Integer)
    password=db.Column(db.String(100))

class Notification(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    member_id=db.Column(db.String(150),db.ForeignKey('member.id'))
    name=db.Column(db.String(100))  
    desc=db.Column(db.String(100))
    status=db.Column(db.String(100))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    update_on = db.Column(db.DateTime(timezone=True), default=func.now())

class Comp(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    member_id=db.Column(db.String(150),db.ForeignKey('member.id'))
    user_id=db.Column(db.String(150),db.ForeignKey('user.id'))  
    status=db.Column(db.String(100))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    update_on = db.Column(db.DateTime(timezone=True), default=func.now())

class Family(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.String(150),db.ForeignKey('user.id'))
    name=db.Column(db.String(100))
    age=db.Column(db.Integer)
    gender= db.Column(db.String(1))
    phone = db.Column(db.String(20))
















