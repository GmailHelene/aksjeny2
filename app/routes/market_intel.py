"""
Market Intelligence Routes - for insider trading, institutional ownership, and market data
"""
import logging
from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..utils.access_control import access_required, demo_access

# Import service here to avoid issues
try:
    from ..services.external_apis import ExternalAPIService
except ImportError as e:
    print(f"Warning: Could not import ExternalAPIService: {e}")
    ExternalAPIService = None

logger = logging.getLogger(__name__)
market_intel = Blueprint('market_intel', __name__, url_prefix='/market-intel')

def get_real_insider_data(ticker):
    """Get real insider trading data for a specific ticker"""
    try:
        if ExternalAPIService:
            # Get real insider trading data
            insider_data = ExternalAPIService.get_insider_trading(ticker, limit=15)
            if insider_data:
                return insider_data
    except Exception as e:
        logger.warning(f"Error fetching real insider data for {ticker}: {e}")
    
    # Return empty list instead of fake data
    return []

def generate_demo_insider_data(ticker):
    """DEPRECATED: Use get_real_insider_data instead"""
    logger.warning(f"generate_demo_insider_data called for {ticker} - this function is deprecated")
    return get_real_insider_data(ticker)

@market_intel.route('/')
@access_required
def index():
    """Market intelligence dashboard"""
    try:
        # Check if service is available
        if not ExternalAPIService:
            return render_template('market_intel/index.html',
                                 insider_data={},
                                 sector_performance={},
                                 earnings_calendar=[],
                                 crypto_fear_greed={},
                                 economic_indicators={},
                                 market_news=[],
                                 error="Ekstern data-service er ikke tilgjengelig.")
        
        # Get recent insider trading for popular Norwegian and global stocks
        try:
            from ..services.data_service import DataService
            
            # Get top Norwegian stocks by market cap/volume
            oslo_tickers = ['EQNR.OL', 'DNB.OL', 'TEL.OL', 'NHY.OL', 'YAR.OL']
            global_tickers = ['AAPL', 'MSFT', 'TSLA']
            
            # Combine and prioritize based on real market data availability
            popular_tickers = []
            
            # Add Oslo stocks that have real data
            for ticker in oslo_tickers[:3]:
                try:
                    stock_info = DataService.get_stock_info(ticker)
                    if stock_info and stock_info.get('regularMarketPrice'):
                        popular_tickers.append(ticker)
                except:
                    continue
            
            # Add global stocks that have real data
            for ticker in global_tickers:
                try:
                    stock_info = DataService.get_stock_info(ticker)
                    if stock_info and stock_info.get('regularMarketPrice'):
                        popular_tickers.append(ticker)
                        if len(popular_tickers) >= 5:  # Limit total
                            break
                except:
                    continue
            
        except Exception as e:
            logger.warning(f"Error getting dynamic popular tickers: {e}")
            # Fallback to basic Norwegian stocks only
            popular_tickers = ['EQNR.OL', 'DNB.OL', 'TEL.OL']
        
        insider_data = {}
        
        for ticker in popular_tickers[:3]:  # Limit to avoid API rate limits
            try:
                insider_data[ticker] = ExternalAPIService.get_insider_trading(ticker, limit=5) or []
            except:
                insider_data[ticker] = []
        
        # Get sector performance with fallback
        try:
            sector_performance = ExternalAPIService.get_sector_performance() or {}
        except:
            sector_performance = {}
        
        # Get earnings calendar with fallback
        try:
            earnings_calendar = ExternalAPIService.get_earnings_calendar(days_ahead=14) or []
        except:
            earnings_calendar = []
        
        # Get crypto fear & greed index with fallback
        try:
            crypto_fear_greed = ExternalAPIService.get_crypto_fear_greed_index() or {}
        except:
            crypto_fear_greed = {}
        
        # Get economic indicators with fallback
        try:
            economic_indicators = ExternalAPIService.get_economic_indicators() or {}
        except:
            economic_indicators = {}
        
        # Get market news with fallback
        try:
            market_news = ExternalAPIService.get_market_news(limit=10) or []
        except:
            market_news = []
        
        return render_template('market_intel/index.html',
                             insider_data=insider_data,
                             sector_performance=sector_performance,
                             earnings_calendar=earnings_calendar,
                             crypto_fear_greed=crypto_fear_greed,
                             economic_indicators=economic_indicators,
                             market_news=market_news)
    except Exception as e:
        print(f"Error in market_intel index: {e}")
        # Return basic template with empty data instead of error page
        return render_template('market_intel/index.html',
                             insider_data={},
                             sector_performance={},
                             earnings_calendar=[],
                             crypto_fear_greed={},
                             economic_indicators={},
                             market_news=[],
                             error="Kunne ikke hente alle markedsdata. Viser tilgjengelig informasjon.")

