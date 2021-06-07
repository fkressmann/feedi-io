from flask import url_for, request
from flask_login import current_user


def get_profile_pic(user, anon=False):
    if anon:
        return url_for('static', filename='img/pic_anonymous.png')
    return url_for('profile.get_pic', profile_pic=user.profile_pic) if user.profile_pic else url_for('static', filename='img/pic_missing.png')


class JinjaFunctions:
    def init_app(self, app):
        app.jinja_env.globals.update(get_profile_pic=get_profile_pic)
        app.jinja_env.globals.update(get_room_pic=self.get_room_pic)
        app.jinja_env.globals.update(is_active_menu_entry_for=self.is_active_menu_entry_for)

    def get_room_pic(self):
        room = current_user.room
        return url_for('room.get_pic', room_pic=room.room_pic) if room.room_pic else url_for('static', filename='img/logo.png')

    def is_active_menu_entry_for(self, menue_entry):
        return 'text-primary' if url_for(request.endpoint)[1:] == menue_entry else ''


jinja_functions = JinjaFunctions()
