from extensions.db import db

class Room(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(80))
    primary_color = db.Column(db.String(6))
    secondary_color = db.Column(db.String(6))

    def __repr__(self):
        return f"<Room {self.name}>"