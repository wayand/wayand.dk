from flask import json, render_template, flash, redirect, url_for, request
from app import sitemap
from app.blog import bp
from app.models import Post, Category, PostStatus, Setting, SettingType
from sqlalchemy import desc
import re
from datetime import datetime

class PageHeading:
    title: str = "Posts"
    breadcrumb: dict = {"name": "Posts", "link": "admin/posts"}

def find_h2_tags(text):
    pattern = r'<h2>(.*?)</h2>'
    matches = re.findall(pattern, text)
    return matches

@bp.get("/")
def posts():
    general_setting = Setting().of_type(SettingType.GENERAL)
    ROWS_PER_PAGE = general_setting["numberOfPostsOnBlogPage"].value

    # Set the pagination configuration
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter(Post.status == PostStatus.PUBLISH.name)
        .order_by(desc("id"))
        .paginate(page=page, per_page=int(ROWS_PER_PAGE))
    )

    next_url = url_for("blog.posts", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("blog.posts", page=posts.next_num) if posts.has_prev else None
    return render_template(
        "frontend/blog/posts.html",
        general_setting=general_setting,
        posts=posts,
        page_heading=PageHeading(),
        next_url=next_url,
        prev_url=prev_url,
    )

@bp.get("/categories/<string:category>")
def get_posts_by_category(category):
    general_setting = Setting().of_type(SettingType.GENERAL)
    ROWS_PER_PAGE = general_setting["numberOfPostsOnBlogPage"].value

    # Set the pagination configuration
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter(Post.status == PostStatus.PUBLISH.name, Post.categories.any(Category.slug == category))
        .order_by(desc("id"))
        .paginate(page=page, per_page=int(ROWS_PER_PAGE))
    )

    next_url = url_for("blog.posts", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("blog.posts", page=posts.next_num) if posts.has_prev else None
    return render_template(
        "frontend/blog/posts.html",
        general_setting=general_setting,
        posts=posts,
        page_heading=PageHeading(),
        next_url=next_url,
        prev_url=prev_url,
    )

@bp.get("/tags/<string:tag>")
def get_posts_by_tag(tag):
    ...

@bp.get("/<string:slug>")
def get_post_by_slug(slug):
    general_setting = Setting().of_type(SettingType.GENERAL)

    post = Post.query.filter_by(slug=slug, status=PostStatus.PUBLISH.name).first_or_404(
        description=f"Post slug {slug} doesn't exist."
    )
    h2tags = find_h2_tags(post.content)

    for h2 in h2tags:
        post.content = post.content.replace(f'<h2>{h2}</h2>', f'<h2 id="{ h2.replace(" ", "-") }"><a href="#{ h2.replace(" ", "-") }" class="headerlink" title="{h2}"></a>{h2}</h2>')

    return render_template(
        "frontend/blog/post.html",
        general_setting=general_setting,
        post=post,
        h2tags=h2tags,
        page_heading={},
    )


@sitemap.register_generator
def sitemap_get_post_by_slug():
    '''generate URLs using language codes
        Note. used by flask-sitemap
    '''
    posts = Post.query.filter_by(status=PostStatus.PUBLISH.name)
    for post in posts:
        yield 'blog.get_post_by_slug', {"slug":post.slug}, post.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ"), 'weekly', 0.9