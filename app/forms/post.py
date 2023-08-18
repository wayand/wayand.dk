from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import ValidationError, InputRequired, Length, Optional
from app.models import Post


class PostForm(FlaskForm):
    """Post form"""

    title = StringField(
        "Title",
        [
            InputRequired(),
            Length(
                min=5, message="Title length must be longer than %(min)d characters"
            ),
        ],
    )
    meta_title = StringField(
        "Meta Title",
        [
            InputRequired(),
            Length(
                min=5, message="Meta Title length must be longer than %(min)d characters"
            ),
        ]
    )
    meta_description = StringField(
        "Meta Description",
        [
            InputRequired(),
            Length(
                min=5,max=255, message="Meta Descriptions length must be between %(min)d and %(max)d characters"
            ),
        ]
    )
    content = TextAreaField(
        "Content",
        [
            Length(
                min=20, message="Content length must be longer than %(min)d characters"
            )
        ],
    )
    categories = SelectMultipleField("Categories", coerce=int)
    tags = SelectMultipleField("Tags", coerce=int)
    featured_image = FileField(
        "Featured image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"], "Only Images types .jpg and png are allowed!!"
            )
        ],
    )
    summary = TextAreaField(
        "Summary",
        [
            Optional(),
            Length(min=20, message="Summary length must be longer than %(min)d chars."),
        ],
    )
    submit = SubmitField("Submit")

    def __init__(self, original_title=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_title(self, title):
        if title.data != self.original_title:
            duplicate_check = Post.query.filter_by(title=title.data).first()
            if duplicate_check:
                raise ValidationError("Please use a different title.")
