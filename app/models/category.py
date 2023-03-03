from app.models import db, BaseModel


class Category(BaseModel):
    """Blog post categories"""

    __tablename__ = "categories"

    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    name = db.Column(db.String(75), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())

    def __repr__(self) -> str:
        return f'<Category "{self.name}">'
