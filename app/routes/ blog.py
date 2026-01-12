from flask import Blueprint, render_template, abort
from app.utils import load_blog_posts, get_post_by_slug

bp = Blueprint('blog', __name__)

@bp.route('/')
def blog():
    """Liste des articles de blog"""
    posts = load_blog_posts()
    return render_template('blog.html', posts=posts)

@bp.route('/<slug>')
def post(slug):
    """Article de blog individuel"""
    post = get_post_by_slug(slug)
    if not post:
        abort(404)
    return render_template('post.html', post=post)