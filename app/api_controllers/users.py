from flask import session, redirect, request, flash, jsonify
from app import app
from flask_bcrypt import Bcrypt

from app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/api/user/register', methods=['POST'])
def api_register():

    user_data = request.get_json()

    registration_errors = User.api_validate_registration(user_data)
    if registration_errors:
        return jsonify(
            {
                'errors': registration_errors
            }
        ), 422

    User.save({
        "password": bcrypt.generate_password_hash(user_data['password']),
        "first_name": user_data['first_name'],
        "last_name": user_data['last_name'],
        "email_address": user_data['email_address'],
    })

    return jsonify(), 200

@app.route('/api/user/login', methods=['POST'])
def api_login():
    pass

@app.route('/api/user/logout')
def api_logout():
    session.clear()
    return {}, 200