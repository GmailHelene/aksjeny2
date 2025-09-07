from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify, g, send_from_directory, make_response, abort, Response
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import logging
from datetime import datetime, timedelta
import traceback
import random
import string
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, func, or_
import uuid
import requests
from functools import wraps
import time
import re
import base64
from io import BytesIO
from ..config import Config
from ..extensions import db, mail
from ..models import User
from ..utils.validators import is_safe_url, is_valid_email, is_strong_password
from ..utils.helpers import get_or_create_csrf_token
from ..utils.helpers import generate_random_number, generate_unique_id
from ..utils.cache import cache_with_timeout, clear_cache, get_cached_data
from ..utils.security import sanitize_input, is_valid_ip
from ..utils.logging_utils import setup_custom_logger
from ..utils.email_service import send_email
from flask_mail import Message

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

# Main routes
@main.route('/')
def index():
    """Home page with proper error handling"""
    try:
        # Track visit
        if current_user.is_authenticated:
            current_user.last_visit = datetime.now()
            db.session.commit()
        
        # Determine if demo mode is active
        demo_mode = session.get('demo_mode', False)
        
        # Get market overview data
        market_data = get_market_overview_data()
        
        # Get featured stocks for demo
        featured_stocks = get_featured_stocks()
        
        return render_template('index.html', 
                              market_data=market_data,
                              featured_stocks=featured_stocks,
                              demo_mode=demo_mode)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template('index.html', 
                              error="Vi beklager, det oppstod en feil ved lasting av siden. Vennligst prøv igjen senere.")

def get_market_overview_data():
    """Get overview of key market indices with demo fallback"""
    try:
        # If we have cached data, use it
        cached_data = get_cached_data('market_overview')
        if cached_data:
            return cached_data
        
        # Attempt to get real market data
        try:
            # This would be replaced with actual market data API call
            # For now, returning realistic demo data
            pass
        except Exception as api_error:
            logger.warning(f"Failed to get market data from API: {api_error}")
        
        # Generate demo data as fallback
        market_data = {
            'osebx': {
                'value': 1234.56,
                'change': 14.52,
                'change_percent': 1.2,
                'trend': 'up'
            },
            'sp500': {
                'value': 4567.89,
                'change': -22.84,
                'change_percent': -0.5,
                'trend': 'down'
            },
            'bitcoin': {
                'value': 65432,
                'change': 1470,
                'change_percent': 2.3,
                'trend': 'up'
            },
            'usd_nok': {
                'value': 10.45,
                'change': 0.03,
                'change_percent': 0.3,
                'trend': 'up'
            }
        }
        
        # Cache the data
        cache_with_timeout('market_overview', market_data, timeout=300)  # Cache for 5 minutes
        
        return market_data
    except Exception as e:
        logger.error(f"Error getting market overview data: {e}")
        # Return minimal emergency fallback
        return {
            'osebx': {'value': 0, 'change': 0, 'change_percent': 0, 'trend': 'neutral'},
            'sp500': {'value': 0, 'change': 0, 'change_percent': 0, 'trend': 'neutral'},
            'bitcoin': {'value': 0, 'change': 0, 'change_percent': 0, 'trend': 'neutral'},
            'usd_nok': {'value': 0, 'change': 0, 'change_percent': 0, 'trend': 'neutral'}
        }

def get_featured_stocks():
    """Get featured stocks for homepage with demo fallback"""
    try:
        # If we have cached data, use it
        cached_data = get_cached_data('featured_stocks')
        if cached_data:
            return cached_data
            
        # Generate demo data
        featured_stocks = [
            {
                'symbol': 'EQNR.OL',
                'name': 'Equinor',
                'price': 0,
                'change_percent': 0.0,
                'recommendation': 'HOLD',
                'insight': 'Stabil utvikling'
            },
            {
                'symbol': 'DNB.OL',
                'name': 'DNB',
                'price': 0,
                'change_percent': 0.0,
                'recommendation': 'HOLD',
                'insight': 'Stabil utvikling'
            },
            {
                'symbol': 'TEL.OL',
                'name': 'Telenor',
                'price': 0,
                'change_percent': 0.0,
                'recommendation': 'HOLD',
                'insight': 'Stabil utvikling'
            }
        ]
        
        # Cache the data
        cache_with_timeout('featured_stocks', featured_stocks, timeout=900)  # Cache for 15 minutes
        
        return featured_stocks
    except Exception as e:
        logger.error(f"Error getting featured stocks: {e}")
        return []

@main.route('/demo')
def demo():
    """Activate demo mode for the session"""
    session['demo_mode'] = True
    flash('Demo-modus er aktivert! Utforsk alle funksjoner.', 'info')
    return redirect(url_for('main.index'))

@main.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@main.route('/terms')
def terms():
    """Terms and conditions page"""
    return render_template('terms.html')

@main.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')

