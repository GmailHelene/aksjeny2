from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import json
import random
from datetime import datetime, timedelta

# Create Norwegian Market Intelligence Blueprint
norwegian_intel = Blueprint('norwegian_intel', __name__, url_prefix='/norwegian-intel')

@norwegian_intel.route('/')
def index():
    """Norwegian Market Intelligence Hub"""
    return render_template('norwegian_intel/index.html')

@norwegian_intel.route('/social-sentiment')
def social_sentiment():
    """Real-time social sentiment for Norwegian stocks"""
    # Simulated data - in production would connect to Twitter/Reddit APIs
    norwegian_stocks = [
        {'ticker': 'EQNR', 'name': 'Equinor ASA', 'sentiment': 0.75, 'mentions': 342, 'trend': 'bullish'},
        {'ticker': 'DNB', 'name': 'DNB Bank ASA', 'sentiment': 0.68, 'mentions': 218, 'trend': 'neutral'},
        {'ticker': 'TEL', 'name': 'Telenor ASA', 'sentiment': 0.45, 'mentions': 156, 'trend': 'bearish'},
        {'ticker': 'NHY', 'name': 'Norsk Hydro ASA', 'sentiment': 0.82, 'mentions': 89, 'trend': 'very_bullish'},
        {'ticker': 'MOWI', 'name': 'Mowi ASA', 'sentiment': 0.71, 'mentions': 67, 'trend': 'bullish'},
        {'ticker': 'YAR', 'name': 'Yara International ASA', 'sentiment': 0.63, 'mentions': 45, 'trend': 'neutral'},
        {'ticker': 'AKER', 'name': 'Aker ASA', 'sentiment': 0.78, 'mentions': 123, 'trend': 'bullish'},
        {'ticker': 'SalMar', 'name': 'SalMar ASA', 'sentiment': 0.69, 'mentions': 34, 'trend': 'neutral'}
    ]
    
    return render_template('norwegian_intel/social_sentiment.html', 
                         sentiment_data=norwegian_stocks,
                         last_updated=datetime.now())

@norwegian_intel.route('/oil-correlation')
def oil_correlation():
    """Oil price correlation matrix for Norwegian stocks"""
    # Simulated correlation data
    correlations = [
        {'ticker': 'EQNR', 'correlation': 0.89, 'strength': 'Very Strong', 'oil_sensitivity': 'High'},
        {'ticker': 'AKER', 'correlation': 0.72, 'strength': 'Strong', 'oil_sensitivity': 'High'},
        {'ticker': 'DNB', 'correlation': 0.34, 'strength': 'Moderate', 'oil_sensitivity': 'Medium'},
        {'ticker': 'NHY', 'correlation': 0.45, 'strength': 'Moderate', 'oil_sensitivity': 'Medium'},
        {'ticker': 'TEL', 'correlation': 0.12, 'strength': 'Weak', 'oil_sensitivity': 'Low'},
        {'ticker': 'MOWI', 'correlation': -0.08, 'strength': 'Very Weak', 'oil_sensitivity': 'Low'}
    ]
    
    oil_price_data = {
        'current_price': 85.67,
        'change_24h': 1.23,
        'change_percent': 1.46,
        'weekly_trend': 'bullish'
    }
    
    return render_template('norwegian_intel/oil_correlation.html',
                         correlations=correlations,
                         oil_data=oil_price_data,
                         current_time=datetime.now())

@norwegian_intel.route('/government-impact')
def government_impact():
    """Government announcement impact analyzer"""
    recent_announcements = [
        {
            'date': '2025-08-18',
            'title': 'Økt satsing på fornybar energi',
            'affected_sectors': ['Renewable Energy', 'Oil & Gas'],
            'impact_score': 0.78,
            'affected_stocks': ['EQNR', 'NHY', 'REC']
        },
        {
            'date': '2025-08-15', 
            'title': 'Nye skatteregler for oljesektoren',
            'affected_sectors': ['Oil & Gas'],
            'impact_score': -0.45,
            'affected_stocks': ['EQNR', 'AKER', 'PGS']
        },
        {
            'date': '2025-08-12',
            'title': 'Økt støtte til oppdrettsnæringen',
            'affected_sectors': ['Aquaculture'],
            'impact_score': 0.65,
            'affected_stocks': ['MOWI', 'SalMar', 'LSG']
        }
    ]
    
    return render_template('norwegian_intel/government_impact.html',
                         announcements=recent_announcements,
                         current_time=datetime.now())

@norwegian_intel.route('/shipping-intelligence')
def shipping_intelligence():
    """Norwegian shipping intelligence with Baltic Dry Index correlation"""
    shipping_data = [
        {'ticker': 'FRONTLINE', 'correlation_bdi': 0.82, 'fleet_size': 68, 'avg_age': 8.2},
        {'ticker': 'GOLDEN_OCEAN', 'correlation_bdi': 0.76, 'fleet_size': 84, 'avg_age': 9.1},
        {'ticker': 'WALLENIUS', 'correlation_bdi': 0.45, 'fleet_size': 125, 'avg_age': 12.3},
        {'ticker': 'HAFNIA', 'correlation_bdi': 0.67, 'fleet_size': 102, 'avg_age': 10.5}
    ]
    
    baltic_dry_index = {
        'current': 1456,
        'change_24h': -23,
        'change_percent': -1.55,
        'trend': 'bearish'
    }
    
    return render_template('norwegian_intel/shipping_intelligence.html',
                         shipping_data=shipping_data,
                         bdi_data=baltic_dry_index,
                         current_time=datetime.now())

@norwegian_intel.route('/api/real-time-sentiment/<ticker>')
def api_real_time_sentiment(ticker):
    """API endpoint for real-time sentiment data"""
    # Simulated real-time data
    sentiment_data = {
        'ticker': ticker.upper(),
        'sentiment_score': round(random.uniform(0.2, 0.9), 2),
        'mentions_1h': random.randint(5, 50),
        'trending_keywords': ['earnings', 'dividend', 'growth', 'oil'],
        'sentiment_trend': random.choice(['bullish', 'bearish', 'neutral']),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(sentiment_data)

@norwegian_intel.route('/api/oil-correlation/<ticker>')
def api_oil_correlation(ticker):
    """API endpoint for oil correlation data"""
    correlation_data = {
        'ticker': ticker.upper(),
        'oil_correlation': round(random.uniform(-0.2, 0.9), 2),
        'sensitivity': random.choice(['Low', 'Medium', 'High']),
        'price_elasticity': round(random.uniform(0.1, 2.5), 2),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(correlation_data)
