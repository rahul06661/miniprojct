from crypt import methods
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User,Member,Notification,Comp,Family,Admin
from . import db
import json
import datetime
views = Blueprint('views', __name__)





@views.route('',methods=['GET','POST'])
def home():
    return render_template("home.html",user=current_user)
    
"""
@views.route('/member_home',methods=['GET','POST'])
@login_required
def comp_views():   
    return render_template("member_home.html",user=current_user)
"""
@views.route('/user_home',methods=['GET','POST'])
@login_required
def user_home():
    return render_template('user_home.html',user=current_user)

@views.route('/member_home',methods=['GET','POST'])
@login_required
def member_home():
    return render_template("member_home.html", user=current_user)

@views.route('/comp_reg', methods=['GET', 'POST'])    
@login_required
def complaint_reg():
    if request.method=='POST':
        c_name = request.form.get('c_name')
        Complaint_desc = request.form.get('Complaint_desc')
        user = User.query.filter_by(id=current_user.id).first()   
        user_id=current_user.id
        remark=""
        status='active'
        print(c_name)
        print("__"*10)
        print(Complaint_desc)
        new_comp=Comp(member_id=user.member_id,user_id=current_user.id,name=c_name,desc=Complaint_desc,\
        remark=remark,status=status,created_on=datetime.datetime.today(),\
            update_on=datetime.datetime.today())
        db.session.add(new_comp)
        db.session.commit()
        return render_template("complaints.html",user=current_user)
    else:
        return render_template("complaints.html",user=current_user)


@views.route('/compview',methods=['GET','POST'])
@login_required
def compview():
    print("____444__"*10)
    print(current_user)
    com=Comp()
    complaints = Comp.query.filter(com.member_id==current_user.member_id).all()
    print(com.member_idz)
    print("Comp.member_id",Comp.member_id)
    print("current_user.member_id",current_user.member_id)
    complaints_dicts={}

    for comp in complaints:
        complaints_dicts[comp.id]={'name':comp.name,
                                    'desc':comp.desc,
                                    'status':comp.status,
                                    'remark':comp.remark,
                                    'created_on':comp.created_on,
                                    'updated_on':comp.update_on}
        print(complaints_dicts)
    return render_template("comp_view.html",user=current_user,data=complaints_dicts)

@views.route('/notification',methods=['GET','POST'])
@login_required
def notification():
    if request.method=='POST':
        name=request.form.get('name')
        desc=request.form.get('descrption')
        status='active'
        new_notification=Notification(name=name,desc=desc,member_id=current_user.id,status=status,created_on=datetime.datetime.today(),\
            update_on=datetime.datetime.today())
        db.session.add(new_notification)
        db.session.commit()
        return render_template("post_notification.html",user=current_user)
    else:
        return render_template("post_notification.html",user=current_user)