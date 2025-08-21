#!/usr/bin/env python3
"""Check notifications database table and create if missing"""

import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_notifications_database():
    """Check if notifications table exists and create if missing"""
    try:
        from app import create_app
        from app.extensions import db
        from app.models.notifications import Notification
        
        app = create_app()
        
        with app.app_context():
            # Check if notifications table exists
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"Available database tables: {tables}")
            
            if 'notifications' not in tables:
                print("❌ Notifications table does not exist!")
                print("Creating notifications table...")
                
                # Create the table
                db.create_all()
                print("✅ Notifications table created successfully")
                
                # Create some sample notifications for testing
                from app.models.user import User
                users = User.query.limit(2).all()
                
                if users:
                    sample_notifications = [
                        {
                            'user_id': users[0].id,
                            'title': 'Welcome to Aksjeradar!',
                            'message': 'Thank you for joining our platform. Start by exploring our stock analysis tools.',
                            'type': 'system_alert',
                            'priority': 'medium'
                        },
                        {
                            'user_id': users[0].id,
                            'title': 'Price Alert: AAPL',
                            'message': 'Apple Inc. (AAPL) has reached your target price of $150.00',
                            'type': 'price_alert',
                            'priority': 'high',
                            'ticker': 'AAPL',
                            'price': 150.25,
                            'threshold': 150.0
                        }
                    ]
                    
                    for notif_data in sample_notifications:
                        notification = Notification(**notif_data)
                        db.session.add(notification)
                    
                    db.session.commit()
                    print(f"✅ Created {len(sample_notifications)} sample notifications")
                
            else:
                print("✅ Notifications table exists")
                
                # Check notification count
                notification_count = Notification.query.count()
                print(f"Total notifications in database: {notification_count}")
                
                if notification_count == 0:
                    print("ℹ️ No notifications found, creating sample data...")
                    
                    from app.models.user import User
                    users = User.query.limit(2).all()
                    
                    if users:
                        sample_notifications = [
                            Notification(
                                user_id=users[0].id,
                                title='System Status Update',
                                message='All systems are running smoothly. New features have been added to the platform.',
                                type='system_alert',
                                priority='low'
                            ),
                            Notification(
                                user_id=users[0].id,
                                title='Market Alert',
                                message='The Norwegian stock market (OSE) closed up 2.3% today.',
                                type='market_alert',
                                priority='medium'
                            )
                        ]
                        
                        for notification in sample_notifications:
                            db.session.add(notification)
                        
                        db.session.commit()
                        print(f"✅ Created {len(sample_notifications)} sample notifications")
            
            return True
            
    except Exception as e:
        print(f"❌ Error checking notifications database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_notifications_database()
    if success:
        print("\n✅ Notifications database check completed successfully!")
    else:
        print("\n❌ Notifications database check failed!")
