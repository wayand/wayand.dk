from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app.admin import bp, Page
from app.models import Post, PostStatus, Category, Tag
from app.forms import PostForm
from datetime import datetime
from sqlalchemy import desc, text, func
from werkzeug.utils import secure_filename
import os
from app.utils import helpers


def get_post(id):
    post = Post.query.filter_by(id=id).first_or_404(
        description=f"Post id {id} doesn't exist."
    )
    return post


def save_uploaded_image(file):
    if not file:
        return None
    assets_dir = os.path.join(
        os.path.dirname(current_app.instance_path), "app/static/images"
    )

    filename = secure_filename(file.filename)
    file.save(os.path.join(assets_dir, "blog", filename))
    return filename


@bp.route("/posts/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_post(id):
    post = get_post(id)

    page = Page(can_show_component_new=False, title="Edit post", h1="Edit post")

    form = PostForm(post.title, obj=post)

    tags = Tag.query.all()
    tags = [(tag.id, tag.name) for tag in tags]
    form.tags.choices = tags

    categories = Category.query.all()
    categories = [(cat.id, cat.name) for cat in categories]
    form.categories.choices = categories

    if request.method == "GET":
        form.tags.data = [tag.id for tag in post.tags]
        form.categories.data = [cat.id for cat in post.categories]

    # status = request.form.get("submit-btn")
    status = PostStatus(request.form.get("submit-btn"))

    if form.validate_on_submit():
        tags = form.tags.data
        tags_objects_list = Tag.query.filter(Tag.id.in_(tags)).all()

        featured_image = save_uploaded_image(form.featured_image.data)

        categories = form.categories.data
        categories_objects_list = Category.query.filter(
            Category.id.in_(categories)
        ).all()

        post.title = form.title.data
        post.content = form.content.data
        post.summary = form.summary.data

        if featured_image:
            post.feature_image = featured_image

        post.status = status
        if status.value == "publish":
            post.published_at = datetime.utcnow()

        post.categories = categories_objects_list
        post.tags = tags_objects_list

        post.update()

        flash("Your post is now updated!", "success")
        return redirect(url_for("admin.edit_post", id=post.id))

    return render_template("admin/blog/post_form.html", page=page, form=form, post=post)


@bp.route("/posts/create", methods=("GET", "POST"))
@login_required
def create_post():

    page = Page(
        can_show_component_new=False, title="Create new post", h1="Create new post"
    )

    form = PostForm()

    tags = Tag.query.all()
    tags = [(tag.id, tag.name) for tag in tags]
    form.tags.choices = tags

    categories = Category.query.all()
    categories = [(cat.id, cat.name) for cat in categories]
    form.categories.choices = categories

    # status = request.form.get("submit-btn")
    status = PostStatus(request.form.get("submit-btn"))

    published_at = None
    if status.value == "publish":
        published_at = datetime.utcnow()

    if form.validate_on_submit():
        tags = form.tags.data
        tags_objects_list = Tag.query.filter(Tag.id.in_(tags)).all()

        categories = form.categories.data
        categories_objects_list = Category.query.filter(
            Category.id.in_(categories)
        ).all()

        post = Post(
            author_id=1,
            slug=helpers.create_slug(form.title.data),
            title=form.title.data,
            content=form.content.data,
            summary=form.summary.data,
            status=status,
            published_at=published_at,
        )
        post.categories.extend(categories_objects_list)
        post.tags.extend(tags_objects_list)
        post.save()

        flash("Your post is now live!", "info")
        return redirect(url_for("admin.posts"))

    return render_template("admin/blog/post_form.html", page=page, form=form)


@bp.get("/posts")
@login_required
def posts():
    SEARCH_QUERY = request.args.get("q")
    STATUS_FILTER = request.args.get("filter")
    ROWS_PER_PAGE = request.args.get("per_page", default=10, type=int)
    page = Page(can_show_component_new=False, title="Posts", h1="Overview of all posts")

    post_count_by_status = (
        Post.query.with_entities(Post.status, func.count("*"))
        .group_by(Post.status)
        .all()
    )
    post_count_by_status = {
        status_name.value: status_count
        for status_name, status_count in post_count_by_status
    }

    STATUS_FILTER = PostStatus(STATUS_FILTER).name if STATUS_FILTER else ""

    FILTERS = list()
    if STATUS_FILTER:
        FILTERS.append(text(f"status = '{STATUS_FILTER}'"))
    else:
        status_trash = PostStatus.TRASH.name
        FILTERS.append(text(f"status != '{status_trash}'"))
        if SEARCH_QUERY and len(SEARCH_QUERY) > 0:
            FILTERS.append(text(f"title ilike '%{SEARCH_QUERY}%'"))

    # Set the pagination configuration
    pagination_page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter(*FILTERS)
        .order_by(desc("id"))
        .paginate(page=pagination_page, per_page=ROWS_PER_PAGE, error_out=False)
    )

    next_url = (
        url_for("admin.posts", page=posts.next_num, per_page=ROWS_PER_PAGE)
        if posts.has_next
        else None
    )
    prev_url = (
        url_for("admin.posts", page=posts.prev_num, per_page=ROWS_PER_PAGE)
        if posts.has_prev
        else None
    )

    return render_template(
        "admin/blog/posts.html",
        posts=posts,
        next_url=next_url,
        prev_url=prev_url,
        page=page,
        post_count_by_status=post_count_by_status,
    )
