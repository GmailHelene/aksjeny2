from sqlalchemy import text
from app.extensions import db

def add_missing_columns():
    """Add notification-related columns to users table if they don't exist"""
    
    columns_to_add = [
        ('email_notifications_enabled', 'BOOLEAN DEFAULT TRUE'),
        ('price_alerts_enabled', 'BOOLEAN DEFAULT TRUE'),
        ('market_news_enabled', 'BOOLEAN DEFAULT TRUE'),
        ('portfolio_updates_enabled', 'BOOLEAN DEFAULT TRUE'),
        ('ai_insights_enabled', 'BOOLEAN DEFAULT TRUE'),
        ('weekly_reports_enabled', 'BOOLEAN DEFAULT TRUE'),
        ('notification_settings', 'TEXT'),
        ('email_notifications', 'BOOLEAN DEFAULT TRUE'),
        ('price_alerts', 'BOOLEAN DEFAULT TRUE'),
        ('market_news', 'BOOLEAN DEFAULT TRUE')
    ]
    
    try:
        # Check each column
        for column_name, column_type in columns_to_add:
            try:
                # Check if column exists
                sql = text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='users' 
                    AND column_name=:column_name
                """)
                result = db.session.execute(sql, {'column_name': column_name})
                exists = result.fetchone() is not None

                if not exists:
                    # Add column if it doesn't exist
                    sql = text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
                    db.session.execute(sql)
                    print(f"Added column {column_name} to users table")
                else:
                    print(f"Column {column_name} already exists")
                    
            except Exception as e:
                print(f"Error checking/adding column {column_name}: {e}")
                
        db.session.commit()
        print("Successfully added all missing notification columns")
        
    except Exception as e:
        print(f"Database error: {e}")
        db.session.rollback()

if __name__ == '__main__':
    add_missing_columns()
