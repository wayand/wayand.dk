from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app.forms import (
    LoginForm,
    PersonalInfoForm,
    ProfileSocialsForm,
    ChangePasswordForm,
)
from app import login
from app.admin import bp, Page

# if not current_user.is_authenticated:
#     return current_app.login_manager.unauthorized()


@login.user_loader
def load_user(id):
    """Check if user is logged-in on every page load."""
    if id is not None:
        return User.query.get(int(id))
    return None


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("admin.dashboard")
            return redirect(next_page)

        flash("Please check your login details and try again.")
        return redirect(url_for("admin.login"))

    return render_template("admin/login.html", form=form)


@bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@bp.get("/profile")
@login_required
def profile():
    page = Page(
        can_show_component_new=False,
        title="General Settings",
        h1="General Settings",
    )
    personal_info_form = PersonalInfoForm(obj=current_user)
    profile_socials_form = ProfileSocialsForm(obj=current_user)
    change_password_form = ChangePasswordForm(obj=current_user)
    return render_template(
        "admin/profile.html",
        page=page,
        personal_info_form=personal_info_form,
        profile_socials_form=profile_socials_form,
        change_password_form=change_password_form,
    )
