from flask import Blueprint, render_template, request, current_app, send_file
from extensions.db import db
from extensions.image_service import image_service
from flask_login import login_required, current_user

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


@profile_bp.route('/profile/upload_pic', methods=['POST'])
@login_required
def upload_pic():
    pic = request.files['pic']
    if pic.filename != '':
        filename = image_service.crop_and_save_pic(pic)
        current_user.profile_pic = filename
        db.session.commit()
    return redirect(url_for(".view"))


@profile_bp.route('/profile-pics/<profile_pic>')
@login_required
def get_pic(profile_pic):
    maybe_user = User.query.filter_by(profile_pic=profile_pic).first()
    if not maybe_user or maybe_user.room != current_user.room:
        return 404
    path = current_app.config.get('PICTURE_PATH') + maybe_user.profile_pic
    return send_file(path, max_age=300)
