from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User,Member,Notification,Comp,Family
from . import db
import json

views = Blueprint('views', __name__)


@views.route('',methods=['GET','POST'])
def home():
    print(current_user)
    return render_template("home.html",user=current_user)

@views.route('/comp_reg', methods=['GET', 'POST'])    
@login_required
def complaint_reg():
    if request.method=='POST':
        c_name = request.form.get('c_name')
        Complaint_desc = request.form.get('Complaint_desc')
        user = User.query.filter_by(id=current_user.id).first()   
        user_id=current_user.id
        status='active'
        new_comp=Notification(member_id=user.member_id,name=c_name,desc=Complaint_desc,status=status)
        db.session.add(new_comp)
        db.session.commit()








"""
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)"""


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
