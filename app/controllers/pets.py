from flask import render_template, redirect, request, session
from app import app

from app.models.pet import Pet

@app.route('/pet/<int:pet_id>')
def view_pet(pet_id):
    
    return render_template('pets/view.html', pet=Pet.get_one(pet_id))

@app.route('/pet/add') 
def get_add_pet_form():

    if 'user_id' not in session:
        return redirect('/')

    return render_template('pets/add.html')

@app.route('/pet/add', methods=['POST']) 
def add_pet():

    if 'user_id' not in session:
        return redirect('/')
    
    new_pet = {
        'name': request.form['name'],
        'type': request.form['type'],
        'age': request.form['age'],
        'hobby': request.form['hobby'],
        'favorite_snack': request.form['favorite_snack'],
        'user_id': session['user_id']
    }

    Pet.save(new_pet)

    return redirect('/dashboard')

@app.route('/pet/update/<int:id>')
def get_update_pet_form(id):

    if 'user_id' not in session:
        return redirect('/')

    return render_template('pets/update.html', pet = Pet.get_one(id))

@app.route('/pet/update', methods=['POST'])
def update_pet():

    if 'user_id' not in session:
        return redirect('/')

    Pet.update(request.form)
    return( redirect('/dashboard') ) 

@app.route('/pet/like/<int:pet_id>') 
def like_pet(pet_id):

    if 'user_id' not in session:
        return redirect('/')

    Pet.like(pet_id, session['user_id'])

    return redirect('/dashboard')

@app.route('/pet/unlike/<int:pet_id>') 
def unlike_pet(pet_id):

    if 'user_id' not in session:
        return redirect('/')

    Pet.unlike(pet_id, session['user_id'])

    return redirect('/dashboard')