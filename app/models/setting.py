import enum

from app.models import db, BaseModel


class SettingType(enum.Enum):
    GENERAL = "general"
    SEO = "seo"
    PRIVACY = "privacy"
    COMMENT = "comment"
    MEDIA = "media"


class Setting(BaseModel):
    """Blog setting"""

    __tablename__ = "settings"
    name = db.Column(db.String(100))
    value = db.Column(db.Text)
    type = db.Column(db.Enum(SettingType))

    @classmethod
    def of_type(cls, type):
        settings = cls.query.filter_by(type=type).all()
        return {setting.name: setting for setting in settings}

    def exists(self):
        return (
            db.session.query(Setting.name).filter_by(name=self.name).first() is not None
        )
