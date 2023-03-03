from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class TagForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            Length(
                min=1,
                max=30,
                message="Tag Name length must be between %(min)d and %(max)d characters",
            )
        ],
    )
    slug = StringField("Slug")
    description = TextAreaField(
        "Description",
        validators=[
            Length(
                max=100,
                message="Description length must be lower than %(max)d characters",
            )
        ],
    )
    submit = SubmitField("Submit")
