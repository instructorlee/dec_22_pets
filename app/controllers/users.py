from flask import session, redirect, request, flash
from app import app
from flask_bcrypt import Bcrypt

from app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/user/register', methods=['POST'])
def register():

    if not User.validate_registration(request.form):
        return redirect('/')

    User.save({
        "password": bcrypt.generate_password_hash(request.form['password']),
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email_address": request.form['email_address'],
    })

    flash ("Thank you for registering!", "register")
    return redirect('/')

@app.route('/user/login', methods=['POST'])
def login():
    
    user = User.get_by_email(request.form['email_address'])

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']): # hashed password first, password to be checked
        flash("Invalid Credentials", "login")
        return redirect('/')

    session['user_id'] = user.id

    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')