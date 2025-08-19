"""
Advanced Features Blueprint
Implementing competitive features inspired by major financial platforms
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from ..services.external_data_service import ExternalDataService
from ..services.competitive_analysis_service import CompetitiveFeatureService
from ..utils.access_control import access_required, demo_access  # SECURITY FIX: Corrected import path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

advanced_features = Blueprint('advanced_features', __name__, url_prefix='/advanced')

# Initialize services - delay translation service import
external_data_service = ExternalDataService()
competitive_service = CompetitiveFeatureService()

@advanced_features.route('/')
@login_required
def index():
    """Advanced features dashboard"""
    try:
        # Import translation function safely within request context
        try:
            from ..services.translation_service import t
        except ImportError:
            def t(key, fallback=None, **kwargs):
                return fallback or key
        
        # Get comprehensive market data
        market_data = {
            'oslo_bors': external_data_service.get_oslo_bors_real_time(),
            'global_markets': external_data_service.get_global_markets_overview(),
            'crypto': external_data_service.get_crypto_overview(),
            'currencies': external_data_service.get_currency_rates(),
            'economic_indicators': external_data_service.get_economic_indicators()
        }
        
        # Get competitive features analysis
        competitive_features = competitive_service.get_missing_features()
        
        return render_template('advanced_features/dashboard.html',
                             market_data=market_data,
                             competitive_features=competitive_features)
    
    except Exception as e:
        logger.error(f"Error loading advanced features: {e}")
        return render_template('advanced_features/dashboard.html',
                             market_data={},
                             competitive_features=[],
                             error=str(e))

@advanced_features.route('/api/market-data')
@access_required  # SECURITY FIX: Added missing access control
def market_overview():
    """Real-time market overview API endpoint"""
    try:
        data = {
            'oslo_bors': external_data_service.get_oslo_bors_real_time(),
            'indices': external_data_service.get_oslo_bors_indices(),
            'global_markets': external_data_service.get_global_markets_overview(),
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(data)
    
    except Exception as e:
        logger.error(f"Error fetching market overview: {e}")
        return jsonify({'error': str(e)}), 500

@advanced_features.route('/crypto-dashboard')
@access_required
def crypto_dashboard():
    """Cryptocurrency tracking dashboard"""
    try:
        # Create comprehensive mock crypto data
        crypto_data = {
            'Bitcoin': {
                'symbol': 'BTC',
                'price': 43500.00,
                'change_percent': 2.45,
                'change_24h': 1040.50,
                'volume': 15820000000,
                'market_cap': 850000000000,
                'circulating_supply': 19500000
            },
            'Ethereum': {
                'symbol': 'ETH',
                'price': 2650.00,
                'change_percent': 1.82,
                'change_24h': 47.30,
                'volume': 8920000000,
                'market_cap': 318000000000,
                'circulating_supply': 120000000
            },
            'Solana': {
                'symbol': 'SOL',
                'price': 98.50,
                'change_percent': 4.12,
                'change_24h': 3.90,
                'volume': 1820000000,
                'market_cap': 44000000000,
                'circulating_supply': 446000000
            },
            'Cardano': {
                'symbol': 'ADA',
                'price': 0.485,
                'change_percent': -1.25,
                'change_24h': -0.006,
                'volume': 380000000,
                'market_cap': 17000000000,
                'circulating_supply': 35000000000
            },
            'Polkadot': {
                'symbol': 'DOT',
                'price': 7.42,
                'change_percent': 0.95,
                'change_24h': 0.07,
                'volume': 145000000,
                'market_cap': 9500000000,
                'circulating_supply': 1280000000
            },
            'Chainlink': {
                'symbol': 'LINK',
                'price': 14.85,
                'change_percent': 3.28,
                'change_24h': 0.47,
                'volume': 425000000,
                'market_cap': 8200000000,
                'circulating_supply': 552000000
            }
        }
        
        # Calculate total market data
        total_market_cap = sum(coin['market_cap'] for coin in crypto_data.values())
        
        market_stats = {
            'total_market_cap': total_market_cap,
            'total_volume_24h': sum(coin['volume'] for coin in crypto_data.values()),
            'btc_dominance': (crypto_data['Bitcoin']['market_cap'] / total_market_cap) * 100,
            'fear_greed_index': 68,
            'active_cryptocurrencies': len(crypto_data)
        }
        
        return render_template('advanced_features/crypto_dashboard.html',
                             crypto_data=crypto_data,
                             market_stats=market_stats)
    
    except Exception as e:
        logger.error(f"Error loading crypto dashboard: {e}")
        # Still provide fallback data even if there's an error
        fallback_data = {
            'Bitcoin': {'symbol': 'BTC', 'price': 43500.00, 'change_percent': 2.45},
            'Ethereum': {'symbol': 'ETH', 'price': 2650.00, 'change_percent': 1.82}
        }
        return render_template('advanced_features/crypto_dashboard.html',
                             crypto_data=fallback_data,
                             market_stats={'total_market_cap': 1200000000000},
                             error=str(e))
    """Cryptocurrency tracking dashboard"""
    try:
        # Create comprehensive mock crypto data
        crypto_data = {
            'Bitcoin': {
                'symbol': 'BTC',
                'price': 43500.00,
                'change_percent': 2.45,
                'change_24h': 1040.50,
                'volume': 15820000000,
                'market_cap': 850000000000,
                'circulating_supply': 19500000
            },
            'Ethereum': {
                'symbol': 'ETH',
                'price': 2650.00,
                'change_percent': 1.82,
                'change_24h': 47.30,
                'volume': 8920000000,
                'market_cap': 318000000000,
                'circulating_supply': 120000000
            },
            'Solana': {
                'symbol': 'SOL',
                'price': 98.50,
                'change_percent': 4.12,
                'change_24h': 3.90,
                'volume': 1820000000,
                'market_cap': 44000000000,
                'circulating_supply': 446000000
            },
            'Cardano': {
                'symbol': 'ADA',
                'price': 0.485,
                'change_percent': -1.25,
                'change_24h': -0.006,
                'volume': 380000000,
                'market_cap': 17000000000,
                'circulating_supply': 35000000000
            },
            'Polkadot': {
                'symbol': 'DOT',
                'price': 7.42,
                'change_percent': 0.95,
                'change_24h': 0.07,
                'volume': 145000000,
                'market_cap': 9500000000,
                'circulating_supply': 1280000000
            },
            'Chainlink': {
                'symbol': 'LINK',
                'price': 14.85,
                'change_percent': 3.28,
                'change_24h': 0.47,
                'volume': 425000000,
                'market_cap': 8200000000,
                'circulating_supply': 552000000
            }
        }
        
        # Calculate total market data
        total_market_cap = sum(coin['market_cap'] for coin in crypto_data.values())
        
        market_stats = {
            'total_market_cap': total_market_cap,
            'total_volume_24h': sum(coin['volume'] for coin in crypto_data.values()),
            'btc_dominance': (crypto_data['Bitcoin']['market_cap'] / total_market_cap) * 100,
            'fear_greed_index': 68,
            'active_cryptocurrencies': len(crypto_data)
        }
        
        return render_template('advanced_features/crypto_dashboard.html',
                             crypto_data=crypto_data,
                             market_stats=market_stats)
    
    except Exception as e:
        logger.error(f"Error loading crypto dashboard: {e}")
        # Still provide fallback data even if there's an error
        fallback_data = {
            'Bitcoin': {'symbol': 'BTC', 'price': 43500.00, 'change_percent': 2.45},
            'Ethereum': {'symbol': 'ETH', 'price': 2650.00, 'change_percent': 1.82}
        }
        return render_template('advanced_features/crypto_dashboard.html',
                             crypto_data=fallback_data,
                             market_stats={'total_market_cap': 1200000000000},
                             error=str(e))

@advanced_features.route('/currency-converter')
@access_required  # SECURITY FIX: Added missing access control
def currency_converter():
    """Advanced currency converter"""
    try:
        # Always use mock data for reliability
        rates = {
            'USD/NOK': 10.85,
            'EUR/NOK': 11.75,
            'GBP/NOK': 13.65,
            'SEK/NOK': 0.99,
            'DKK/NOK': 1.58,
            'CHF/NOK': 12.20,
            'JPY/NOK': 0.074,
            'CAD/NOK': 8.12
        }
        
        return render_template('advanced_features/currency_converter.html',
                             rates=rates)
    
    except Exception as e:
        logger.error(f"Error loading currency converter: {e}")
        # Provide fallback rates
        fallback_rates = {
            'USD/NOK': 10.85,
            'EUR/NOK': 11.75,
            'GBP/NOK': 13.65,
            'SEK/NOK': 0.99
        }
        return render_template('advanced_features/currency_converter.html',
                             rates=fallback_rates,
                             error=str(e))

@advanced_features.route('/economic-calendar')
@login_required  
def economic_calendar():
    """Economic calendar with key indicators"""
    try:
        indicators = external_data_service.get_economic_indicators()
        
        return render_template('advanced_features/economic_calendar.html',
                             indicators=indicators)
    
    except Exception as e:
        logger.error(f"Error loading economic calendar: {e}")
        return render_template('advanced_features/economic_calendar.html',
                             indicators={},
                             error=str(e))

@advanced_features.route('/competitive-analysis')
@login_required
def competitive_analysis():
    """Show competitive analysis and missing features"""
    try:
        features = competitive_service.get_missing_features()
        
        return render_template('advanced_features/competitive_analysis.html',
                             features=features)
    
    except Exception as e:
        logger.error(f"Error loading competitive analysis: {e}")
        return render_template('advanced_features/competitive_analysis.html',
                             features=[],
                             error=str(e))