@main.route('/help')
def help():
    """Help and FAQ page"""
    return render_template('help.html')

@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """User feedback form"""
    if request.method == 'POST':
        try:
            # Get form data
            name = sanitize_input(request.form.get('name', ''))
            email = sanitize_input(request.form.get('email', ''))
            message = sanitize_input(request.form.get('message', ''))
            feedback_type = sanitize_input(request.form.get('type', 'general'))
            
            # Validate inputs
            if not name or not email or not message:
                flash('Alle felt må fylles ut.', 'warning')
                return render_template('feedback.html')
            
            if not is_valid_email(email):
                flash('Vennligst oppgi en gyldig e-postadresse.', 'warning')
                return render_template('feedback.html')
            
            # Save feedback to database
            # [Implementation would go here]
            
            # Send notification email to admin
            try:
                subject = f"Ny tilbakemelding: {feedback_type}"
                body = f"Navn: {name}\nE-post: {email}\nType: {feedback_type}\n\nMelding:\n{message}"
                
                send_email(subject=subject, 
                          recipient="admin@aksjeradar.trade", 
                          body=body)
            except Exception as email_error:
                logger.error(f"Failed to send feedback notification email: {email_error}")
            
            flash('Takk for din tilbakemelding! Vi vil vurdere den nøye.', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            logger.error(f"Error in feedback submission: {e}")
            flash('Det oppstod en feil under innsendingen. Vennligst prøv igjen senere.', 'danger')
    
    return render_template('feedback.html')

@main.route('/robots.txt')
def robots():
    """Serve robots.txt file"""
    return send_from_directory('static', 'robots.txt')

@main.route('/sitemap.xml')
def sitemap():
    """Serve sitemap.xml file"""
    return send_from_directory('static', 'sitemap.xml')

@main.route('/api/health')
def health_check():
    """API health check endpoint"""
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        
        # Return success response
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.now().isoformat(),
            'version': getattr(Config, 'VERSION', 'unknown'),
            'environment': getattr(Config, 'FLASK_ENV', 'production')
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@main.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@main.route('/profile')
@login_required
def profile():
    """Redirect to the new profile page under /user"""
    return redirect(url_for('profile.profile_page'))

@main.route('/my-subscription')
@login_required
def my_subscription():
    """Display user's subscription details with improved error handling"""
    try:
        # Debug current user subscription info
        logger.info(f"User {current_user.id} subscription check:")
        logger.info(f"  has_subscription: {getattr(current_user, 'has_subscription', 'N/A')}")
        logger.info(f"  subscription_type: {getattr(current_user, 'subscription_type', 'N/A')}")
        logger.info(f"  subscription_start: {getattr(current_user, 'subscription_start', 'N/A')}")
        logger.info(f"  subscription_end: {getattr(current_user, 'subscription_end', 'N/A')}")
        logger.info(f"  is_premium: {getattr(current_user, 'is_premium', 'N/A')}")
        logger.info(f"  email: {current_user.email}")
        
        # Initialize subscription object
        subscription = None
        subscription_status = 'free'
        
        # Check subscription status using various methods
        try:
            # Check if user has active subscription attribute
            if hasattr(current_user, 'has_subscription') and current_user.has_subscription:
                subscription_status = 'premium'
            elif hasattr(current_user, 'has_active_subscription') and callable(current_user.has_active_subscription):
                if current_user.has_active_subscription():
                    subscription_status = 'premium'
            elif hasattr(current_user, 'is_premium') and current_user.is_premium:
                subscription_status = 'premium'
            # Check for exempt users (admin access)
            elif hasattr(current_user, 'email'):
                from ..utils.access_control import EXEMPT_EMAILS
                if current_user.email in EXEMPT_EMAILS:
                    subscription_status = 'premium'
            else:
                subscription_status = 'free'
        except Exception as e:
            logger.error(f"Error checking subscription status: {e}")
            subscription_status = 'free'
        
        # Get subscription details
        if subscription_status == 'premium':
            subscription = {
                'type': getattr(current_user, 'subscription_type', 'premium'),
                'start_date': getattr(current_user, 'subscription_start', None),
                'end_date': getattr(current_user, 'subscription_end', None),
                'status': 'active',
                'auto_renew': getattr(current_user, 'auto_renew', True),
                'billing_frequency': getattr(current_user, 'billing_frequency', 'monthly'),
                'price': '249 kr' if getattr(current_user, 'billing_frequency', 'monthly') == 'monthly' else '2499 kr'
            }
        
        return render_template('subscription/details.html', 
                             subscription=subscription, 
                             subscription_status=subscription_status)
    except Exception as e:
        logger.error(f"Error in my_subscription: {e}")
        flash('Vi kunne ikke hente abonnementsinformasjonen. Vennligst prøv igjen senere.', 'warning')
        return redirect(url_for('main.index'))
