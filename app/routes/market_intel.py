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
@demo_access
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
        earnings_data = ExternalAPIService.get_earnings_calendar(days_ahead=days_ahead)
        
        return render_template('market_intel/earnings_calendar.html',
                             earnings_data=earnings_data,
                             days_ahead=days_ahead)
    except Exception as e:
        return render_template('error.html', error="Kunne ikke hente resultatkalender.")

@market_intel.route('/sector-analysis')
@access_required
def sector_analysis():
    """Sector performance analysis"""
    try:
        sector_data = ExternalAPIService.get_sector_performance()
        screener_data = ExternalAPIService.get_stock_screener(
            market_cap_min=1000000000,  # 1B+ market cap
            volume_min=1000000          # 1M+ volume
        )
        
        return render_template('market_intel/sector_analysis.html',
                             sector_data=sector_data,
                             screener_data=screener_data[:20])  # Top 20
    except Exception as e:
        return render_template('error.html', error="Kunne ikke hente sektoranalyse.")

@market_intel.route('/economic-indicators')
@access_required
def economic_indicators():
    """Economic indicators and market overview"""
    try:
        economic_data = ExternalAPIService.get_economic_indicators()
        crypto_fear_greed = ExternalAPIService.get_crypto_fear_greed_index()
        
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
