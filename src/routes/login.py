from flask import Blueprint, get_flashed_messages, render_template, request, flash, url_for as for1
from werkzeug.utils import redirect as redirect1

from extensions.db import db
from flask_login import login_user

from models.Room import Room
from models.User import User
from routes.util import *

login_bp = Blueprint('login', __name__)


@login_bp.route('/')
def index():
    invite_id = request.args.get("invite_id")

    maybe_room = None
    if invite_id:
        maybe_room = Room.query.get(invite_id)
        if not maybe_room:
            flash("Sorry, dieser Link ist ungültig. Frage deinen Host nach dem richtigen Link.",
                  FLASH_DANGER)

    messages = get_flashed_messages(True)
    return render_template('login.html', messages=messages, room=maybe_room)


@login_bp.route('/login', methods=['POST'])
def login():
    room_id = request.form.get('room_id')
    email = request.form.get('user_id')
    password = request.form.get('password')
    type = request.form.get('type')
    print(room_id, email, password, type)
    print(request.form)

    if not room_id or not email or not password:
        flash(f"Unvollständig", FLASH_DANGER)
        return redirect(url_for('login.index', invite_id=room_id))

    maybe_room = Room.query.get(room_id)
    if not maybe_room:
        flash(f"Raum {room_id} konnte nicht gefunden werden", FLASH_DANGER)
        return redirect1(for1('login.index'))

    maybe_user: User = User.query.get(email)
    if type == 'sign_up':
        if maybe_user:
            flash("Es gibt schon einen Account mit dieser Email Adresse", FLASH_DANGER)
            return redirect(url_for('login.index', invite_id=room_id))

        new_user = User(email, password, maybe_room)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("profile.view"))
    else:
        if maybe_user.check_login(password):
            login_user(maybe_user)
            return redirect(url_for("profile.view"))
        else:
            flash(f"Das Passwort ist falsch", FLASH_DANGER)
            return redirect(url_for('login.index', invite_id=room_id))


def redirect_login():
    return redirect(url_for('login.index'))
