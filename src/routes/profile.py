from flask import Blueprint, get_flashed_messages, render_template, request, flash
from extensions.db import db
from flask_login import login_required, current_user

from models.Room import Room
from models.User import User
from routes.util import *

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
@login_required
def view():
    user: User = current_user
    return render_template("profile_settings.html", user=user)


@profile_bp.route('/profile/edit', methods=['POST'])
@login_required
def edit():
    user: User = current_user
    user.firstname = request.form.get("firstname")
    user.lastname = request.form.get("lastname")
    user.info = request.form.get("info")
    db.session.commit()
    return redirect(url_for(".view"))
