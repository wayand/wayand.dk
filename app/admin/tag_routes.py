from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.admin import bp, Page
from app.models import Tag
from app.forms import TagForm

from app.utils import helpers


@bp.route("/tags", methods=("GET", "POST"))
@login_required
def tags():

    page = Page(
        can_show_component_new=False,
        title="Overview of tags",
        h1="Tags",
    )

    form = TagForm()

    SEARCH_QUERY = request.args.get("q")

    if SEARCH_QUERY and len(SEARCH_QUERY) > 0:
        tags = Tag.query.filter(Tag.name.ilike(f"%{SEARCH_QUERY}%")).all()
    else:
        tags = Tag.query.all()

    if form.validate_on_submit():
        slug = form.slug.data if form.slug.data else form.name.data
        tag = Tag(
            name=form.name.data,
            slug=helpers.create_slug(slug),
            description=form.description.data,
        )
        tag.save()
        flash("Tag created successfully!", "success")
        return redirect(url_for("admin.tags"))

    return render_template("admin/blog/tags.html", page=page, tags=tags, form=form)


@bp.route("/tags/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_tag(id):

    tag = Tag.query.filter_by(id=id).first_or_404(
        description=f"Category id {id} doesn't exist."
    )
    page = Page(
        can_show_component_new=False,
        title="Edit Tag",
        h1=f"Edit Tag: '<b>{tag.name}</b>'",
    )

    form = TagForm(obj=tag)

    if form.validate_on_submit():
        slug = form.slug.data if form.slug.data else form.name.data
        tag.name = form.name.data
        tag.slug = helpers.create_slug(slug)
        tag.description = form.description.data

        tag.save()
        flash("Tag updated successfully!", "success")
        return redirect(url_for("admin.edit_tag", id=tag.id))

    return render_template("admin/blog/tag_form.html", page=page, form=form, tag=tag)