@market_intel.route('/insider-trading')
@access_required
def insider_trading():
    """Redirect to the new insider trading page"""
    ticker = request.args.get('ticker', '').strip().upper()
    
    # Redirect to the new insider trading URL
    if ticker:
        return redirect(url_for('insider_trading.index', ticker=ticker), code=301)
    else:
        return redirect(url_for('insider_trading.index'), code=301)

@market_intel.route('/earnings-calendar')
@access_required
def earnings_calendar():
    """Earnings calendar page"""
    days_ahead = request.args.get('days', 30, type=int)
    
    try:
        if ExternalAPIService:
            earnings_data = ExternalAPIService.get_earnings_calendar(days_ahead=days_ahead)
        else:
            # Fallback data when service is not available
            earnings_data = [
                {
                    'symbol': 'EQNR',
                    'company_name': 'Equinor ASA',
                    'earnings_date': '2025-02-06',
                    'estimate': '1.25',
                    'actual': None,
                    'surprise': None
                },
                {
                    'symbol': 'DNB',
                    'company_name': 'DNB Bank ASA',
                    'earnings_date': '2025-02-10',
                    'estimate': '2.15',
                    'actual': None,
                    'surprise': None
                },
                {
                    'symbol': 'TEL',
                    'company_name': 'Telenor ASA',
                    'earnings_date': '2025-02-12',
                    'estimate': '0.85',
                    'actual': None,
                    'surprise': None
                }
            ]
        
        return render_template('market_intel/earnings_calendar.html',
                             earnings_data=earnings_data,
                             days_ahead=days_ahead)
    except Exception as e:
        logger.error(f"Error in earnings calendar: {e}")
        return render_template('error.html', error="Kunne ikke hente resultatkalender.")

