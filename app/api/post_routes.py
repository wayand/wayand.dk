import pathlib
from flask import jsonify, request, current_app
from flask_login import current_user, login_required
from app.api import bp
from app.models import Post, Category, Tag
from sqlalchemy import desc, text, func
from app.utils import helpers
import os


@bp.patch("/posts/<int:id>/slug")
@login_required
def update_post_slug(id):
    post = Post.query.filter_by(id=id).first_or_404(
        description=f"Post id {id} doesn't exist."
    )

    json_data = request.get_json()
    slug = json_data.get("slug")
    if not slug:
        return jsonify(error="slug is required"), 422

    post.slug = helpers.clean_slug(slug)
    post.update()
    return jsonify(message="ok", parmalink=post.parmalink), 200


@bp.patch("/posts/bulk-trash")
@login_required
def post_bulk_trash():
    json_data = request.get_json()
    ids = json_data.get("ids")
    if not isinstance(ids, list) or len(ids) < 1:
        return jsonify(error="no post ids provided"), 422

    posts = Post.query.filter(Post.id.in_(ids)).all()
    for post in posts:
        post.status = "trash"
        post.update()

    return jsonify(message="ok", ids=[post.id for post in posts])


@bp.patch("/posts/bulk-restore")
@login_required
def post_bulk_restore():
    json_data = request.get_json()
    ids = json_data.get("ids")
    if not isinstance(ids, list) or len(ids) < 1:
        return jsonify(error="no post ids provided"), 422

    posts = Post.query.filter(Post.id.in_(ids)).all()
    for post in posts:
        post.status = "draft"
        post.update()

    return jsonify(message="ok", ids=[post.id for post in posts])


@bp.delete("/posts/<int:id>/feature-image")
@login_required
def feature_image_delete(id):
    post = Post.query.filter_by(id=id).first_or_404(
        description=f"Post id {id} doesn't exist."
    )

    feature_image_fullpath = os.path.join(
        os.path.dirname(current_app.instance_path), "app" + post.featured_image_path
    )

    pathlib.Path(feature_image_fullpath).unlink()

    post.feature_image = ""
    post.update()
    return jsonify(message="ok")


@bp.delete("/posts/<int:id>")
@login_required
def post_delete(id):
    post = Post.query.filter_by(id=id).first_or_404(
        description=f"Post id {id} doesn't exist."
    )
    post.delete()
    return jsonify(message="ok", id=post.id)


@bp.delete("/posts/bulk-delete")
@login_required
def post_bulk_delete():
    json_data = request.get_json()
    ids = json_data.get("ids")
    if not isinstance(ids, list) or len(ids) < 1:
        return jsonify(error="no post ids provided"), 422

    posts = Post.query.filter(Post.id.in_(ids)).all()
    for post in posts:
        post.delete()

    return jsonify(message="ok", ids=[post.id for post in posts])


@bp.delete("/categories/<int:id>")
@bp.delete("/categories")
@login_required
def category_delete(id=0):
    if id == 0:
        json_data = request.get_json()
        ids = json_data.get("ids")
        if not isinstance(ids, list) or len(ids) < 1:
            return jsonify(error="no category ids provided"), 422

        cats = Category.query.filter(Category.id.in_(ids)).all()
        for cat in cats:
            cat.delete()
        return jsonify(message="ok", ids=[cat.id for cat in cats])
    else:
        cat = Category.query.filter_by(id=id).first_or_404(
            description=f"Category id {id} doesn't exist."
        )
        cat.delete()
        return jsonify(message="ok", id=cat.id)


@bp.delete("/tags")
@login_required
def tag_delete():
    json_data = request.get_json()
    ids = json_data.get("ids")
    if not isinstance(ids, list) or len(ids) < 1:
        return jsonify(error="no tag ids provided"), 422

    tags = Tag.query.filter(Tag.id.in_(ids)).all()
    for tag in tags:
        tag.delete()
    return jsonify(message="ok", ids=[tag.id for tag in tags])
