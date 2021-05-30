from flask_login import LoginManager
from models.User import User

login_manager = LoginManager()
login_manager.login_view = 'login.index'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)