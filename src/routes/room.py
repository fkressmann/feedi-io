import uuid

from flask import Blueprint, get_flashed_messages, render_template, request, current_app, flash, send_file
from flask_login import login_required, current_user
from PIL import Image, ImageOps

from extensions.db import db
from extensions.limiter import limiter
from models.Room import Room
from models.User import User
from routes.util import *

room_bp = Blueprint('room', __name__)

def crop_and_save_pic(pic):
    image = Image.open(pic.stream)

    path = current_app.config.get('ROOM_PIC_PATH')
    filename = str(uuid.uuid4()) + '.' + image.format

    image.save(path + filename)

    return filename

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
    maybe_room_pic = request.files['room_picture']
    pri_color = request.form.get('primary_color')
    sec_color = request.form.get('secondary_color')
    key_to_update = request.form.get('key_to_update')

    cropped_picture = ''
    if maybe_room_pic: cropped_picture = crop_and_save_pic(maybe_room_pic)

    if key_to_update:
        maybe_room = Room.query.filter_by(admin_key=key_to_update).first()
        if not maybe_room:
            flash("Dieser Key ist falsch", FLASH_DANGER)
            return redirect(url_for('login.index'))
        maybe_room.name = room_name
        maybe_room.room_pic = cropped_picture
        maybe_room.primary_color = pri_color
        maybe_room.secondary_color = sec_color
        db.session.commit()
        flash("Raum erfolgreich aktualisiert", FLASH_SUCCESS)
        return redirect(url_for('login.index'))

    room = Room(room_name, cropped_picture, pri_color, sec_color)
    db.session.add(room)
    db.session.commit()
    return render_template('room_created.html', room=room)

@room_bp.route('/room-pics/<room_pic>')
@login_required
def get_pic(room_pic):
    maybe_user = User.query.get(current_user.id)
    room = Room.query.filter_by(room_pic=room_pic).first()
    if not maybe_user or maybe_user.room_id != room.id:
        return 404
    path = current_app.config.get('ROOM_PIC_PATH') + room_pic
    return send_file(path, max_age=300)