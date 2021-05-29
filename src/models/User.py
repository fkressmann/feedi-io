from extensions.db import db
from sqlalchemy.dialects.postgresql import UUID



class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(), primary_key=True, unique=True)
    password = db.Column(db.String())

    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    info = db.Column(db.String())

    room_id = db.Column(UUID, db.ForeignKey('room.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User {self.firstname} {self.lastname} ({self.email})>"