from app import create_app
from app.models.user import User
from app.models.favorites import Favorites
from flask import session, url_for, redirect, flash, render_template
from flask_login import login_user, current_user, login_required
import traceback
import logging

app = create_app()
logger = logging.getLogger(__name__)

def simplified_profile_route():
    """Simplified profile route for debugging"""
    with app.app_context():
        try:
            logger.info("Simplified profile route called")
            
            # Basic initialization with safe defaults
            user_stats = {
                'member_since': getattr(current_user, 'created_at', None),
                'last_login': getattr(current_user, 'last_login', None),
                'total_searches': getattr(current_user, 'total_searches', 0),
                'favorite_stocks': 0
            }
            
            # Simple favorites loading
            user_id = getattr(current_user, 'id', None)
            user_favorites = []
            
            if user_id:
                try:
                    favorites = Favorites.query.filter_by(user_id=user_id).all()
                    logger.info(f"Found {len(favorites)} favorites for user {user_id}")
                    
                    for fav in favorites:
                        favorite_info = {
                            'symbol': fav.symbol,
                            'name': fav.name or fav.symbol,
                            'exchange': fav.exchange or 'Unknown',
                            'created_at': fav.created_at
                        }
                        user_favorites.append(favorite_info)
                        
                    user_stats['favorite_stocks'] = len(user_favorites)
                    
                except Exception as db_error:
                    logger.error(f"Database error: {db_error}")
            
            # Return complete template with minimal data
            return render_template('profile.html',
                user=current_user,
                subscription=None,
                subscription_status='basic',
                user_stats=user_stats,
                user_language='nb',
                user_display_mode='light',
                user_number_format='norwegian',
                user_dashboard_widgets='[]',
                user_favorites=user_favorites,
                favorites=user_favorites,
                email_notifications=True,
                price_alerts=True,
                market_news=True,
                portfolio_updates=True,
                ai_insights=True,
                weekly_reports=True,
                referrals_made=0,
                referral_earnings=0,
                referral_code=f'REF{getattr(current_user, "id", "001")}',
                errors=None)
                
        except Exception as e:
            logger.error(f"Error in simplified profile: {e}")
            logger.error(traceback.format_exc())
            flash('Det oppstod en teknisk feil under lasting av profilen. Prøv igjen senere.', 'warning')
            return redirect(url_for('main.index'))

if __name__ == "__main__":
    # For testing outside of Flask context
    print("This is a helper module, not meant to be run directly")
