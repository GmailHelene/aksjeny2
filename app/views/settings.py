from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import app, db
from app.models import User, UserSettings

@app.route('/settings')
@login_required
def settings():
    """Display user settings page"""
    try:
        # Get or create user settings
        user_settings = UserSettings.query.filter_by(user_id=current_user.id).first()
        if not user_settings:
            user_settings = UserSettings(
                user_id=current_user.id,
                email_notifications=True,
                sms_notifications=False,
                push_notifications=False,
                newsletter=True
            )
            db.session.add(user_settings)
            db.session.commit()
        
        return render_template('settings/settings.html', 
                             user=current_user,
                             settings=user_settings)
    except Exception as e:
        app.logger.error(f"Settings error: {str(e)}")
        # Create minimal settings object for template
        default_settings = {
            'email_notifications': True,
            'sms_notifications': False,
            'push_notifications': False,
            'newsletter': True
        }
        return render_template('settings/settings.html', 
                             user=current_user,
                             settings=default_settings)

@app.route('/settings/update', methods=['POST'])
@login_required
def update_settings():
    """Update user settings via AJAX"""
    try:
        setting = request.form.get('setting')
        value = request.form.get('value') == 'true'
        
        user_settings = UserSettings.query.filter_by(user_id=current_user.id).first()
        if not user_settings:
            user_settings = UserSettings(user_id=current_user.id)
            db.session.add(user_settings)
        
        # Update the specific setting
        if hasattr(user_settings, setting):
            setattr(user_settings, setting, value)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Innstilling oppdatert'})
        else:
            return jsonify({'success': False, 'error': 'Ugyldig innstilling'}), 400
            
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Update settings error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
