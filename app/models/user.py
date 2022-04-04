from __future__ import print_function # In python 2.7
import sys
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class User(UserMixin):
    def __init__(self, uid, email, firstname, lastname, password=None, address=None):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.address = address
    
    def get_id(self):
        return (self.uid)

    def is_seller(self):
        # returns true if a user is a seller, false otherwise
        rows = app.db.execute("""
SELECT *
FROM Sellers
WHERE uid = :uid
""",
                              uid=self.uid)
        if rows:
            return True
        return False

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, uid, email, firstname, lastname
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def email_exists_update(email, uid):
        #checks if email exists for a user other than the current user (for updating email)
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email, uid != :uid
""",
                              email=email,
                              uid=uid)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            print('this is the email: ' + email, file=sys.stderr)
            print('this is the password: ' + password, file=sys.stderr)
            print('this is the firstname: ' + firstname, file=sys.stderr)
            print('this is the lastname: ' + lastname, file=sys.stderr)
            rows = app.db.execute("""
INSERT INTO Users(uid, email, firstname, lastname, password)
VALUES(DEFAULT, :email, :firstname, :lastname, :password)
RETURNING uid
""",
                                  email=email,
                                  firstname=firstname,
                                  lastname=lastname,
                                  password=generate_password_hash(password))
            
            uid = rows[0][0]
            rows_account = app.db.execute("""
INSERT INTO ACCOUNT(uid, balance)
VALUES(:uid, DEFAULT)
RETURNING *
            """,
                                    uid=uid)
            return User.get(uid)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname
FROM Users
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def get_profile(uid):
        #gets profile information
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, password, address
FROM Users
WHERE uid = :uid
""",
                            uid=uid)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def get_public(uid):
        #gets public profile information
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address
FROM Users
WHERE uid = :uid
""",
        uid=uid)
        return User(*(rows[0])) if rows else None
    
    @staticmethod
    def make_seller(uid):
        # adds the specified user to the sellers table
        try:
            app.db.execute(
                """
                INSERT INTO Sellers
                VALUES (%d)
                """ % (uid))
            return True
        except Exception:
            return False

    @staticmethod
    def get_public_seller(uid):
        rows = app.db.execute("""
SELECT Users.uid, Users.firstname, Users.email, Users.address, Seller_Reviews.rating, Seller_Reviews.comments, Seller_Reviews.votes
FROM Users, Seller_Reviews
WHERE Users.uid = Seller_Reviews.seller_id AND Users.uid = :uid
""",
        uid=uid)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def update_profile(uid, email, password, firstname, lastname, address):
        rows = app.db.execute("""
UPDATE Users
SET
    email = :email,
    firstname = :firstname,
    lastname = :lastname,
    password = :password,
    address = :address
WHERE uid = :uid
RETURNING *
""",
                                  uid=uid,
                                  email=email,
                                  firstname=firstname,
                                  lastname=lastname,
                                  password=generate_password_hash(password),
                                  address=address)

    def get_address(user):
        rows = app.db.execute(
            """
            SELECT address
            FROM Users
            WHERE uid=:uid
            """, uid=user.uid
        )
        return rows[0][0]

