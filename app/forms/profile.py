from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import ValidationError, InputRequired, Length, EqualTo

from app.models import User


class PersonalInfoForm(FlaskForm):
    """ "Personal Information"""

    first_name = StringField(
        "First Name",
        [
            Length(
                min=5,
                max=20,
                message="Firstname length must be between %(min)d and %(max)d characters",
            )
        ],
    )
    last_name = StringField(
        "Last Name",
        [
            Length(
                min=5,
                max=20,
                message="Lastname length must be between %(min)d and %(max)d characters",
            )
        ],
    )
    bio = TextAreaField(
        "Bio",
        [Length(min=20, message="Bio length must be longer than %(min)d characters")],
    )
    personal_info_submit = SubmitField("Save Personal Info")


class ProfileSocialsForm(FlaskForm):
    social_twitter = StringField(
        "Twitter",
        [
            Length(
                min=5,
                max=100,
                message="Twitter length must be between %(min)d and %(max)d characters",
            )
        ],
    )
    social_github = StringField(
        "Github",
        [
            Length(
                min=5,
                max=100,
                message="Github length must be between %(min)d and %(max)d characters",
            )
        ],
    )
    social_facebook = StringField(
        "Facebook",
        [
            Length(
                min=5,
                max=100,
                message="Facebook length must be between %(min)d and %(max)d characters",
            )
        ],
    )
    social_linkedin = StringField(
        "Linkedin",
        [
            Length(
                min=5,
                max=100,
                message="Linkedin length must be between %(min)d and %(max)d characters",
            )
        ],
    )
    profile_socials_submit = SubmitField("Save Socials")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", [Length(min=4, max=72)])
    new_password = PasswordField("New Password", [Length(min=4, max=72)])
    verify_password = PasswordField("Verify Password", [EqualTo("new_password")])
    change_password_submit = SubmitField("Change Password")
