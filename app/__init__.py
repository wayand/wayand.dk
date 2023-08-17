from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sitemap import Sitemap

migrate = Migrate(compare_type=True)
login = LoginManager()
login.session_protection = "strong"
login.login_view = "admin.login"
login.login_message = "Please log in to access this page."


def page_not_found(e):
    return render_template("errors/404.html"), 404


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_error_handler(404, page_not_found)

    from app.models import db

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    sitemap = Sitemap()
    sitemap.init_app(app)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/apiv1")

    from app.admin import bp as admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.blog import bp as blog_bp

    app.register_blueprint(blog_bp, url_prefix="/blog")

    # for k, v in app.config.items():
    #     print('k:', k, 'v:', v)

    return app
