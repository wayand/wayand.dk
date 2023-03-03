from flask import Blueprint, render_template, request
from flask_login import login_required
from dataclasses import dataclass

bp = Blueprint("admin", __name__)


@dataclass
class Page:
    can_show_component_new: bool = False
    title: str = "page title"
    h1: str = "page h1 heading"


from app.admin import (
    auth_routes,
    post_routes,
    category_routes,
    tag_routes,
    settings_routes,
)


@bp.before_request
def my_login_required():
    print("request.endpoint", request.endpoint)
    if request.endpoint in ["admin.login"]:
        print("Inside-> request.endpoint", request.endpoint)
        return


@bp.get("/")
@bp.get("/dashboard")
@login_required
def dashboard():
    page = Page(
        can_show_component_new=True, title="Dashboard", h1="This is the Dashboard"
    )
    return render_template("admin/dashboard.html", page=page)


@bp.errorhandler(404)
def page_not_found(error):
    # app.logger.error('404', exc_info=sys.exc_info())
    return render_template("errors/admin/404.html", error=error)


@bp.errorhandler(500)
def internal_error(error):
    # app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    return render_template("errors/admin/500.html", error=error)
