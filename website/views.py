
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User,Member,Notification,Comp,Family,Login
from . import db
import json
import datetime
views = Blueprint('views', __name__)


@views.route('',methods=['GET','POST'])
def home():
    return render_template("home.html",user=current_user)
    
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
        user = User.query.filter_by(email=current_user.email).first()           
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
                'created_on':complaints.created_on,
                'updated_on':complaints.update_on
            }
    if request.method=='GET':
        return render_template("detail_compview.html",user=current_user,data=complaints_dicts)
    if request.method=='POST':       
        complaints.remark=request.form.get('Remark')
        complaints.status= request.form.get('Status')
        complaints.updated_on=datetime.datetime.today()
        db.session.commit()
        return render_template("comp_view.html",user=current_user,data=complaints_dicts)

    

@views.route('/notification',methods=['GET','POST'])
@login_required
def notification():
    if request.method=='POST':
        name=request.form.get('name')
        desc=request.form.get('descrption')
        status='active'
        member_obj=Member.query.filter_by(email=current_user.email).first()
        new_notification=Notification(name=name,desc=desc,member_id=member_obj.id,status=status,created_on=datetime.datetime.today(),\
            update_on=datetime.datetime.today())
        db.session.add(new_notification)
        db.session.commit()
        return render_template("post_notification.html",user=current_user)
    else:
        return render_template("post_notification.html",user=current_user)

