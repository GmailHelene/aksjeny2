from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models.forum import ForumPost
from app.models.user import User
from flask_login import login_required, current_user
from flask_wtf.csrf import validate_csrf, ValidationError
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

forum = Blueprint('forum', __name__)

@forum.route('/')
def index():
    """Forum main page with fallback for missing table"""
    try:
        # Get real forum statistics
        total_posts = ForumPost.query.count()
        total_topics = ForumPost.query.count()  # Assuming each post is a topic for now
        total_members = User.query.count()
        
        # Get recent posts for the main listing
        posts = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(20).all()
        
        # Get recent topics for sidebar
        recent_topics = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(5).all()
        
    except Exception as e:
        logger.error(f"Forum index error: {e}")
        # Fallback data when forum_posts table doesn't exist
        total_posts = 0
        total_topics = 0
        total_members = 0
        posts = []
        recent_topics = []
    
    # Create categories with actual or fallback data
    categories = [
        {
            'name': 'Aksjeanalyse',
            'description': 'Diskuter spesifikke aksjer og deres utvikling',
            'icon': 'bi bi-graph-up',
            'topics': max(1, total_topics // 3) if total_topics > 0 else 0,
            'posts': max(1, total_posts // 3) if total_posts > 0 else 0
        },
        {
            'name': 'Markedstrender',
            'description': 'Generelle markedstrender og økonomiske nyheter',
            'icon': 'bi bi-trending-up',
            'topics': max(1, total_topics // 3) if total_topics > 0 else 0,
            'posts': max(1, total_posts // 3) if total_posts > 0 else 0
        },
        {
            'name': 'Investeringsstrategier',
            'description': 'Del og diskuter ulike investeringsstrategier',
            'icon': 'bi bi-lightbulb',
            'topics': max(1, total_topics // 3) if total_topics > 0 else 0,
            'posts': max(1, total_posts // 3) if total_posts > 0 else 0
        }
    ]
    
    return render_template('forum/index.html', 
                         posts=posts, 
                         categories=categories,
                         recent_topics=recent_topics,
                         total_members=total_members,
                         online_now=max(1, total_members // 20) if total_members > 0 else 0)

@forum.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Validate CSRF token
        try:
            validate_csrf(request.form.get('csrf_token'))
        except ValidationError as e:
            logger.warning(f"CSRF validation failed: {e}")
            flash('Sikkerhetsfeil: Vennligst prøv igjen.', 'error')
            return redirect(url_for('forum.create'))
            
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('Tittel og innhold er påkrevd.', 'error')
            return redirect(url_for('forum.create'))
        post = ForumPost(
            title=title, 
            content=content, 
            user_id=current_user.id,
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Innlegg opprettet!', 'success')
        return redirect(url_for('forum.index'))
    return render_template('forum/create.html')

# Alias for create_topic (used in template)
@forum.route('/create_topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    """Create a new forum topic with simplified handling"""
    try:
        if request.method == 'POST':
            # Validate CSRF token
            try:
                validate_csrf(request.form.get('csrf_token'))
            except ValidationError as e:
                logger.warning(f"CSRF validation failed: {e}")
                flash('Sikkerhetsfeil: Vennligst prøv igjen.', 'error')
                return render_template('forum/create_topic.html')
            
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            category = request.form.get('category', 'general')
            
            if not title or not content:
                flash('Tittel og innhold er påkrevd.', 'error')
                return render_template('forum/create_topic.html')
                
            # Create a simple forum post (since ForumTopic might not exist)
            try:
                # Ensure database tables exist
                db.create_all()
                
                post = ForumPost(
                    title=title,
                    content=content,
                    user_id=current_user.id,
                    author_id=current_user.id,
                    category=category if hasattr(ForumPost, 'category') else None
                )
                db.session.add(post)
                db.session.commit()
                flash('Innlegg opprettet!', 'success')
                return redirect(url_for('forum.index'))
                
            except Exception as db_error:
                logger.error(f"Database error creating forum post: {db_error}")
                db.session.rollback()
                
                # Try creating a basic post without category field
                try:
                    post = ForumPost(
                        title=title,
                        content=content,
                        user_id=current_user.id,
                        author_id=current_user.id
                    )
                    db.session.add(post)
                    db.session.commit()
                    flash('Innlegg opprettet!', 'success')
                    return redirect(url_for('forum.index'))
                except Exception as fallback_error:
                    logger.error(f"Fallback forum post creation failed: {fallback_error}")
                    db.session.rollback()
                    flash('Kunne ikke opprette innlegg. Prøv igjen senere.', 'error')
                
        # GET request - show form
        categories = [
            {'id': 'aksjeanalyse', 'name': 'Aksjeanalyse'},
            {'id': 'markedstrender', 'name': 'Markedstrender'},
            {'id': 'investeringsstrategier', 'name': 'Investeringsstrategier'},
            {'id': 'general', 'name': 'Generelt'}
        ]
        
        return render_template('forum/create_topic.html', categories=categories)
        
    except Exception as e:
        logger.error(f"Error in create_topic: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        flash('En teknisk feil oppsto. Prøv igjen senere.', 'error')
        return redirect(url_for('forum.index'))

@forum.route('/category/<category_name>')
def category(category_name):
    """Category view with proper error handling"""
    try:
        # Handle invalid category names
        if category_name == '---' or not category_name.strip():
            flash('Ugyldig kategori.', 'error')
            return redirect(url_for('forum.index'))
        
        # Get posts - in the future this could be filtered by actual category
        posts = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(20).all()
        
        return render_template('forum/category.html', 
                             posts=posts, 
                             category_name=category_name.replace('-', ' ').title())
    except Exception as e:
        logger.error(f"Forum category error for {category_name}: {e}")
        flash('Kunne ikke laste kategori.', 'error')
        return redirect(url_for('forum.index'))

@forum.route('/topic/<topic_id>')
def topic(topic_id):
    """Topic view with proper error handling"""
    try:
        # Handle invalid topic IDs
        if topic_id == '---' or not str(topic_id).isdigit():
            flash('Ugyldig emne-ID.', 'error')
            return redirect(url_for('forum.index'))
        
        # Alias for view route
        return view(int(topic_id))
    except ValueError:
        flash('Ugyldig emne-ID.', 'error')
        return redirect(url_for('forum.index'))
    except Exception as e:
        logger.error(f"Forum topic error for {topic_id}: {e}")
        flash('Kunne ikke laste emne.', 'error')
        return redirect(url_for('forum.index'))

@forum.route('/search')
def search():
    """Search with better error handling"""
    try:
        query = request.args.get('q', '').strip()
        if query:
            # Use proper SQL LIKE syntax for better compatibility
            posts = ForumPost.query.filter(
                db.or_(
                    ForumPost.title.ilike(f'%{query}%'),
                    ForumPost.content.ilike(f'%{query}%')
                )
            ).order_by(ForumPost.created_at.desc()).limit(50).all()
        else:
            posts = []
        return render_template('forum/search.html', posts=posts, query=query)
    except Exception as e:
        logger.error(f"Forum search error for query '{query}': {e}")
        return render_template('forum/search.html', 
                             posts=[], 
                             query=query,
                             error="Søket kunne ikke utføres. Prøv igjen.")

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
