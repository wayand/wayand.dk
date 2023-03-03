from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length, Optional


class CategoryForm(FlaskForm):
    parent_category = SelectField("Parent Category", default=-1)
    name = StringField(
        "Name",
        validators=[
            Length(
                min=2,
                max=50,
                message="Name length must be between %(min)d and %(max)d characters",
            ),
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
