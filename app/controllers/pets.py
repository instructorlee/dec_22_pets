import os

from flask import render_template, redirect, request, session, send_file
from app import app
from werkzeug.utils import secure_filename

from app.models.pet import Pet
from app.decorators import login_required

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pet/<int:pet_id>')
def view_pet(pet_id):

    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('pets/view.html', pet=Pet.get_one(pet_id))

@app.route('/pet/add') 
@login_required
def get_add_pet_form(user):
    return render_template('pets/add.html')

@app.route('/pet/add', methods=['POST']) 
@login_required
def add_pet(user):

    filename = "" # default

    if 'image_path' in request.files:
        file = request.files['image_path'] # grab the file
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.abspath(app.config['UPLOAD_FOLDER'] + filename))

    new_pet = {
        'name': request.form['name'],
        'type': request.form['type'],
        'age': request.form['age'],
        'hobby': request.form['hobby'],
        'favorite_snack': request.form['favorite_snack'],
        'image_path': filename,
        'user_id': user.id
    }

    Pet.save(new_pet)

    return redirect('/dashboard')


@app.route('/get_image/<int:id>')
def get_image(id):

    pet = Pet.get_one(id)
    return send_file(os.path.abspath(app.config['UPLOAD_FOLDER'] + pet.image_path), mimetype='image/jpeg')

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