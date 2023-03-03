from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import ValidationError, Email, Length, InputRequired
from app.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        label="Your Email",
        validators=[
            InputRequired(),
            Length(min=1, max=64),
            Email(message="Enter a valid email."),
        ],
    )
    password = PasswordField(
        label="Your Password", validators=[InputRequired(), Length(min=4, max=72)]
    )
    remember = BooleanField(label="Remember me")

    submit = SubmitField("Sign in")

    # def validate_email(self, email):
    #     if User.query.filter_by(email=email.data).first():
    #         raise ValidationError("Email already registered!")
