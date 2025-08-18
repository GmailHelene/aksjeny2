from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
from ..utils.access_control import demo_access
from ..services.data_service import DataService
import logging

logger = logging.getLogger(__name__)

market_bp = Blueprint('market', __name__, url_prefix='/market')

@market_bp.route('/overview')
@demo_access
def overview():
    """Market overview page"""
    try:
        logger.info("Loading market overview page")
        
        # Get market data
        oslo_data = DataService.get_oslo_bors_overview()
        global_data = DataService.get_global_stocks_overview()
        crypto_data = DataService.get_crypto_overview()
        
        # Calculate market statistics
        stats = {
            'oslo_stocks': len(oslo_data) if oslo_data else 0,
            'global_stocks': len(global_data) if global_data else 0,
            'crypto_currencies': len(crypto_data) if crypto_data else 0,
            'total_instruments': (len(oslo_data) if oslo_data else 0) + 
                               (len(global_data) if global_data else 0) + 
                               (len(crypto_data) if crypto_data else 0)
        }
        
        # Get top performers
        top_performers = []
        worst_performers = []
        
        if oslo_data:
            oslo_list = list(oslo_data.values())
            oslo_sorted = sorted(oslo_list, key=lambda x: x.get('change_percent', 0), reverse=True)
            top_performers.extend(oslo_sorted[:5])
            worst_performers.extend(oslo_sorted[-3:])
        
        if global_data:
            global_list = list(global_data.values())
            global_sorted = sorted(global_list, key=lambda x: x.get('change_percent', 0), reverse=True)
            top_performers.extend(global_sorted[:5])
            worst_performers.extend(global_sorted[-3:])
        
        # Sort final lists
        top_performers = sorted(top_performers, key=lambda x: x.get('change_percent', 0), reverse=True)[:10]
        worst_performers = sorted(worst_performers, key=lambda x: x.get('change_percent', 0))[:6]
        
        return render_template('market/overview_standalone.html',
                             market_data={
                                 'oslo_stocks': oslo_data,
                                 'global_stocks': global_data,
                                 'crypto': crypto_data
                             },
                             stats=stats,
                             top_performers=top_performers,
                             worst_performers=worst_performers)
        
    except Exception as e:
        logger.error(f"Error loading market overview: {e}")
        return render_template('market/overview_standalone.html',
                             market_data={'oslo_stocks': {}, 'global_stocks': {}, 'crypto': {}},
                             stats={'oslo_stocks': 0, 'global_stocks': 0, 'crypto_currencies': 0, 'total_instruments': 0},
                             top_performers=[],
                             worst_performers=[],
                             error="Kunne ikke laste markedsdata")

@market_bp.route('/sectors')
@demo_access
def sectors():
    """Market sectors analysis page"""
    try:
        logger.info("Loading market sectors page")
        
        # Mock sector data (would normally come from an API)
        sectors = {
            'Energi': {
                'companies': ['EQNR.OL', 'AKE.OL', 'PGS.OL'],
                'change_percent': 2.3,
                'market_cap': 1200000000000,
                'top_performers': ['EQNR.OL']
            },
            'Teknologi': {
                'companies': ['AAPL', 'MSFT', 'GOOGL'],
                'change_percent': 1.8,
                'market_cap': 8500000000000,
                'top_performers': ['AAPL']
            },
            'Finans': {
                'companies': ['DNB.OL', 'NHY.OL'],
                'change_percent': -0.5,
                'market_cap': 650000000000,
                'top_performers': ['DNB.OL']
            },
            'Sjømat': {
                'companies': ['SALM.OL', 'LSG.OL'],
                'change_percent': 3.1,
                'market_cap': 450000000000,
                'top_performers': ['SALM.OL']
            }
        }
        
        # Sort sectors by performance
        sorted_sectors = sorted(sectors.items(), key=lambda x: x[1]['change_percent'], reverse=True)
        
        return render_template('market/sectors.html',
                             sectors=dict(sorted_sectors),
                             sector_stats={
                                 'total_sectors': len(sectors),
                                 'positive_sectors': len([s for s in sectors.values() if s['change_percent'] > 0]),
                                 'negative_sectors': len([s for s in sectors.values() if s['change_percent'] < 0])
                             })
        
    except Exception as e:
        logger.error(f"Error loading market sectors: {e}")
        return render_template('market/sectors.html',
                             sectors={},
                             sector_stats={'total_sectors': 0, 'positive_sectors': 0, 'negative_sectors': 0},
                             error="Kunne ikke laste sektordata")
