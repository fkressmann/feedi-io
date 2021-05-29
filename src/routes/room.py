from flask import Blueprint, get_flashed_messages, render_template, request, flash

from models.Room import Room
from models.User import User
from routes.util import *

room_bp = Blueprint('room', __name__)

@room_bp.route('/create-room')