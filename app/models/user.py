from flask import flash
import re

from app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db_name = 'dec_22_exm_review'

class User:

    def __init__(self, data):

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']

    def serialize(self):
        pass
        
    @classmethod
    def get_all(cls):

        query = """
            SELECT
                *
            FROM
                users;
        """

        rows = connectToMySQL(cls.db_name).query_db(query) # show in debugger

        return [cls(row) for row in rows] # list comprehension

    @classmethod
    def save(cls, data):

        query = """
            INSERT INTO 
                users
                (password, first_name, last_name, email_address) 
            VALUES 
                (%(password)s, %(first_name)s, %(last_name)s, %(email_address)s);
        """

        result = connectToMySQL('dec_22_exm_review').query_db(query,data)

        return result

    @classmethod
    def get_one(cls, id):

        query  = """
            SELECT 
                * 
            FROM 
                users 

            WHERE 
                id = %(id)s;
        """

        results = connectToMySQL('dec_22_exm_review').query_db(query, {'id': id})

        return cls(results[0]) if results else None

    @classmethod
    def get_by_email(cls, email_address):

        query  = """
            SELECT 
                * 
            FROM 
                users 

            WHERE 
                email_address=%(email_address)s
        """

        results = connectToMySQL('dec_22_exm_review').query_db(query, {'email_address': email_address})

        return cls(results[0]) if results else None

    @classmethod
    def update(cls, data):

        query = """
            UPDATE 
                users 
            SET 
                first_name=%(first_name)s,
                last_name=%(last_name)s,
                email_address=%(email_address)s
            WHERE 
                id = %(id)s;
        """

        return connectToMySQL('dec_22_exm_review').query_db(query,data)

    @classmethod
    def destroy(cls, id):

        query  = """
            DELETE FROM 
                users 
            WHERE 
                id = %(id)s;
        """
        
        return connectToMySQL('dec_22_exm_review').query_db(query, {'id': id})

    @staticmethod
    def validate_registration(user): 
        is_valid = True

        if User.get_by_email(user['email_address']):
            flash("Email already taken", "register")
            is_valid = False

        if not EMAIL_REGEX.match(user['email_address']):
            flash("Invalid Email Address", "register")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False

        if user['password'] != user['password_confirm']:
            flash("Passwords need to match","register")
            is_valid = False

        if len(user['first_name']) == 0:
            flash("Enter a first name", "register")
            is_valid = False

        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid = False

        return is_valid

    @staticmethod
    def api_validate_registration(user): 
        errors = []

        if User.get_by_email(user['email_address']):
            errors.append("Email already taken")

        if not EMAIL_REGEX.match(user['email_address']):
            errors.append("Invalid Email Address")

        if len(user['password']) < 8:
            errors.append("Password must be at least 8 characters")

        if user['password'] != user['password_confirm']:
            errors.append("Passwords need to match")

        if len(user['first_name']) == 0:
            errors.append("Enter a first name")

        if len(user['last_name']) < 3:
            errors.append("Last name must be at least 3 characters")

        return errors