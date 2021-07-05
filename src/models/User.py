import hashlib
import os
import binascii
from flask_login import UserMixin
from sqlalchemy import func

from extensions.db import db

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String())
    profile_pic = db.Column(db.String(), nullable=True)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    firstname = db.Column(db.String(), nullable=True)
    lastname = db.Column(db.String(), nullable=True)
    info = db.Column(db.String(), nullable=True)

    room_id = db.Column(db.String(8), db.ForeignKey('room.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User {self.firstname} {self.lastname} ({self.email})>"

    def __init__(self, email, password, room):
        self.email = email
        self.password = hash_password(password)
        self.room = room

    def change_password(self, new_password):
        self.password = hash_password(new_password)

    def check_login(self, given_pw):
        return verify_password(self.password, given_pw)

    def get_id(self):
        return self.id
