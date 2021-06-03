from flask import url_for


def get_profile_pic(user, anon=False):
    if anon:
        return url_for('static', filename='img/pic_anonymous.png')
    return url_for('profile.get_pic', profile_pic=user.profile_pic) if user.profile_pic else url_for('static', filename='img/pic_missing.png')


class JinjaFunctions:
    def init(self, app):
        app.jinja_env.globals.update(get_profile_pic=get_profile_pic)


jinja_functions = JinjaFunctions()
