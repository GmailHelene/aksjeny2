"""
Forum models for database-backed discussion system
"""

from datetime import datetime
from .. import db

class ForumCategory(db.Model):
    __tablename__ = 'forum_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='bi-folder')
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    topics = db.relationship('ForumTopic', backref='category', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ForumCategory {self.name}>'
    
    @property
    def topic_count(self):
        return self.topics.filter_by(is_active=True).count()
    
    @property
    def post_count(self):
        total = 0
        for topic in self.topics.filter_by(is_active=True):
            total += topic.post_count
        return total

class ForumTopic(db.Model):
    __tablename__ = 'forum_topics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    
    # Relationships
    category_id = db.Column(db.Integer, db.ForeignKey('forum_categories.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status fields
    is_pinned = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Counters
    view_count = db.Column(db.Integer, default=0)
    reply_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_post_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Tags (JSON field for flexibility)
    tags = db.Column(db.Text)  # JSON string of tags
    
    # Relationships
    author = db.relationship('User', backref='forum_topics')
    posts = db.relationship('ForumPost', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ForumTopic {self.title}>'
    
    @property
    def post_count(self):
        return self.posts.filter_by(is_active=True).count()
    
    @property
    def last_post(self):
        return self.posts.filter_by(is_active=True).order_by(ForumPost.created_at.desc()).first()
    
    def get_tags(self):
        """Get tags as a list"""
        import json
        if self.tags:
            try:
                return json.loads(self.tags)
            except:
                return []
        return []
    
    def set_tags(self, tag_list):
        """Set tags from a list"""
        import json
        self.tags = json.dumps(tag_list) if tag_list else None

class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    
    # Relationships
    topic_id = db.Column(db.Integer, db.ForeignKey('forum_topics.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=True)  # For replies
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_edited = db.Column(db.Boolean, default=False)
    
    # Engagement
    like_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='forum_posts')
    parent_post = db.relationship('ForumPost', remote_side=[id], backref='replies')
    likes = db.relationship('ForumPostLike', backref='post', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ForumPost {self.id} by {self.author.username if self.author else "Unknown"}>'

class ForumPostLike(db.Model):
    __tablename__ = 'forum_post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate likes
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_like'),)
    
    user = db.relationship('User', backref='forum_likes')
    
    def __repr__(self):
        return f'<ForumPostLike post:{self.post_id} user:{self.user_id}>'

class ForumTopicView(db.Model):
    __tablename__ = 'forum_topic_views'
    
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('forum_topics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for anonymous views
    ip_address = db.Column(db.String(45))
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    topic = db.relationship('ForumTopic', backref='topic_views')
    user = db.relationship('User', backref='forum_views')
    
    def __repr__(self):
        return f'<ForumTopicView topic:{self.topic_id} user:{self.user_id}>'
