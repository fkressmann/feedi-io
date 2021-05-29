from flask import Blueprint, get_flashed_messages, render_template, request, flash

from extensions.db import db
from models.Room import Room
from models.User import User
from routes.util import *

room_bp = Blueprint('room', __name__)


@room_bp.route('/create-room', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create_room.html")
    else:
        print(request.form)
        room_name = request.form.get('room_name')
        pri_color = request.form.get('primary_color')
        sec_color = request.form.get('secondary_color')
        room = Room(room_name, pri_color, sec_color)

        db.session.add(room)
        db.session.commit()

        return f"Created. ID:{room.id}, admin key:{room.admin_key}"