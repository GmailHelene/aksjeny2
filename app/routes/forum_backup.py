from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import desc, func
from ..extensions import db
from ..models import User, ForumCategory, ForumTopic, ForumPost, ForumPostLike, ForumTopicView
import json
import re

# Create Forum Blueprint
forum = Blueprint('forum', __name__, url_prefix='/forum')

def create_slug(title):
    """Create URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:100]  # Limit length

def initialize_forum_data():
    """Initialize forum with default categories and sample topics if database is empty"""
    try:
        # Check if categories exist
        if ForumCategory.query.count() == 0:
            # Create default categories
            categories = [
                {'name': 'Enkeltaksjer', 'slug': 'enkeltaksjer', 'description': 'Diskusjon om spesifikke aksjer og selskaper', 'icon': 'bi-building', 'order': 1},
                {'name': 'Investeringsstrategier', 'slug': 'investeringsstrategier', 'description': 'Del og diskuter investeringsstrategier', 'icon': 'bi-graph-up', 'order': 2},
                {'name': 'Teknisk Analyse', 'slug': 'teknisk-analyse', 'description': 'Charts, indikatorer og teknisk analyse', 'icon': 'bi-bar-chart', 'order': 3},
                {'name': 'Markedsnyheter', 'slug': 'markedsnyheter', 'description': 'Diskuter dagens markedsnyheter og hendelser', 'icon': 'bi-newspaper', 'order': 4},
                {'name': 'Begynnerhjørnet', 'slug': 'begynnerhjornet', 'description': 'Spørsmål og hjelp for nye investorer', 'icon': 'bi-question-circle', 'order': 5}
            ]
            
            for cat_data in categories:
                category = ForumCategory(**cat_data)
                db.session.add(category)
            
            db.session.commit()
            
            # Create sample topics with real Norwegian stock focus
            sample_topics = [
                {
                    'title': 'EQNR - Diskusjon om kvartalstall Q3 2025',
                    'content': 'Hva tenker dere om EQNRs Q3-tall? Produksjonen ser sterk ut, men capex er høyere enn forventet. Diskuter gjerne deres analyser her.',
                    'category_slug': 'enkeltaksjer',
                    'tags': ['EQNR', 'Olje', 'Kvartalstall'],
                    'is_pinned': True
                },
                {
                    'title': 'Beste småkapitalaksjer for 2025?',
                    'content': 'Hvilke småkapitalaksjer på Oslo Børs ser dere mest potensial i for 2025? Del deres analyser og favoritter!',
                    'category_slug': 'investeringsstrategier',
                    'tags': ['Småkap', 'Strategi', '2025']
                },
                {
                    'title': 'Teknisk analyse av DNB - Breakout eller fakeout?',
                    'content': 'DNB har brutt over viktig motstandsnivå på 220kr. Hva tenker dere - er dette et ekte breakout eller blir det en fakeout?',
                    'category_slug': 'teknisk-analyse',
                    'tags': ['DNB', 'Teknisk', 'Breakout']
                }
            ]
            
            # Get or create a default admin user for sample topics
            admin_user = User.query.filter_by(email='admin@aksjeradar.no').first()
            if not admin_user:
                admin_user = User.query.first()  # Use first available user
            
            if admin_user:
                for topic_data in sample_topics:
                    category = ForumCategory.query.filter_by(slug=topic_data['category_slug']).first()
                    if category:
                        topic = ForumTopic(
                            title=topic_data['title'],
                            slug=create_slug(topic_data['title']),
                            content=topic_data['content'],
                            category_id=category.id,
                            author_id=admin_user.id,
                            is_pinned=topic_data.get('is_pinned', False)
                        )
                        topic.set_tags(topic_data.get('tags', []))
                        db.session.add(topic)
                
                db.session.commit()
                
    except Exception as e:
        print(f"Error initializing forum data: {e}")
        db.session.rollback()

@forum.route('/')
def index():
    """Forum homepage with categories and recent topics"""
    try:
        # Initialize forum data if needed
        initialize_forum_data()
        
        # Get all active categories
        categories = ForumCategory.query.filter_by(is_active=True).order_by(ForumCategory.order, ForumCategory.name).all()
        
        # Get recent topics (last 10)
        recent_topics = ForumTopic.query.filter_by(is_active=True)\
            .order_by(desc(ForumTopic.last_post_at))\
            .limit(10).all()
        
        return render_template('forum/index.html', 
                             categories=categories,
                             recent_topics=recent_topics)
    except Exception as e:
        flash('Feil ved lasting av forum', 'error')
        return render_template('forum/index.html', categories=[], recent_topics=[])

@forum.route('/category/<category_slug>')
def category(category_slug):
    """Show topics in a specific category"""
    try:
        # Find category
        category_info = ForumCategory.query.filter_by(slug=category_slug, is_active=True).first()
        if not category_info:
            flash('Kategori ikke funnet', 'error')
            return redirect(url_for('forum.index'))
        
        # Get topics for this category
        topics = ForumTopic.query.filter_by(category_id=category_info.id, is_active=True)\
            .order_by(desc(ForumTopic.is_pinned), desc(ForumTopic.last_post_at)).all()
        
        return render_template('forum/category.html',
                             category_name=category_info.name,
                             category_info=category_info,
                             topics=topics)
    except Exception as e:
        flash('Feil ved lasting av kategori', 'error')
        return redirect(url_for('forum.index'))

@forum.route('/topic/<int:topic_id>')
def topic(topic_id):
    """Show a specific topic with posts"""
    try:
        # Find topic
        topic_data = ForumTopic.query.filter_by(id=topic_id, is_active=True).first()
        if not topic_data:
            flash('Topic not found', 'error')
            return redirect(url_for('forum.index'))
        
        # Increment view count
        topic_data.view_count += 1
        
        # Track unique views if user is logged in
        if current_user.is_authenticated:
            existing_view = ForumTopicView.query.filter_by(
                topic_id=topic_id, 
                user_id=current_user.id
            ).first()
            
            if not existing_view:
                view = ForumTopicView(topic_id=topic_id, user_id=current_user.id)
                db.session.add(view)
        
        db.session.commit()
        
        # Get posts for this topic
        posts = ForumPost.query.filter_by(topic_id=topic_id, is_active=True)\
            .order_by(ForumPost.created_at).all()
        
        return render_template('forum/topic.html',
                             topic=topic_data,
                             posts=posts)
    except Exception as e:
        flash('Feil ved lasting av topic', 'error')
        return redirect(url_for('forum.index'))

@forum.route('/create-topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    """Create a new forum topic"""
    
    # Get all active categories
    forum_categories = ForumCategory.query.filter_by(is_active=True)\
        .order_by(ForumCategory.order, ForumCategory.name).all()
    
    # Get category from URL parameter if provided
    category_slug = request.args.get('category')
    category_info = None
    if category_slug:
        category_info = ForumCategory.query.filter_by(slug=category_slug).first()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category_id = request.form.get('category')
        content = request.form.get('content', '').strip()
        tags_input = request.form.get('tags', '').strip()
        
        if not title or not category_id or not content:
            flash('Alle felter er påkrevd', 'error')
            return redirect(url_for('forum.create_topic'))
        
        try:
            # Validate category
            category = ForumCategory.query.filter_by(id=category_id, is_active=True).first()
            if not category:
                flash('Ugyldig kategori', 'error')
                return redirect(url_for('forum.create_topic'))
            
            # Process tags
            tags = []
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            
            # Create topic
            new_topic = ForumTopic(
                title=title,
                slug=create_slug(title),
                content=content,
                category_id=category.id,
                author_id=current_user.id
            )
            new_topic.set_tags(tags)
            
            db.session.add(new_topic)
            db.session.flush()  # Get the ID
            
            flash('Topic opprettet!', 'success')
            return redirect(url_for('forum.topic', topic_id=new_topic.id))
            
        except Exception as e:
            db.session.rollback()
            flash('Feil ved opprettelse av topic', 'error')
            return redirect(url_for('forum.create_topic'))
    
    return render_template('forum/create_topic.html', 
                         forum_categories=forum_categories,
                         category_info=category_info)

@forum.route('/post-reply/<int:topic_id>', methods=['POST'])
@login_required  
def post_reply(topic_id):
    """Post a reply to a topic"""
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('Innhold er påkrevd', 'error')
        return redirect(url_for('forum.topic', topic_id=topic_id))
    
    try:
        # Verify topic exists and is active
        topic_data = ForumTopic.query.filter_by(id=topic_id, is_active=True).first()
        if not topic_data:
            flash('Topic not found', 'error')
            return redirect(url_for('forum.index'))
        
        # Check if topic is locked
        if topic_data.is_locked:
            flash('Dette topic er låst for nye innlegg', 'error')
            return redirect(url_for('forum.topic', topic_id=topic_id))
        
        # Create new post
        new_post = ForumPost(
            content=content,
            topic_id=topic_id,
            author_id=current_user.id
        )
        
        db.session.add(new_post)
        
        # Update topic stats
        topic_data.reply_count += 1
        topic_data.last_post_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Svar lagt til!', 'success')
        return redirect(url_for('forum.topic', topic_id=topic_id))
        
    except Exception as e:
        db.session.rollback()
        flash('Feil ved posting av svar', 'error')
        return redirect(url_for('forum.topic', topic_id=topic_id))

@forum.route('/search')
def search():
    """Search forum topics and posts"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return render_template('forum/search.html', results=[], query='')
    
    try:
        # Search in topic titles and content
        results = ForumTopic.query.filter_by(is_active=True).filter(
            db.or_(
                ForumTopic.title.ilike(f'%{query}%'),
                ForumTopic.content.ilike(f'%{query}%'),
                ForumTopic.tags.ilike(f'%{query}%')
            )
        ).order_by(desc(ForumTopic.last_post_at)).limit(50).all()
        
        return render_template('forum/search.html', results=results, query=query)
        
    except Exception as e:
        flash('Feil ved søk', 'error')
        return render_template('forum/search.html', results=[], query=query)

@forum.route('/api/like-post/<int:topic_id>/<int:post_id>', methods=['POST'])
@login_required
def like_post(topic_id, post_id):
    """Like/unlike a forum post"""
    try:
        # Verify post exists
        post = ForumPost.query.filter_by(id=post_id, topic_id=topic_id, is_active=True).first()
        if not post:
            return jsonify({'success': False, 'error': 'Post not found'})
        
        # Check if user already liked this post
        existing_like = ForumPostLike.query.filter_by(
            post_id=post_id, 
            user_id=current_user.id
        ).first()
        
        if existing_like:
            # Unlike - remove like
            db.session.delete(existing_like)
            post.like_count = max(0, post.like_count - 1)
            liked = False
        else:
            # Like - add like
            new_like = ForumPostLike(post_id=post_id, user_id=current_user.id)
            db.session.add(new_like)
            post.like_count += 1
            liked = True
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'likes': post.like_count,
            'liked': liked
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Database error'})
