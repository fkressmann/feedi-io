from flask import Blueprint, get_flashed_messages, render_template, request, flash
from flask_login import login_required, current_user

from extensions.db import db
from models.Room import Room
from models.User import User
from routes.util import *

room_bp = Blueprint('room', __name__)


@room_bp.route("/overview")
@login_required
def overview():
    user: User = current_user
    room_users = [u for u in user.room.users]
    room_users.remove(user)
    return render_template("overview.html", room_users=room_users)


@room_bp.route('/create-room', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create_room.html")
    else:
        room_name = request.form.get('room_name')
        pri_color = request.form.get('primary_color')
        sec_color = request.form.get('secondary_color')
        room = Room(room_name, pri_color, sec_color)

        db.session.add(room)
        db.session.commit()

        return render_template('room_created.html', room=room)
