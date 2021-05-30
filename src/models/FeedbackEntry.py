from extensions.db import db
from models.User import User


class FeedbackEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    anonymous = db.Column(db.Boolean)

    giver_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    giver = db.relationship('User', backref=db.backref('given_feedback', lazy=True), foreign_keys=[giver_id])

    receiver_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    receiver = db.relationship('User', backref=db.backref('received_feedback', lazy=True), foreign_keys=[receiver_id])

    def __repr__(self):
        return f"<User {self.firstname} {self.lastname} ({self.email})>"

    def __init__(self, giver: User, receiver: User, text: str, anonymous: bool):
        self.giver = giver
        self.receiver = receiver
        self.text = text
        self.anonymous = anonymous

