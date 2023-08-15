from app.models import db, BaseModel
from flask import url_for
import enum

post_tag = db.Table(
    "post_tag",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

post_category = db.Table(
    "post_category",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column(
        "category_id", db.Integer, db.ForeignKey("categories.id"), primary_key=True
    ),
)


class PostStatus(enum.Enum):
    PUBLISH = "publish"  # Viewable by any site visitor.
    DRAFT = "draft"  # This is an incomplete post that's not ready for publication.
    AUTO_DRAFT = "autodraft"  # saved automatically while you are editing.
    PRIVATE = "private"  # Viewable only to WordPress users at the Administrator level.
    INHERIT = "inherit"  # This allows a child post to automatically adopt the same status as its parent post.
    TRASH = "trash"

    @classmethod
    def _missing_(cls, value):
        return cls.DRAFT


class Post(BaseModel):
    """Blog post/article"""

    __tablename__ = "posts"

    parent_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    slug = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    meta_title = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.String(255), nullable=True)
    summary = db.Column(db.String(400))
    feature_image = db.Column(db.String(300))
    content = db.Column(db.Text)
    status = db.Column(db.Enum(PostStatus))
    published_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # relationships
    author = db.relationship("User", backref="posts")
    comments = db.relationship("Comment", backref="posts")
    categories = db.relationship("Category", secondary=post_category, backref="posts")
    tags = db.relationship("Tag", secondary=post_tag, backref="posts")

    def __repr__(self) -> str:
        return f"<Post {self.title}>"

    @property
    def featured_image_path(self):
        return (
            url_for("static", filename="frontend/images/blog/" + self.feature_image)
            if self.feature_image
            else None
        )

    @property
    def parmalink(self):
        return url_for("blog.get_post_by_slug", slug=self.slug)