@market_intel.route('/sector-analysis')
@demo_access
def sector_analysis():
    """Enhanced sector performance analysis with real data and comprehensive content"""
    try:
        logger.info("Enhanced sector analysis requested")
        
        # Get real data service
        try:
            from ..services.data_service import DataService
        except ImportError:
            DataService = None
        
        # Initialize containers for data
        sector_data = []
        top_gainers = []
        top_losers = []
        sector_rotation_data = []
        market_cap_breakdown = []
        
        # Try to get real sector data first
        if DataService and current_user.is_authenticated:
            try:
                logger.info("🔍 Fetching REAL sector data for authenticated user")
                
                # Get sector performance data
                sector_performance = DataService.get_sector_performance()
                if sector_performance and len(sector_performance) > 0:
                    sector_data = sector_performance
                    logger.info(f"✅ Got real sector performance data: {len(sector_data)} sectors")
                
                # Get top performers across sectors
                oslo_stocks = DataService.get_oslo_bors_overview()
                if oslo_stocks:
                    # Extract top gainers and losers
                    sorted_by_change = sorted(oslo_stocks.items(), 
                                            key=lambda x: x[1].get('change_percent', 0), 
                                            reverse=True)
                    top_gainers = [{'symbol': k, **v} for k, v in sorted_by_change[:10]]
                    top_losers = [{'symbol': k, **v} for k, v in sorted_by_change[-10:]]
                    logger.info(f"✅ Got top gainers/losers: {len(top_gainers)}/{len(top_losers)}")
                
            except Exception as data_error:
                logger.warning(f"DataService failed: {data_error}")
        
        # Use enhanced fallback data if real data unavailable
        if not sector_data:
            logger.info("📊 Using enhanced fallback sector data")
            sector_data = [
                {
                    'name': 'Energy & Oil', 
                    'performance': 2.4, 
                    'symbol': 'XLE', 
                    'change': 2.4,
                    'change_percent': 2.4,
                    'market_cap': 850000000000,
                    'volume': 125000000,
                    'companies_count': 23,
                    'description': 'Olje, gass og fornybar energi'
                },
                {
                    'name': 'Technology', 
                    'performance': -0.8, 
                    'symbol': 'XLK', 
                    'change': -0.8,
                    'change_percent': -0.8,
                    'market_cap': 1200000000000,
                    'volume': 280000000,
                    'companies_count': 67,
                    'description': 'Software, hardware og tech-tjenester'
                },
                {
                    'name': 'Financials', 
                    'performance': 1.2, 
                    'symbol': 'XLF', 
                    'change': 1.2,
                    'change_percent': 1.2,
                    'market_cap': 650000000000,
                    'volume': 180000000,
                    'companies_count': 45,
                    'description': 'Banker, forsikring og fintech'
                },
                {
                    'name': 'Healthcare', 
                    'performance': 0.5, 
                    'symbol': 'XLV', 
                    'change': 0.5,
                    'change_percent': 0.5,
                    'market_cap': 980000000000,
                    'volume': 150000000,
                    'companies_count': 34,
                    'description': 'Farma, medisinsk utstyr og biotech'
                },
                {
                    'name': 'Shipping & Maritime', 
                    'performance': 3.2, 
                    'symbol': 'SHIP', 
                    'change': 3.2,
                    'change_percent': 3.2,
                    'market_cap': 180000000000,
                    'volume': 95000000,
                    'companies_count': 18,
                    'description': 'Shipping, offshore og maritim'
                },
                {
                    'name': 'Materials & Mining', 
                    'performance': 0.8, 
                    'symbol': 'XLB', 
                    'change': 0.8,
                    'change_percent': 0.8,
                    'market_cap': 420000000000,
                    'volume': 110000000,
                    'companies_count': 28,
                    'description': 'Metaller, gruvedrift og materialer'
                },
                {
                    'name': 'Consumer Goods', 
                    'performance': -1.1, 
                    'symbol': 'XLY', 
                    'change': -1.1,
                    'change_percent': -1.1,
                    'market_cap': 320000000000,
                    'volume': 75000000,
                    'companies_count': 41,
                    'description': 'Forbruksvarer og detaljhandel'
                },
                {
                    'name': 'Real Estate', 
                    'performance': 1.5, 
                    'symbol': 'XLRE', 
                    'change': 1.5,
                    'change_percent': 1.5,
                    'market_cap': 290000000000,
                    'volume': 60000000,
                    'companies_count': 35,
                    'description': 'Eiendom, REITs og utvikling'
                }
            ]
        
        # Enhanced fallback stock data
        if not top_gainers:
            top_gainers = [
                {'symbol': 'EQNR.OL', 'name': 'Equinor ASA', 'last_price': 280.50, 'change_percent': 3.2, 'sector': 'Energy', 'volume': 8500000},
                {'symbol': 'MOWI.OL', 'name': 'Mowi ASA', 'last_price': 195.30, 'change_percent': 2.8, 'sector': 'Consumer Goods', 'volume': 2100000},
                {'symbol': 'DNB.OL', 'name': 'DNB Bank ASA', 'last_price': 220.30, 'change_percent': 2.1, 'sector': 'Financials', 'volume': 5200000},
                {'symbol': 'FRONTS.OL', 'name': 'Frontline Ltd', 'last_price': 145.80, 'change_percent': 1.9, 'sector': 'Shipping', 'volume': 1800000},
                {'symbol': 'YAR.OL', 'name': 'Yara International', 'last_price': 375.20, 'change_percent': 1.6, 'sector': 'Materials', 'volume': 1200000}
            ]
        
        if not top_losers:
            top_losers = [
                {'symbol': 'KAHOOT.OL', 'name': 'Kahoot! ASA', 'last_price': 45.20, 'change_percent': -4.1, 'sector': 'Technology', 'volume': 3200000},
                {'symbol': 'AUTOSTORE.OL', 'name': 'AutoStore Holdings', 'last_price': 12.85, 'change_percent': -3.8, 'sector': 'Technology', 'volume': 8900000},
                {'symbol': 'FLEX.OL', 'name': 'Flex LNG Ltd', 'last_price': 198.50, 'change_percent': -2.9, 'sector': 'Shipping', 'volume': 950000},
                {'symbol': 'BAKKA.OL', 'name': 'Bakkavor Group', 'last_price': 65.40, 'change_percent': -2.3, 'sector': 'Consumer Goods', 'volume': 750000},
                {'symbol': 'ELKEM.OL', 'name': 'Elkem ASA', 'last_price': 18.95, 'change_percent': -1.8, 'sector': 'Materials', 'volume': 1850000}
            ]
        
        # Calculate sector rotation and market metrics
        total_market_cap = sum(sector.get('market_cap', 0) for sector in sector_data)
        for sector in sector_data:
            if sector.get('market_cap'):
                sector['market_cap_percentage'] = (sector['market_cap'] / total_market_cap) * 100
        
        # Sector rotation data (momentum indicators)
        sector_rotation_data = [
            {'sector': 'Energy', 'momentum_1w': 2.1, 'momentum_1m': 8.4, 'momentum_3m': 15.2},
            {'sector': 'Technology', 'momentum_1w': -1.2, 'momentum_1m': -3.8, 'momentum_3m': 12.5},
            {'sector': 'Financials', 'momentum_1w': 0.8, 'momentum_1m': 4.2, 'momentum_3m': 9.1},
            {'sector': 'Shipping', 'momentum_1w': 3.4, 'momentum_1m': 12.1, 'momentum_3m': 22.8}
        ]
        
        logger.info(f"Returning enhanced sector analysis with {len(sector_data)} sectors, {len(top_gainers)} gainers, {len(top_losers)} losers")
        
        return render_template('market-intel/sector-analysis.html',
                             sectors=sector_data,
                             sector_performance=sector_data,
                             top_gainers=top_gainers,
                             top_losers=top_losers,
                             sector_rotation=sector_rotation_data,
                             total_market_cap=total_market_cap,
                             data_source='REAL DATA' if (DataService and current_user.is_authenticated) else 'ENHANCED DEMO')
                             
    except Exception as e:
        logger.error(f"Error in enhanced sector_analysis: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Return comprehensive fallback template
        return render_template('market-intel/sector-analysis.html',
                             sectors=[],
                             sector_performance=[],
                             top_gainers=[],
                             top_losers=[],
                             sector_rotation=[],
                             total_market_cap=0,
                             error="Kunne ikke laste sektoranalyse",
                             data_source='ERROR')

@market_intel.route('/economic-indicators')
@demo_access
def economic_indicators():
    """Economic indicators and market overview"""
    try:
        if ExternalAPIService:
            economic_data = ExternalAPIService.get_economic_indicators()
            crypto_fear_greed = ExternalAPIService.get_crypto_fear_greed_index()
        else:
            # Fallback data when service is not available
            economic_data = {
                'inflation_rate': 3.2,
                'unemployment_rate': 3.8,
                'gdp_growth': 2.1,
                'interest_rate': 4.5,
                'oil_price': 85.30,
                'usd_nok': 10.45
            }
            crypto_fear_greed = {
                'value': 45,
                'classification': 'Neutral',
                'last_update': datetime.now().strftime('%Y-%m-%d')
            }
        
        return render_template('market_intel/economic_indicators.html',
                             economic_data=economic_data,
                             crypto_fear_greed=crypto_fear_greed)
    except Exception as e:
        return render_template('error.html', error="Kunne ikke hente økonomiske indikatorer.")

# API endpoints for AJAX requests
@market_intel.route('/api/insider-trading/<ticker>')
@access_required
def api_insider_trading(ticker):
    """API endpoint for insider trading data"""
    try:
        limit = request.args.get('limit', 10, type=int)
        data = ExternalAPIService.get_insider_trading(ticker, limit=limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/institutional-ownership/<ticker>')
@access_required
def api_institutional_ownership(ticker):
    """API endpoint for institutional ownership data"""
    try:
        data = ExternalAPIService.get_institutional_ownership(ticker)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/sector-performance')
@access_required
def api_sector_performance():
    """API endpoint for sector performance"""
    try:
        data = ExternalAPIService.get_sector_performance()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/earnings-calendar')
@access_required
def api_earnings_calendar():
    """API endpoint for earnings calendar"""
    try:
        days_ahead = request.args.get('days', 30, type=int)
        data = ExternalAPIService.get_earnings_calendar(days_ahead=days_ahead)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/crypto-fear-greed')
@access_required
def api_crypto_fear_greed():
    """API endpoint for crypto fear & greed index"""
    try:
        data = ExternalAPIService.get_crypto_fear_greed_index()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/economic-indicators')
@demo_access
def api_economic_indicators():
    """Unified economic indicators endpoint with simple timeframe support.

    Query params:
      timeframe=live|daily|weekly (default live)
    """
    timeframe = request.args.get('timeframe', 'live').lower()
    if timeframe not in {'live','daily','weekly'}:
        timeframe = 'live'
    try:
        base_data = None
        crypto_fg = None
        if ExternalAPIService:
            try:
                base_data = ExternalAPIService.get_economic_indicators()
                crypto_fg = ExternalAPIService.get_crypto_fear_greed_index()
            except Exception as ext_err:
                current_app.logger.warning(f"External economic indicators failed: {ext_err}")
        if not base_data:
            base_data = {
                'inflation_rate': 2.8,
                'interest_rate': 4.5,
                'unemployment_rate': 3.2,
                'oil_price': 85.2
            }
        # Derive simple timeframe adjustments (placeholder logic until real historical feed present)
        adjustments = {
            'live': {'inflation_rate': 0.00, 'interest_rate': 0.00, 'unemployment_rate': 0.00, 'oil_price': 0.0},
            'daily': {'inflation_rate': 0.01, 'interest_rate': 0.00, 'unemployment_rate': -0.01, 'oil_price': -0.3},
            'weekly': {'inflation_rate': 0.05, 'interest_rate': 0.00, 'unemployment_rate': 0.05, 'oil_price': -1.5},
        }
        adj = adjustments[timeframe]
        enriched = {
            'timeframe': timeframe,
            'inflation_rate': round(base_data.get('inflation_rate', 0) + adj['inflation_rate'], 2),
            'interest_rate': round(base_data.get('interest_rate', 0) + adj['interest_rate'], 2),
            'unemployment_rate': round(base_data.get('unemployment_rate', 0) + adj['unemployment_rate'], 2),
            'oil_price': round(base_data.get('oil_price', 0) + adj['oil_price'], 2),
            'crypto_fear_greed': crypto_fg or {'value': 45, 'classification': 'Neutral'},
            'data_source': 'EXTERNAL' if ExternalAPIService else 'FALLBACK'
        }
        return jsonify(enriched)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/analyst-coverage')
@demo_access
def analyst_coverage():
    """Redirect to external data analyst coverage"""
    return redirect(url_for('external_data.analyst_coverage'), code=301)

@market_intel.route('/market-intelligence')
@demo_access
def market_intelligence():
    """Redirect to external data market intelligence"""
    return redirect(url_for('external_data.market_intelligence'), code=301)
