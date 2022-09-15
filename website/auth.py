from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Member
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))


@auth.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')

        if email=='admin@gmail.com' and password=='admin':
            return render_template("admin.html", user=current_user)
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)



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
            flash('Member Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("member_register.html", user=current_user)



@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('Email')
        Name = request.form.get('Name')
        Age = request.form.get('Age')
        gender = request.form.get('gender')
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
            print(member)

            new_user = User(member_id=member.id,email=email,name=Name,age=Age, gender=gender,phone=Phone,blood_group=blood_group,\
            ward=ward,Houseno=House_Number,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

