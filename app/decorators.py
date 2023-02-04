from flask import jsonify, request, session, redirect
from functools import wraps

from app.models.user import User

def login_required(function):
    @wraps(function)

    def wrap(*args, **kwargs):

        if 'user_id' in session:

            user = User.get_one(int(session['user_id']))

            if user:
                return function(user, *args, **kwargs)

        return redirect('/')

    return wrap


"""
def create_character(name):
    return {
        'name': name,
        'can_teleport': False
    }

fred = create_character('Fred')
print ( fred )

def create_new_fantastic_character(name):
    character = create_character(name)
    character['speed'] = 50
    character['is_magical'] = False
    return character



wilma = create_new_fantastic_character('Wilma')
print( wilma )
"""