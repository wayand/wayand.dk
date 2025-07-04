import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Base configuration"""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    SECRET_KEY = os.environ.get("SECRET_KEY")
    TINYMCE_API_KEY = os.environ.get("TINYMCE_API_KEY")

    SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = False
    SITEMAP_URL_SCHEME = "https"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    ENV = "development"
    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_wayand_db.db"
