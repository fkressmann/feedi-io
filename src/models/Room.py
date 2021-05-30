from sqlalchemy import func

from extensions.db import db
import random
import uuid

class Room(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(80))
    primary_color = db.Column(db.String(7))
    secondary_color = db.Column(db.String(7))
    admin_key = db.Column(db.String(36))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __init__(self, name, primary_color, secondary_color):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.id = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
        self.admin_key = str(uuid.uuid4())


    def __repr__(self):
        return f"<Room {self.name}>"