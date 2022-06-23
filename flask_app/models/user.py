import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "tv_shows_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.shows = []

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate_registration(user):
        is_valid = True
        special_char = ["!", "@", "#", "$", "%", "&", "*"]
        user_in_db = User.get_by_email(user)
        if user_in_db:
            flash("Email is associated with another account")
            is_valid = False
        if len(user["first_name"]) < 3:
            flash("First name must be at least 2 characters")
            is_valid = False
        if not user["first_name"].isalpha():
            flash("First name can only contain letters")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if not user["last_name"].isalpha():
            flash("Last name can only contain letters")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address")
            is_valid = False
        if user["password"] != user["confirm_password"]:
            flash("Passwords do not match")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Passwords must be at least 8 characters")
            is_valid = False
        if not True in (char.isdigit() for char in user["password"]):
            flash("Password must contain at least one number")
            is_valid = False
        if not True in (char.isupper() for char in user["password"]):
            flash("Password must contain at least one uppercase letter")
            is_valid = False
        if not any(char in special_char for char in user["password"]):
            flash("Password must contain at least one special character: !, @, #, $, %, &, or *")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        user = User.get_by_email(user)
        if not user:
            flash("Email is not associated with an account")
            is_valid = False
        return is_valid
