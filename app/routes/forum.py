from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models.forum_post import ForumPost
from flask_login import login_required, current_user

forum = Blueprint('forum', __name__)

@forum.route('/')
def index():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('forum/index.html', posts=posts)

@forum.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('Tittel og innhold er påkrevd.', 'error')
            return redirect(url_for('forum.create'))
        post = ForumPost(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Innlegg opprettet!', 'success')
        return redirect(url_for('forum.index'))
    return render_template('forum/create.html')

@forum.route('/<int:post_id>')
def view(post_id):
    post = ForumPost.query.get_or_404(post_id)
    return render_template('forum/view.html', post=post)

@forum.route('/api/posts')
def api_posts():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])

@forum.route('/api/post/<int:post_id>')
def api_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    return jsonify(post.to_dict())
