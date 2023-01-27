from flask import render_template, redirect, request, session, jsonify
from app import app

from app.models.pet import Pet

@app.route('/api/pet')
def api_all_pets():

    if 'user_id' not in session:
        return {}, 401

    return jsonify( [ pet.serialize() for pet in Pet.get_all() ] ), 200 # list comprehension

@app.route('/api/pet/<int:pet_id>')
def api_view_pet(pet_id):

    pet = Pet.get_one(pet_id)
    return jsonify(pet.serialize() if pet else {}), 200

@app.route('/api/pet/add', methods=['POST']) 
def api_add_pet():

    if 'user_id' not in session:
        return {}, 401

    data = request.get_json()
    
    new_pet = {
        'name': data['name'],
        'type': data['type'],
        'age': data['age'],
        'hobby': data['hobby'],
        'favorite_snack': data['favorite_snack'],
        'user_id': session['user_id']
    }

    return Pet.get_one(Pet.save(new_pet)).serialize(), 201

@app.route('/api/pet/update', methods=['POST']) 
def api_update_pet():

    if 'user_id' not in session:
        return {}, 401

    data = request.get_json()
    
    new_pet = {
        'id': data['id'],
        'name': data['name'],
        'type': data['type'],
        'age': data['age'],
        'hobby': data['hobby'],
        'favorite_snack': data['favorite_snack'],
        'user_id': session['user_id']
    }

    Pet.update(new_pet)

    return Pet.get_one(data['id']).serialize(), 200

@app.route('/api/user/delete/<int:pet_id>')
def api_delete_pet(pet_id):

    Pet.destroy(pet_id)
    return {}, 200

@app.route('/api/pet/like/<int:pet_id>') 
def api_like_pet(pet_id):

    if 'user_id' not in session:
        return {}, 401

    Pet.like(pet_id, session['user_id'])

    return {}, 201

@app.route('/api/pet/unlike/<int:pet_id>') 
def api_unlike_pet(pet_id):

    if 'user_id' not in session:
        return {}, 401

    Pet.unlike(pet_id, session['user_id'])

    return {}, 201