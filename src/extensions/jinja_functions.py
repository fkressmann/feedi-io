from flask import url_for
from sqlalchemy.sql.functions import user
from models.Room import Room
from models.User import User


def get_profile_pic(user, anon=False):
    if anon:
        return url_for('static', filename='img/pic_anonymous.png')
    return url_for('profile.get_pic', profile_pic=user.profile_pic) if user.profile_pic else url_for('static', filename='img/pic_missing.png')

def get_room_pic_by_user_id(user_id):
    maybe_user: User = User.query.filter_by(id=user_id).first()
    maybe_room: Room = Room.query.filter_by(id=maybe_user.room_id).first()
    return url_for('room.get_pic', room_pic=maybe_room.room_pic) if maybe_room.room_pic else url_for('static', filename='img/logo.png')


class JinjaFunctions:
    def init_app(self, app):
        app.jinja_env.globals.update(get_profile_pic=get_profile_pic)
        app.jinja_env.globals.update(get_room_pic_by_user_id=get_room_pic_by_user_id)


jinja_functions = JinjaFunctions()
