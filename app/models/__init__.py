from app.models.base import db, BaseModel

from app.models.user import User
from app.models.tag import Tag
from app.models.category import Category
from app.models.post import Post, PostStatus
from app.models.comment import Comment
from app.models.setting import Setting, SettingType

from flask_marshmallow import Marshmallow

ma = Marshmallow()
