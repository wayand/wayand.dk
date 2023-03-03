from app.models import db, BaseModel


class Comment(BaseModel):
    """User-generated comment on a blog post"""

    __tablename__ = 'comments'
    
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    body = db.Column(db.Text)

    published = db.Column(db.Boolean, default=False)
    removed = db.Column(db.Boolean, default=False)

    # relationships
    user = db.relationship('User')

    def __repr__(self) -> str:
        return f"<Post {self.id}>"
