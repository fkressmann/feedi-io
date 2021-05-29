from extensions.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(), unique=True)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship('Team', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User {self.pseudo}>"