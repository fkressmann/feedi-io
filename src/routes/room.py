from flask import Blueprint, get_flashed_messages, render_template, request, flash
from flask_login import login_required, current_user

from extensions.db import db
from extensions.limiter import limiter
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


@room_bp.route('/create-room')
def form():
    admin_key = request.args.get('admin_key')
    maybe_room = None
    if admin_key:
        maybe_room = Room.query.filter_by(admin_key=admin_key).first()
        if not maybe_room:
            flash("Dieser Key ist falsch", FLASH_DANGER)
            return redirect(url_for('login.index'))
    return render_template("create_room.html", content=maybe_room)


@limiter.limit("1 per minute")
@room_bp.route('/create-room', methods=['POST'])
def create():
    room_name = request.form.get('room_name')
    pri_color = request.form.get('primary_color')
    sec_color = request.form.get('secondary_color')
    key_to_update = request.form.get('key_to_update')

    if key_to_update:
        maybe_room = Room.query.filter_by(admin_key=key_to_update).first()
        if not maybe_room:
            flash("Dieser Key ist falsch", FLASH_DANGER)
            return redirect(url_for('login.index'))
        maybe_room.name = room_name
        maybe_room.primary_color = pri_color
        maybe_room.secondary_color = sec_color
        db.session.commit()
        flash("Raum erfolgreich aktualisiert", FLASH_SUCCESS)
        return redirect(url_for('login.index'))

    room = Room(room_name, pri_color, sec_color)
    db.session.add(room)
    db.session.commit()
    return render_template('room_created.html', room=room)
