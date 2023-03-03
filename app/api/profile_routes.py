from flask import jsonify, request
from flask_login import current_user, login_required
from app.api import bp
from app.models import User
from app.forms import PersonalInfoForm, ProfileSocialsForm, ChangePasswordForm


@bp.patch("/profile/personal-info")
@login_required
def update_profile_personal_info():
    form = PersonalInfoForm()
    if form.validate():

        user = current_user
        user.first_name = (
            form.first_name.data if form.first_name.data else user.first_name
        )
        user.last_name = form.last_name.data if form.last_name.data else user.last_name
        user.bio = form.bio.data if form.bio.data else user.bio
        user.update()

        return jsonify(messange="ok")
    return jsonify(errors=form.errors), 400


@bp.patch("/profile/socials")
@login_required
def update_profile_socials():
    form = ProfileSocialsForm()
    if form.validate():
        user = current_user
        user.social_twitter = (
            form.social_twitter.data
            if form.social_twitter.data
            else user.social_twitter
        )
        user.social_github = (
            form.social_github.data if form.social_github.data else user.social_github
        )
        user.social_facebook = (
            form.social_facebook.data
            if form.social_facebook.data
            else user.social_facebook
        )
        user.social_linkedin = (
            form.social_linkedin.data
            if form.social_linkedin.data
            else user.social_linkedin
        )
        user.update()

        return jsonify(messange="ok")
    return jsonify(errors=form.errors), 400


@bp.patch("/profile/change-password")
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate():
        user = current_user
        if user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            user.update()
            return jsonify(messange="ok")
        else:
            return jsonify(errors={"error": "Incorrect current password entered."}), 409
    return jsonify(errors=form.errors), 400
