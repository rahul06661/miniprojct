
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User,Member,Notification,Comp,Family,Login
from werkzeug.utils import secure_filename
from . import db
import json
import datetime
import os
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
    user = User.query.filter_by(email=current_user.email).first() 
    complaints=Comp.query.filter_by(user_id=user.id).all()
    print(complaints)
    complaints_dicts={}
    for comp in complaints:
        complaints_dicts[comp.id]={
                                    'ids':comp.id,
                                    'name':comp.name,
                                    'desc':comp.desc,
                                    'status':comp.status,
                                    'remark':comp.remark,
                                    'created_on':comp.created_on,
                                    'updated_on':comp.update_on}
    return render_template("comp_view.html",user=current_user,data=complaints_dicts)

    return render_template('user_home.html',user=current_user)

@views.route('/member_home',methods=['GET','POST'])
@login_required
def member_home():
    id=current_user.id

    member_obj=Member.query.filter_by(email=current_user.email).first() 
    users_obj=User.query.filter_by(member_id=member_obj.id).all()
    user_dict={}
    for user in users_obj:
        user_dict[user.id]={
            'name':user.name,
            'vote_id':user.vote_id,
            'phone':user.phone,
            'approval':user.approval
            }

    return render_template("member_home.html", user=current_user,data=user_dict)

@views.route('/comp_reg', methods=['GET', 'POST'])    
@login_required
def complaint_reg():
    if request.method=='POST':
        c_name = request.form.get('c_name')
        Complaint_desc = request.form.get('Complaint_desc')
        user = User.query.filter_by(email=current_user.email).first()           
        remark=""
        status='active'
        file = request.files['file']
        filename = secure_filename(file.filename)
        path=os.path.join('website/static/files', filename)
        print(path)
        file.save(path)
        new_comp=Comp(member_id=user.member_id,user_id=user.id,name=c_name,desc=Complaint_desc,img_path=path,\
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
    member_obj=Member.query.filter_by(email=current_user.email).first() 
    complaints=Comp.query.filter_by(member_id=member_obj.id).all()
    print(complaints)
    complaints_dicts={}
    for comp in complaints:
        complaints_dicts[comp.id]={
                                    'ids':comp.id,
                                    'name':comp.name,
                                    'desc':comp.desc,
                                    'status':comp.status,
                                    'remark':comp.remark,
                                    'created_on':comp.created_on,
                                    'updated_on':comp.update_on}
    return render_template("comp_view.html",user=current_user,data=complaints_dicts)

@views.route('/detailcomview/<int:id>',methods=['GET','POST'])
@login_required
def detailcomview(id): 
    complaints=Comp.query.filter_by(id=id).first()
    complaints_dicts={}
    
    complaints_dicts={
            'ids':complaints.id,
            'name':complaints.name,
            'desc':complaints.desc,
            'status':complaints.status,
            'remark':complaints.remark,
            'path':complaints.img_path,
            'created_on':complaints.created_on,
            'updated_on':complaints.update_on
            }
    print(complaints.img_path)
    if request.method=='POST':        
        complaints.status='inactive'
        complaints.remark='status checked and passesd'
        complaints.updated_on=datetime.datetime.today()
        db.session.commit()

    return render_template("detail_compview.html",user=current_user,data=complaints_dicts)

@views.route('/notification',methods=['GET','POST'])
@login_required
def notification():
    if request.method=='POST':
        name=request.form.get('name')
        desc=request.form.get('descrption')
        status='active'
        file = request.files['file']
        filename = secure_filename(file.filename)
        path=os.path.join('files', filename)
        print(path)
        file.save(path)
        member_obj=Member.query.filter_by(email=current_user.email).first()
        new_notification=Notification(name=name,desc=desc,member_id=member_obj.id,status=status,img_path=path,created_on=datetime.datetime.today(),\
            update_on=datetime.datetime.today())
        db.session.add(new_notification)
        db.session.commit()
        return render_template("post_notification.html",user=current_user)
    else:
        return render_template("post_notification.html",user=current_user)








        

