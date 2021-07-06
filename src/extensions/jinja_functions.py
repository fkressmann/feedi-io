from flask import url_for, request
from flask_login import current_user


class JinjaFunctions:
    def init_app(self, app):
        self.s3_url = app.config.get('CLOUDFRONT_PATH')
        app.jinja_env.globals.update(get_profile_pic=self.get_profile_pic)
        app.jinja_env.globals.update(get_room_pic=self.get_room_pic)
        app.jinja_env.globals.update(is_active_menu_entry_for=self.is_active_menu_entry_for)

    def get_room_pic(self):
        room = current_user.room
        return self.pic_url(room.room_pic) if room.room_pic else url_for('static', filename='img/logo.png')

    def is_active_menu_entry_for(self, menue_entry):
        return 'text-primary' if url_for(request.endpoint)[1:] == menue_entry else ''

    def get_profile_pic(self, user, anon=False):
        if anon:
            return url_for('static', filename='img/pic_anonymous.png')
        return self.pic_url(user.profile_pic) if user.profile_pic else url_for('static', filename='img/pic_missing.png')

    def pic_url(self, path):
        print(self.s3_url, path)
        return self.s3_url + path


jinja_functions = JinjaFunctions()
