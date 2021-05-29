from flask import Blueprint, get_flashed_messages, render_template, request, flash

from models.Room import Room
from routes.util import *

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    invite_id = request.args.get("invite_id")
    print(invite_id)

    maybe_room = None
    if invite_id:
        maybe_room = Room.query.get(invite_id)
        if not maybe_room:
            flash("Sorry, dieser Link ist ungültig. Frage deinen Host nach dem richtigen Link.",
                  FLASH_DANGER)

    messages = get_flashed_messages(True)
    return render_template('login.html', messages=messages, room=maybe_room)
