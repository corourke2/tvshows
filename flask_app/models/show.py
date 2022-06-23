from flask import flash
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL

class Show:
    db = "tv_shows_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.descr = data["descr"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.creator = None
    
    @classmethod
    def all_shows(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db).query_db(query)
        all_shows = []
        for row in results:
            all_shows.append(row)
        return all_shows

    @classmethod
    def shows_with_users(cls):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        shows = []
        for row in results:
            one_show = cls(row)
            show_creator_info = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            creator = User(show_creator_info)
            one_show.creator = creator
            shows.append(one_show)
        return shows
    
    @classmethod
    def show_by_id(cls, data):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id WHERE shows.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        show = cls(row)
        show_creator_info = {
            "id" : row["users.id"],
            "first_name" : row["first_name"],
            "last_name" : row["last_name"],
            "email" : row["email"],
            "password" : row["password"],
            "created_at" : row["users.created_at"],
            "updated_at" : row["users.updated_at"]
        }
        creator = User(show_creator_info)
        show.creator = creator
        return show

    @classmethod
    def save_show(cls, data):
        query = "INSERT INTO shows (title, network, release_date, descr, created_at, updated_at, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(descr)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, descr = %(descr)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show["title"]) < 3:
            flash("Title must be at least 3 characters")
            is_valid = False
        if len(show["network"]) < 2:
            flash("Network must be at least 3 characters")
            is_valid = False
        if len(show["release_date"]) < 8:
            flash("Please enter a valid date")
            is_valid = False
        if len(show["descr"]) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False
        return is_valid