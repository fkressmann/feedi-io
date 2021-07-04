from flask import Blueprint, render_template, request, current_app, send_file
from werkzeug.utils import send_from_directory
from extensions.db import db
from extensions.image_service import image_service
from flask_login import login_required, current_user

from models.User import User
from routes.util import *

import boto3
import json

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
    S3_BUCKET = current_app.config.get('S3_BUCKET')
    pic = request.files['pic']
    if pic.filename != '':
        content_type = request.mimetype
        old_filename = current_user.profile_pic
        new_filename = image_service.crop_and_save_pic(pic, content_type, True)
        current_user.profile_pic = new_filename
        db.session.commit()
        image_service.delete_image(S3_BUCKET,old_filename)
    return redirect(url_for(".view"))


@profile_bp.route('/profile-pics/<profile_pic>')
@login_required
def get_pic(profile_pic):
    S3_BUCKET = current_app.config.get('S3_BUCKET')

    maybe_user = User.query.filter_by(profile_pic=profile_pic).first()
    if not maybe_user or maybe_user.room != current_user.room:
        return 404

    response = image_service.s3_read_pic(S3_BUCKET,maybe_user.profile_pic)
    return send_file(response, mimetype="JPEG", max_age=300)


@profile_bp.route('/profile/sign_s3/')
def sign_s3():
  S3_BUCKET = current_app.config.get('S3_BUCKET')

  file_name = request.args.get('file_name')
  file_type = request.args.get('file_type')

  s3 = boto3.client('s3')

  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })