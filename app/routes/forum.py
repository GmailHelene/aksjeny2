from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from ..extensions import db
from ..models import User
import json

# Create Forum Blueprint
forum = Blueprint('forum', __name__, url_prefix='/forum')

# Simulated forum data (in production, this would be database models)
FORUM_TOPICS = [
    {
        'id': 1,
        'title': 'EQNR - Diskusjon om kvartalstall Q3 2025',
        'category': 'Enkeltaksjer',
        'author': 'NorwegianInvestor',
        'created': '2025-08-18 14:30',
        'replies': 23,
        'views': 156,
        'last_post': '2025-08-20 09:15',
        'pinned': True,
        'tags': ['EQNR', 'Olje', 'Kvartalstall']
    },
    {
        'id': 2, 
        'title': 'Beste småkapitalaksjer for 2025?',
        'category': 'Investeringsstrategier',
        'author': 'SmallCapHunter',
        'created': '2025-08-19 16:45',
        'replies': 18,
        'views': 89,
        'last_post': '2025-08-20 08:20',
        'pinned': False,
        'tags': ['Småkap', 'Strategi', '2025']
    },
    {
        'id': 3,
        'title': 'Teknisk analyse av DNB - Breakout eller fakeout?',
        'category': 'Teknisk Analyse',
        'author': 'ChartMaster',
        'created': '2025-08-20 07:30',
        'replies': 7,
        'views': 45,
        'last_post': '2025-08-20 09:45',
        'pinned': False,
        'tags': ['DNB', 'Teknisk', 'Breakout']
    }
]

FORUM_POSTS = {
    1: [
        {
            'id': 1,
            'author': 'NorwegianInvestor',
            'content': 'Hva tenker dere om EQNRs Q3-tall? Produksjonen ser sterk ut, men capex er høyere enn forventet.',
            'created': '2025-08-18 14:30',
            'likes': 5,
            'replies': []
        },
        {
            'id': 2,
            'author': 'OilAnalyst',
            'content': 'Enig i at produksjonstallene ser bra ut. Capex økningen er planlagt og støtter fremtidig vekst. Fortsatt positiv til EQNR.',
            'created': '2025-08-18 15:15',
            'likes': 3,
            'replies': []
        }
    ]
}

@forum.route('/')
def index():
    """Forum homepage with categories and recent topics"""
    categories = [
        {
            'name': 'Enkeltaksjer',
            'description': 'Diskusjon om spesifikke aksjer og selskaper',
            'topics': 45,
            'posts': 267,
            'icon': 'bi-building'
        },
        {
            'name': 'Investeringsstrategier', 
            'description': 'Del og diskuter investeringsstrategier',
            'topics': 32,
            'posts': 189,
            'icon': 'bi-graph-up'
        },
        {
            'name': 'Teknisk Analyse',
            'description': 'Charts, indikatorer og teknisk analyse',
            'topics': 28,
            'posts': 145,
            'icon': 'bi-bar-chart'
        },
        {
            'name': 'Markedsnyheter',
            'description': 'Diskuter dagens markedsnyheter og hendelser',
            'topics': 52,
            'posts': 324,
            'icon': 'bi-newspaper'
        },
        {
            'name': 'Begynnerhjørnet',
            'description': 'Spørsmål og hjelp for nye investorer',
            'topics': 67,
            'posts': 412,
            'icon': 'bi-question-circle'
        }
    ]
    
    recent_topics = FORUM_TOPICS[:5]  # Show 5 most recent
    
    return render_template('forum/index.html', 
                         categories=categories,
                         recent_topics=recent_topics)

@forum.route('/category/<category_name>')
def category(category_name):
    """Show topics in a specific category"""
    # Filter topics by category
    category_topics = [t for t in FORUM_TOPICS if t['category'] == category_name]
    
    # Create category info object
    category_info = {
        'name': category_name,
        'description': f'Diskusjon om {category_name.lower()}',
        'topics': len(category_topics),
        'posts': sum(t.get('replies', 0) for t in category_topics)
    }
    
    return render_template('forum/category.html',
                         category_name=category_name,
                         category_info=category_info,
                         topics=category_topics)

@forum.route('/topic/<int:topic_id>')
def topic(topic_id):
    """Show a specific topic with posts"""
    # Find topic
    topic_data = next((t for t in FORUM_TOPICS if t['id'] == topic_id), None)
    if not topic_data:
        flash('Topic not found', 'error')
        return redirect(url_for('forum.index'))
    
    # Get posts for this topic
    posts = FORUM_POSTS.get(topic_id, [])
    
    return render_template('forum/topic.html',
                         topic=topic_data,
                         posts=posts)

@forum.route('/create-topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    """Create a new forum topic"""
    
    # Define forum categories
    forum_categories = {
        'enkeltaksjer': {'display_name': 'Enkeltaksjer'},
        'investeringsstrategier': {'display_name': 'Investeringsstrategier'},
        'teknisk_analyse': {'display_name': 'Teknisk Analyse'},
        'markedsnyheter': {'display_name': 'Markedsnyheter'},
        'begynnerhjornet': {'display_name': 'Begynnerhjørnet'}
    }
    
    # Get category from URL parameter if provided
    category = request.args.get('category')
    category_info = forum_categories.get(category) if category else None
    
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        tags = request.form.get('tags', '').split(',')
        
        if not title or not category or not content:
            flash('Alle felter er påkrevd', 'error')
            return redirect(url_for('forum.create_topic'))
        
        # In production, save to database
        new_topic = {
            'id': len(FORUM_TOPICS) + 1,
            'title': title,
            'category': category,
            'author': current_user.username if current_user.is_authenticated else 'Anonymous',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'replies': 0,
            'views': 0,
            'last_post': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'pinned': False,
            'tags': [tag.strip() for tag in tags if tag.strip()]
        }
        
        FORUM_TOPICS.insert(0, new_topic)
        
        flash('Topic opprettet!', 'success')
        return redirect(url_for('forum.topic', topic_id=new_topic['id']))
    
    return render_template('forum/create_topic.html', 
                         forum_categories=forum_categories,
                         category=category,
                         category_info=category_info)

@forum.route('/post-reply/<int:topic_id>', methods=['POST'])
@login_required  
def post_reply(topic_id):
    """Post a reply to a topic"""
    content = request.form.get('content')
    
    if not content:
        flash('Innhold er påkrevd', 'error')
        return redirect(url_for('forum.topic', topic_id=topic_id))
    
    # Add reply to topic
    if topic_id not in FORUM_POSTS:
        FORUM_POSTS[topic_id] = []
    
    new_post = {
        'id': len(FORUM_POSTS[topic_id]) + 1,
        'author': current_user.username if current_user.is_authenticated else 'Anonymous',
        'content': content,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'likes': 0,
        'replies': []
    }
    
    FORUM_POSTS[topic_id].append(new_post)
    
    # Update topic reply count
    for topic in FORUM_TOPICS:
        if topic['id'] == topic_id:
            topic['replies'] += 1
            topic['last_post'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            break
    
    flash('Svar lagt til!', 'success')
    return redirect(url_for('forum.topic', topic_id=topic_id))

@forum.route('/search')
def search():
    """Search forum topics and posts"""
    query = request.args.get('q', '')
    
    if not query:
        return render_template('forum/search.html', results=[], query='')
    
    # Simple search implementation
    results = []
    for topic in FORUM_TOPICS:
        if (query.lower() in topic['title'].lower() or 
            query.lower() in topic.get('content', '').lower() or
            any(query.lower() in tag.lower() for tag in topic.get('tags', []))):
            results.append(topic)
    
    return render_template('forum/search.html', results=results, query=query)

@forum.route('/api/like-post/<int:topic_id>/<int:post_id>', methods=['POST'])
@login_required
def like_post(topic_id, post_id):
    """Like a forum post"""
    # In production, check if user already liked and update database
    if topic_id in FORUM_POSTS:
        for post in FORUM_POSTS[topic_id]:
            if post['id'] == post_id:
                post['likes'] += 1
                return jsonify({'success': True, 'likes': post['likes']})
    
    return jsonify({'success': False})
