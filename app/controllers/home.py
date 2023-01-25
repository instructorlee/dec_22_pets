from flask import render_template, redirect, request, session
from app import app

from app.models.pet import Pet
from app.models.user import User

@app.route('/')
def home():
    return render_template('home/home.html')

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('home/dashboard.html', pets=Pet.get_all(session['user_id']), user=User.get_one(int(session['user_id'])))