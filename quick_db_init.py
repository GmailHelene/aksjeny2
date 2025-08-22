import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Initializing database...")
    from app import create_app
    from app.models import db
    
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        
        # List available tables
        tables = db.engine.table_names()
        print("Available tables:", tables)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
