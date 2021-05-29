from flask import url_for, redirect

FLASH_DANGER = 'danger'
FLASH_SUCCESS = 'success'
FLASH_WARNING = 'warning'
SESSION_USER = 'user_id'


def redirect_overview():
    return redirect(url_for('web.overview'))
