from flask import Blueprint, request, flash, url_for, redirect, render_template
from flask_login import login_required, current_user

from extensions.db import db
from models.FeedbackEntry import FeedbackEntry
from models.User import User
from routes.util import FLASH_DANGER, FLASH_SUCCESS

feedback_bp = Blueprint('feedback', __name__)


@feedback_bp.route('/feedback-received')
@login_required
def received():
    feedback = current_user.received_feedback
    return render_template("received_feedback.html", feedback=feedback)


@feedback_bp.route('/feedback-given')
@login_required
def given():
    feedback = current_user.given_feedback
    return render_template("given_feedback.html", feedback=feedback)


@feedback_bp.route('/feedback/delete')
def delete():
    id_to_delete = request.args.get('id')
    maybe_feedback = FeedbackEntry.query.get(id_to_delete)
    if not maybe_feedback or maybe_feedback.giver != current_user:
        flash("Kann nicht gelöscht werden", FLASH_DANGER)
        return redirect(url_for('feedback.given'))
    db.session.delete(maybe_feedback)
    db.session.commit()
    flash("Erfolgreich gelöscht", FLASH_SUCCESS)
    return redirect(url_for('feedback.given'))


@feedback_bp.route('/send-feedback')
@login_required
def send():
    receiver_id = request.args.get('receiver')
    maybe_receiver = User.query.get(receiver_id)
    if not maybe_receiver:
        flash("Diesen User kennen wir nicht", FLASH_DANGER)
        return redirect(url_for('room.overview'))

    if current_user.room != maybe_receiver.room:
        flash("Don't break it, dieser User gehört nicht zu deinem Room!", FLASH_DANGER)
        return redirect(url_for('room.overview'))

    return render_template("send_feedback.html", receiver=maybe_receiver)


@feedback_bp.route('/edit-feedback')
@login_required
def edit():
    feedback_id = request.args.get('id')
    maybe_feedback = FeedbackEntry.query.get(feedback_id)
    if not maybe_feedback or maybe_feedback.giver != current_user:
        flash("Ah fuck off", FLASH_DANGER)
        return redirect(url_for('feedback.given'))

    return render_template("send_feedback.html", receiver=maybe_feedback.receiver, content=maybe_feedback)


@feedback_bp.route('/save-feedback', methods=['POST'])
@login_required
def save():
    id_to_update = request.form.get('id_to_update')

    receiver = request.form.get('receiver_id')
    text = request.form.get('feedback_message')
    anonymous = True if request.form.get('send_anonymously') else False

    if id_to_update:
        maybe_feedback = FeedbackEntry.query.get(id_to_update)
        if not maybe_feedback or maybe_feedback.giver != current_user:
            flash("Ah fuck off", FLASH_DANGER)
            return redirect(url_for('feedback.given'))
        maybe_feedback.text = text
        maybe_feedback.anonymous = anonymous
        db.session.commit()
        flash("Erfolgreich aktualisiert", FLASH_SUCCESS)
        return redirect(url_for('feedback.given'))

    maybe_receiver = User.query.get(receiver)
    if not maybe_receiver:
        flash("Diesen Benutzer kennen wir nicht.", FLASH_DANGER)
        return redirect(url_for('room.overview'))

    if not text:
        flash("Musst schon was eingeben du Depp", FLASH_DANGER)
        return redirect(url_for('room.overview'))

    entry = FeedbackEntry(current_user, maybe_receiver, text, anonymous)
    db.session.add(entry)
    db.session.commit()

    flash("Feedback gespeichert, danke!", FLASH_SUCCESS)
    return redirect(url_for('room.overview'))
