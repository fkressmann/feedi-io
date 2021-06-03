import uuid

from flask import Blueprint, get_flashed_messages, render_template, request, flash, current_app, send_file
from extensions.db import db
from flask_login import login_required, current_user
from PIL import Image, ImageOps
import io

from models.Room import Room
from models.User import User
from routes.util import *

profile_bp = Blueprint('profile', __name__)


def crop_and_save_pic(pic):
    image = Image.open(pic.stream)
    resized = ImageOps.fit(image, (500, 500))

    path = current_app.config.get('PROFILE_PIC_PATH')
    filename = str(uuid.uuid4()) + '.jpg'

    resized.save(path + filename)

    return filename


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


@profile_bp.route('/profile/upload_pic', methods=['POST'])
@login_required
def upload_pic():
    pic = request.files['pic']
    if pic.filename != '':
        filename = crop_and_save_pic(pic)
        current_user.profile_pic = filename
        db.session.commit()
    return redirect(url_for(".view"))


@profile_bp.route('/profile-pics/<profile_pic>')
@login_required
def get_pic(profile_pic):
    path = current_app.config.get('PROFILE_PIC_PATH') + profile_pic
    return send_file(path, max_age=300)
