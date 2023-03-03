from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.admin import bp, Page
from app.models import Category
from app.forms import CategoryForm

from app.utils import helpers


@bp.route("/categories", methods=("GET", "POST"))
@login_required
def categories():

    page = Page(
        can_show_component_new=False,
        title="Overview of categories",
        h1="Categories",
    )

    form = CategoryForm()

    SEARCH_QUERY = request.args.get("q")

    if SEARCH_QUERY and len(SEARCH_QUERY) > 0:
        categories = Category.query.filter(
            Category.name.ilike(f"%{SEARCH_QUERY}%")
        ).all()
    else:
        categories = Category.query.all()

    choices_cats = [(cat.id, cat.name) for cat in categories]
    choices_cats.append(("-1", "--"))
    form.parent_category.choices = choices_cats

    if form.validate_on_submit():
        # categories = Category.query.all()
        # categories = [(cat.id, cat.name) for cat in categories]
        # form.parent_category.choices = categories

        slug = form.slug.data if form.slug.data else form.name.data

        category = Category(
            name=form.name.data,
            slug=helpers.create_slug(slug),
            description=form.description.data,
            parent_id=form.parent_category.data
            if form.parent_category.data != "-1"
            else None,
        )
        category.save()
        flash("Category created successfully!", "success")
        return redirect(url_for("admin.categories"))

    return render_template(
        "admin/blog/categories.html", page=page, categories=categories, form=form
    )


@bp.route("/categories/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_category(id):
    category = Category.query.filter_by(id=id).first_or_404(
        description=f"Category id {id} doesn't exist."
    )
    page = Page(
        can_show_component_new=False,
        title="Update category " + category.name,
        h1="Update category " + category.name,
    )
    form = CategoryForm(obj=category)
    categories = Category.query.all()
    choices_cats = [(cat.id, cat.name) for cat in categories]
    choices_cats.append(("-1", "--"))
    form.parent_category.choices = choices_cats

    if request.method == "GET":
        form.parent_category.data = (
            category.parent_id if category.parent_id else form.parent_category.data
        )

    if form.validate_on_submit():
        slug = form.slug.data if form.slug.data else form.name.data
        category.name = form.name.data
        category.slug = helpers.create_slug(slug)
        category.parent_id = (
            form.parent_category.data if form.parent_category.data != "-1" else None
        )
        category.description = form.description.data

        category.update()
        flash("Your Category is now updated!", "success")
        return redirect(url_for("admin.edit_category", id=category.id))

    return render_template(
        "admin/blog/category_form.html", page=page, form=form, category=category
    )
