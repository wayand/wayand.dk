from flask_login import UserMixin
from app.models import db, BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

from flask import url_for


class User(UserMixin, BaseModel):
    """User account"""

    __tablename__ = "users"

    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.Text)
    role = db.Column(db.String(50))

    social_twitter = db.Column(db.String(100))
    social_linkedin = db.Column(db.String(100))
    social_github = db.Column(db.String(100))
    social_facebook = db.Column(db.String(100))

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self) -> str:
    #     return f"<User {self.email}>"

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def url(self):
        return url_for("users.get", id=self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()

    @property
    def avatar_url(self):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon"
