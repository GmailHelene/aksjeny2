from app import create_app, db
from app.models.achievements import Achievement, UserAchievement, UserStats

def init_achievements_db():
    """Initialize achievements database tables and default data"""
    app = create_app('development')
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("✓ Created achievements database tables")
        
        # Check if we already have achievements
        if Achievement.query.count() > 0:
            print("✓ Achievements already exist, skipping initialization")
            return
        
        # Create default achievements
        default_achievements = [
            {
                'name': 'Første innlogging',
                'description': 'Logg inn for første gang',
                'category': 'login',
                'points': 10,
                'icon': 'bi-star-fill',
                'badge_color': 'success'
            },
            {
                'name': 'Trofas bruker', 
                'description': 'Logg inn 7 dager på rad',
                'category': 'login',
                'points': 50,
                'icon': 'bi-calendar-check-fill',
                'badge_color': 'primary'
            },
            {
                'name': 'Aksje-entusiast',
                'description': 'Legg til 10 aksjer i favoritter',
                'category': 'favorites',
                'points': 25,
                'icon': 'bi-heart-fill',
                'badge_color': 'danger'
            },
            {
                'name': 'Portefølje-mester',
                'description': 'Opprett din første portefølje',
                'category': 'portfolio',
                'points': 30,
                'icon': 'bi-briefcase-fill',
                'badge_color': 'info'
            },
            {
                'name': 'Samfunnsbygger',
                'description': 'Skriv ditt første forum-innlegg',
                'category': 'forum',
                'points': 20,
                'icon': 'bi-chat-square-text-fill',
                'badge_color': 'secondary'
            },
            {
                'name': 'Analyse-ekspert',
                'description': 'Besøk analyser 25 ganger',
                'category': 'usage',
                'points': 40,
                'icon': 'bi-graph-up',
                'badge_color': 'warning'
            },
            {
                'name': 'Veteran investor',
                'description': 'Være medlem i 30 dager',
                'category': 'membership',
                'points': 100,
                'icon': 'bi-award-fill',
                'badge_color': 'dark'
            }
        ]
        
        for ach_data in default_achievements:
            achievement = Achievement(**ach_data)
            db.session.add(achievement)
        
        db.session.commit()
        print(f"✓ Created {len(default_achievements)} default achievements")
        
        # Create user stats for existing users
        from app.models.user import User
        users = User.query.all()
        
        for user in users:
            if not UserStats.query.filter_by(user_id=user.id).first():
                user_stats = UserStats(
                    user_id=user.id,
                    total_points=10,  # Give existing users the first login achievement
                    current_level=1,
                    consecutive_login_days=1,
                    last_login=user.created_at
                )
                db.session.add(user_stats)
                
                # Give them the first login achievement
                first_login_ach = Achievement.query.filter_by(category='login').first()
                if first_login_ach:
                    user_achievement = UserAchievement(
                        user_id=user.id,
                        achievement_id=first_login_ach.id
                    )
                    db.session.add(user_achievement)
        
        db.session.commit()
        print(f"✓ Initialized user stats for {len(users)} existing users")
        print("🎉 Achievements system successfully initialized!")

if __name__ == '__main__':
    init_achievements_db()
