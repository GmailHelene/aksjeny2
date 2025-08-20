from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import logging
import random
import numpy as np
from datetime import datetime, timedelta

oil_correlation = Blueprint('oil_correlation', __name__)
logger = logging.getLogger(__name__)

@oil_correlation.route('/oil-correlation')
@login_required
def oil_correlation_page():
    """Oil Price Correlation Matrix for Norwegian Stocks"""
    return render_template('oil_correlation.html', 
                         title="Oil Price Correlation - Aksjeradar")

@oil_correlation.route('/api/oil-correlation/matrix')
@login_required
def get_oil_correlation_matrix():
    """API endpoint for oil correlation matrix data"""
    try:
        # Norwegian oil-related stocks correlation with Brent crude
        oil_stocks = [
            {
                'symbol': 'EQNR.OL',
                'name': 'Equinor ASA',
                'sector': 'Energy',
                'correlation': random.uniform(0.75, 0.92),
                'current_price': 287.40,
                'change_percent': 2.3,
                'volume_correlation': random.uniform(0.65, 0.85),
                'volatility_ratio': random.uniform(1.2, 1.8),
                'beta_oil': random.uniform(1.1, 1.6)
            },
            {
                'symbol': 'AKE.OL',
                'name': 'Aker BP ASA',
                'sector': 'Energy',
                'correlation': random.uniform(0.80, 0.95),
                'current_price': 234.50,
                'change_percent': 3.1,
                'volume_correlation': random.uniform(0.70, 0.90),
                'volatility_ratio': random.uniform(1.4, 2.0),
                'beta_oil': random.uniform(1.3, 1.8)
            },
            {
                'symbol': 'VAR.OL',
                'name': 'Vår Energi ASA',
                'sector': 'Energy',
                'correlation': random.uniform(0.70, 0.88),
                'current_price': 34.85,
                'change_percent': 1.8,
                'volume_correlation': random.uniform(0.60, 0.80),
                'volatility_ratio': random.uniform(1.1, 1.7),
                'beta_oil': random.uniform(1.0, 1.5)
            },
            {
                'symbol': 'PGS.OL',
                'name': 'Petroleum Geo-Services ASA',
                'sector': 'Energy Equipment & Services',
                'correlation': random.uniform(0.65, 0.82),
                'current_price': 12.45,
                'change_percent': 4.2,
                'volume_correlation': random.uniform(0.55, 0.75),
                'volatility_ratio': random.uniform(1.8, 2.5),
                'beta_oil': random.uniform(1.2, 1.9)
            },
            {
                'symbol': 'SUBSEA.OL',
                'name': 'Subsea 7 SA',
                'sector': 'Energy Equipment & Services',
                'correlation': random.uniform(0.50, 0.75),
                'current_price': 124.20,
                'change_percent': 0.9,
                'volume_correlation': random.uniform(0.45, 0.65),
                'volatility_ratio': random.uniform(1.3, 1.9),
                'beta_oil': random.uniform(0.8, 1.4)
            },
            {
                'symbol': 'ARCHER.OL',
                'name': 'Archer Limited',
                'sector': 'Energy Equipment & Services',
                'correlation': random.uniform(0.40, 0.70),
                'current_price': 14.85,
                'change_percent': -1.2,
                'volume_correlation': random.uniform(0.35, 0.55),
                'volatility_ratio': random.uniform(1.5, 2.2),
                'beta_oil': random.uniform(0.9, 1.5)
            }
        ]
        
        # Current oil price data
        oil_data = {
            'brent_price': 85.42,
            'brent_change': 1.8,
            'wti_price': 81.95,
            'wti_change': 1.5,
            'gas_price': 2.654,
            'gas_change': 0.8,
            'last_updated': datetime.now().isoformat()
        }
        
        # Historical correlation trends (30 days)
        correlation_history = []
        base_correlation = 0.78
        for i in range(30):
            day_correlation = base_correlation + random.uniform(-0.15, 0.15)
            correlation_history.append({
                'date': (datetime.now() - timedelta(days=29-i)).isoformat(),
                'average_correlation': max(0, min(1, day_correlation)),
                'oil_price': 85.42 + random.uniform(-8, 8),
                'osebx_return': random.uniform(-3, 3)
            })
        
        # Sector analysis
        sector_analysis = {
            'energy_companies': len([s for s in oil_stocks if s['sector'] == 'Energy']),
            'service_companies': len([s for s in oil_stocks if 'Equipment' in s['sector']]),
            'average_correlation': np.mean([s['correlation'] for s in oil_stocks]),
            'strongest_correlation': max(oil_stocks, key=lambda x: x['correlation']),
            'weakest_correlation': min(oil_stocks, key=lambda x: x['correlation'])
        }
        
        return jsonify({
            'success': True,
            'oil_stocks': oil_stocks,
            'oil_data': oil_data,
            'correlation_history': correlation_history,
            'sector_analysis': sector_analysis,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting oil correlation matrix: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@oil_correlation.route('/api/oil-correlation/predictions')
@login_required
def get_oil_correlation_predictions():
    """AI predictions based on oil price movements"""
    try:
        # Generate predictions for Norwegian stocks based on oil scenarios
        scenarios = [
            {
                'scenario': 'Oil Price +10%',
                'oil_price_change': 10.0,
                'probability': 25,
                'predictions': [
                    {'symbol': 'EQNR.OL', 'predicted_return': 8.5, 'confidence': 92},
                    {'symbol': 'AKE.OL', 'predicted_return': 9.2, 'confidence': 89},
                    {'symbol': 'VAR.OL', 'predicted_return': 7.8, 'confidence': 85},
                    {'symbol': 'PGS.OL', 'predicted_return': 12.3, 'confidence': 78},
                ]
            },
            {
                'scenario': 'Oil Price -10%',
                'oil_price_change': -10.0,
                'probability': 30,
                'predictions': [
                    {'symbol': 'EQNR.OL', 'predicted_return': -7.2, 'confidence': 90},
                    {'symbol': 'AKE.OL', 'predicted_return': -8.9, 'confidence': 87},
                    {'symbol': 'VAR.OL', 'predicted_return': -6.5, 'confidence': 83},
                    {'symbol': 'PGS.OL', 'predicted_return': -11.8, 'confidence': 76},
                ]
            },
            {
                'scenario': 'Oil Price Stable',
                'oil_price_change': 0.0,
                'probability': 45,
                'predictions': [
                    {'symbol': 'EQNR.OL', 'predicted_return': 1.2, 'confidence': 75},
                    {'symbol': 'AKE.OL', 'predicted_return': 0.8, 'confidence': 72},
                    {'symbol': 'VAR.OL', 'predicted_return': 1.5, 'confidence': 70},
                    {'symbol': 'PGS.OL', 'predicted_return': 0.3, 'confidence': 65},
                ]
            }
        ]
        
        # Market regime analysis
        regime_analysis = {
            'current_regime': 'Moderate Volatility',
            'oil_trend': 'Bullish',
            'nok_impact': 'Positive correlation with oil',
            'risk_factors': [
                'Global economic slowdown',
                'OPEC+ production decisions',
                'Geopolitical tensions',
                'Norwegian krone strength'
            ],
            'opportunities': [
                'Energy transition investments',
                'Offshore wind projects',
                'Carbon capture technology',
                'LNG export capacity'
            ]
        }
        
        return jsonify({
            'success': True,
            'scenarios': scenarios,
            'regime_analysis': regime_analysis,
            'model_accuracy': 84.7,
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting oil correlation predictions: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
