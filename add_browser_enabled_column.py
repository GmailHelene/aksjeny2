from sqlalchemy import text
from app.extensions import db

def add_browser_enabled_column():
    """Add browser_enabled column to price_alerts table if it doesn't exist"""

    try:
        # Check if column exists
        sql = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='price_alerts'
            AND column_name='browser_enabled'
        """)
        result = db.session.execute(sql)
        exists = result.fetchone() is not None

        if not exists:
            # Add column if it doesn't exist
            sql = text("ALTER TABLE price_alerts ADD COLUMN browser_enabled BOOLEAN DEFAULT FALSE")
            db.session.execute(sql)
            print("Added column browser_enabled to price_alerts table")
        else:
            print("Column browser_enabled already exists")

        db.session.commit()
        print("Successfully added browser_enabled column")

    except Exception as e:
        print(f"Database error: {e}")
        db.session.rollback()

if __name__ == "__main__":
    add_browser_enabled_column()
