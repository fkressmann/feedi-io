from flask import Blueprint, get_flashed_messages, render_template, request, flash, url_for as for1
from werkzeug.utils import redirect as redirect1

from extensions.db import db
from flask_login import login_user, login_required, logout_user

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

    return render_template('login.html', room=maybe_room)


@login_bp.route('/login', methods=['POST'])
def login():
    room_id = request.form.get('room_id')
    email = request.form.get('user_id')
    password = request.form.get('password')
    type = request.form.get('type')

    if not room_id or not email or not password:
        flash(f"Unvollständig", FLASH_DANGER)
        return redirect(url_for('login.index', invite_id=room_id))

    maybe_room = Room.query.get(room_id)
    if not maybe_room:
        flash(f"Raum {room_id} konnte nicht gefunden werden", FLASH_DANGER)
        return redirect1(for1('login.index'))

    maybe_user: User = User.query.filter_by(email=email).first()
    if type == 'sign_up':
        if maybe_user:
            flash("Es gibt schon einen Account mit dieser Email Adresse", FLASH_DANGER)
            return redirect(url_for('login.index', invite_id=room_id))

        new_user = User(email, password, maybe_room)
        db.session.add(new_user)
        db.session.commit()
        flash("Erfolgreich registiert!", FLASH_SUCCESS)
        login_user(new_user)
        return redirect(url_for("profile.view"))
    else:
        if maybe_user.check_login(password):
            login_user(maybe_user)
            return redirect(url_for("room.overview"))
        else:
            flash(f"Das Passwort ist falsch", FLASH_DANGER)
            return redirect(url_for('login.index', invite_id=room_id))


@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect_login()

def redirect_login():
    return redirect(url_for('login.index'))

@login_bp.route('/about')
def about():
    return render_template('about.html')