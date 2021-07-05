from flask import Blueprint, render_template, request, current_app, flash, send_file
from flask_login import login_required, current_user

from extensions.db import db
from extensions.limiter import limiter
from extensions.image_service import image_service
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
def create_room():
    return render_template("create_room.html")


@room_bp.route('/edit-room')
def edit_form():
    admin_key = request.args.get('admin_key')
    maybe_room = Room.query.filter_by(admin_key=admin_key).first()
    if not maybe_room:
        flash("Dieser Key ist falsch", FLASH_DANGER)
        return redirect(url_for('login.index'))
    return render_template("create_room.html", room=maybe_room)


@limiter.limit("1 per minute")
@room_bp.route('/create-room', methods=['POST'])
def create():
    room_name = request.form.get('room_name')
    maybe_room_pic = request.files.get('room_picture')
    pri_color = request.form.get('primary_color')
    sec_color = request.form.get('secondary_color')

    room_pic = None
    if maybe_room_pic:
        room_pic = image_service.save_pic(maybe_room_pic)

    room = Room(room_name, room_pic, pri_color, sec_color)
    db.session.add(room)
    db.session.commit()
    return render_template('room_created.html', room=room)


@limiter.limit("1 per second")
@room_bp.route('/edit-room', methods=['POST'])
def edit():
    room_name = request.form.get('room_name')
    maybe_room_pic = request.files.get('room_picture')
    pri_color = request.form.get('primary_color')
    sec_color = request.form.get('secondary_color')
    admin_key = request.form.get('key_to_update')

    maybe_room = Room.query.filter_by(admin_key=admin_key).first()
    if not maybe_room:
        flash("Dieser Key ist falsch", FLASH_DANGER)
        return redirect(url_for('login.index'))


    if maybe_room_pic:
        room_pic = image_service.save_pic(maybe_room_pic)
        old_filename = maybe_room.room_pic
        maybe_room.room_pic = room_pic
        image_service.delete_file(old_filename)
    maybe_room.name = room_name
    maybe_room.primary_color = pri_color
    maybe_room.secondary_color = sec_color
    db.session.commit()

    flash("Raum erfolgreich aktualisiert", FLASH_SUCCESS)
    return redirect(url_for('.edit_form', admin_key=admin_key))


@room_bp.route('/room-pics/<room_pic>')
@login_required
def get_pic(room_pic):
    room = Room.query.filter_by(room_pic=room_pic).first()
    if not current_user.room_id == room.id:
        return 404

    pic_bytes = image_service.get_file(room.room_pic)
    return send_file(pic_bytes, mimetype="image/jpeg", max_age=300)
