#!/usr/bin/env python3
"""
Script to fix forum database issues and create missing tables
"""

import sys
import os
sys.path.append('/workspaces/aksjeny2')

from app import create_app, db
from app.models.forum import ForumPost, ForumCategory, ForumTopic

def fix_forum_tables():
    """Create forum tables and add default categories"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Checking forum database tables...")
            
            # Test if tables exist by querying them
            try:
                post_count = ForumPost.query.count()
                print(f"✅ ForumPost table exists - {post_count} posts")
            except Exception as e:
                print(f"❌ ForumPost table issue: {e}")
                
            try:
                category_count = ForumCategory.query.count()
                print(f"✅ ForumCategory table exists - {category_count} categories")
            except Exception as e:
                print(f"❌ ForumCategory table issue: {e}")
                
            try:
                topic_count = ForumTopic.query.count()
                print(f"✅ ForumTopic table exists - {topic_count} topics")
            except Exception as e:
                print(f"❌ ForumTopic table issue: {e}")
                
        except Exception as e:
            print(f"🚨 Database access error: {e}")
            print("🔧 Creating all forum tables...")
            
            # Create all database tables
            db.create_all()
            print("✅ All database tables created!")
            
        # Add default categories if they don't exist
        try:
            categories_data = [
                {
                    'name': 'Aksjeanalyse',
                    'slug': 'aksjeanalyse',
                    'description': 'Diskuter spesifikke aksjer og deres utvikling',
                    'icon': 'bi-graph-up',
                    'order': 1
                },
                {
                    'name': 'Markedstrender',
                    'slug': 'markedstrender', 
                    'description': 'Generelle markedstrender og økonomiske nyheter',
                    'icon': 'bi-trending-up',
                    'order': 2
                },
                {
                    'name': 'Investeringsstrategier',
                    'slug': 'investeringsstrategier',
                    'description': 'Diskuter forskjellige investeringsstrategier og tips',
                    'icon': 'bi-lightbulb',
                    'order': 3
                },
                {
                    'name': 'Generelt',
                    'slug': 'general',
                    'description': 'Generell diskusjon om investering og økonomi',
                    'icon': 'bi-chat-dots',
                    'order': 4
                }
            ]
            
            for cat_data in categories_data:
                existing = ForumCategory.query.filter_by(slug=cat_data['slug']).first()
                if not existing:
                    category = ForumCategory(**cat_data)
                    db.session.add(category)
                    print(f"➕ Added category: {cat_data['name']}")
                else:
                    print(f"✅ Category exists: {cat_data['name']}")
            
            db.session.commit()
            print("✅ Forum setup completed successfully!")
            
        except Exception as e:
            print(f"❌ Error setting up forum categories: {e}")
            db.session.rollback()

if __name__ == "__main__":
    fix_forum_tables()
