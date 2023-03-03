from app.models import db, BaseModel


class Tag(BaseModel):
    """Blog post tags"""

    __tablename__ = "tags"
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())

    def __repr__(self) -> str:
        return f'<Tag "{self.name}">'
