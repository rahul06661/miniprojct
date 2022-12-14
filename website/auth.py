from flask import Blueprint, render_template, request, flash, redirect, url_for
import flask
from .models import User,Member,Comp,Notification,Login
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import views
auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))

@auth.route('/ad')
def adm():
    return render_template("admin.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        log=Login.query.filter_by(email=email).first()
        print(log)
        if log:
            if check_password_hash(log.password,password):
                if log.utype=='A':
                    login_user(log,remember=True)
                    print("################",current_user)
                    #return render_template("admin.html", user=current_user)
                    return redirect(url_for('auth.adm', user=current_user))
                    #return redirect('ad',user=current_user)
                elif log.utype=='m':
                    login_user(log,remember=True)
                    member_obj=Member.query.filter_by(email=log.email).first() 
                    print(member_obj.id)
                    #complaints=Comp.query.filter_by(=log.email)
                    complaints=Comp.query.filter_by(member_id=member_obj.id).all()
                    print("__"*100)
                    print(complaints)
                    return redirect(url_for('views.member_home',user=current_user))                           
                else:
                    login_user(log,remember=True) 
                    member_obj=User.query.filter_by(email=log.email).first() 
                    print(member_obj.id)
                    #complaints=Comp.query.filter_by(=log.email)
                    notifications=Notification.query.filter_by(member_id=member_obj.id).all()
                    notification_dict={}
                    for notifi in notifications:
                        notification_dict[notifi.name]=notifi.desc   
                       
                    return render_template("user_home.html",user=current_user,data=notification_dict)
            else:
                flash('incorrect username or password')
        else:
            flash('incorrect username or password')
    else:
        return render_template("login.html",user=current_user)
    return render_template("login.html",user=current_user)


@auth.route('/sign-up_member', methods=['GET', 'POST'])
def mem_signup():
    if request.method == 'POST':
        email = request.form.get('Email')
        Name = request.form.get('Name')
        Age = request.form.get('Age')
        gender = request.form.get('gender')
        Phone = request.form.get('Phone')
        blood_group=request.form.get('Group')
        ward=request.form.get('Ward')
        password1 ='admin1234'       
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')       
        else:
            new_user = Member(email=email,name=Name,age=Age, gender=gender,phone=Phone,blood_group=blood_group,\
            ward=ward,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            log_data=Login(email=email,password=generate_password_hash(password1, method='sha256'),utype='m')
            db.session.add(log_data)
            db.session.commit()

            flash('Member Account created!', category='success')
            return render_template("admin.html", user=current_user)
    return render_template("member_register.html", user=current_user)



@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('Email')
        Name = request.form.get('Name')
        Age = request.form.get('Age')
        gender = request.form.get('gender')
        vote_id = request.form.get('vote_id') 
        job = request.form.get('job')
        tp = request.form.get('tp')
        Phone = request.form.get('Phone')
        blood_group=request.form.get('Group')
        ward=request.form.get('Ward')
        House_Number = request.form.get('House Number')
        password1 = request.form.get('Pwd')
        password2 = request.form.get('Rpwd')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            member = Member.query.filter_by(ward=ward).first()
            new_user = User(member_id=member.id,email=email,name=Name,age=Age, gender=gender,phone=Phone,\
                vote_id=vote_id,job=job,tax_payer=tp,approval=False,\
                blood_group=blood_group,\
            ward=ward,Houseno=House_Number,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            log_data=Login(email=email,password=generate_password_hash(password1, method='sha256'),utype='u')
            db.session.add(log_data)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            logout_user()
            return redirect(url_for('auth.signin'))  
    return render_template("sign_up.html", user=current_user)

