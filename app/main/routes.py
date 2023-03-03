from flask import json, render_template, flash, redirect, url_for, request, current_app
from app.main import bp
from datetime import date
from app.models import db, User, Post, Setting, SettingType
from sqlalchemy import desc


class Me:
    def __init__(self) -> None:
        self.name = "Wayand Bahramzy"
        self.position = "Full-stack web developer with focus on Backend"
        self.resume = f"I currently work as a Full-stack Web Developer for Trafficlab ApS, located in Copenhagen. I've been making websites for almost about {self.years()} years"

    def years(self) -> int:
        current_year = date.today().year
        return current_year - 2007


def get_featured_post():
    return Post.query.order_by(desc("id")).limit(6)


def get_user_info():
    return (
        db.session.query(
            User.first_name,
            User.last_name,
            User.bio,
            User.social_facebook,
            User.social_github,
            User.social_linkedin,
            User.social_twitter,
        )
        .filter(User.email == "wayandb@outlook.com")
        .first()
    )


@bp.get("/")
def index():
    general_setting = Setting().of_type(SettingType.GENERAL)
    return render_template(
        "frontend/home.html",
        general_setting=general_setting,
        me=get_user_info(),
        posts=get_featured_post(),
    )


@bp.get("/projects")
def contact():
    return render_template("frontend/projects.html")
