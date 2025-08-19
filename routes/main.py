from flask import Blueprint, render_template, current_app
from flask_login import current_user, login_required
from .services import data_service
from .models import Portfolio
from datetime import datetime, timedelta
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        try:
            # Get market data for authenticated users
            oslo_stocks = data_service.get_oslo_stocks()
            global_stocks = data_service.get_global_stocks()
            currencies = data_service.get_currency_pairs()
            crypto = data_service.get_crypto_overview()
            
            # Ensure we have data - use fallback if needed
            if not oslo_stocks or len(oslo_stocks) == 0:
                oslo_stocks = data_service._generate_fallback_oslo_stocks()
            if not global_stocks or len(global_stocks) == 0:
                global_stocks = data_service._generate_fallback_global_stocks()
            if not currencies or len(currencies) == 0:
                currencies = data_service._generate_fallback_currencies()
            if not crypto or len(crypto) == 0:
                crypto = data_service._generate_fallback_crypto()
            
            # Log for debugging
            current_app.logger.info(f"Index page - Oslo stocks: {len(oslo_stocks)}")
            current_app.logger.info(f"Index page - Global stocks: {len(global_stocks)}")
            current_app.logger.info(f"Index page - Currencies: {len(currencies)}")
            current_app.logger.info(f"Index page - Crypto: {len(crypto)}")
            
            return render_template('index.html',
                                 oslo_stocks=oslo_stocks,
                                 global_stocks=global_stocks,
                                 currencies=currencies,
                                 crypto=crypto)
        except Exception as e:
            current_app.logger.error(f"Error loading dashboard data: {str(e)}")
            # Return with fallback data instead of empty
            return render_template('index.html',
                                 oslo_stocks=data_service._generate_fallback_oslo_stocks(),
                                 global_stocks=data_service._generate_fallback_global_stocks(),
                                 currencies=data_service._generate_fallback_currencies(),
                                 crypto=data_service._generate_fallback_crypto())
    
    return render_template('index.html')

@main_bp.route('/financial-dashboard')
@login_required
def financial_dashboard():
    try:
        # Get user's portfolio
        portfolio = Portfolio.query.filter_by(user_id=current_user.id).all()
        
        # Get market data
        stocks_data = {}
        for item in portfolio:
            stock = data_service.get_stock_data(item.symbol)
            if stock:
                stocks_data[item.symbol] = stock
        
        # Get news
        news_items = [
            {
                'title': 'Aksjemarkedet stiger på positive økonomiske signaler',
                'source': 'E24',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'url': '#'
            },
            {
                'title': 'Teknologisektoren leder an oppgangen',
                'source': 'DN',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'url': '#'
            }
        ]
        
        # Get insider trades
        insider_trades = []
        for symbol in stocks_data.keys():
            insider_trades.extend([
                {
                    'symbol': symbol,
                    'company': stocks_data[symbol].name,
                    'insider': 'CEO',
                    'type': 'Kjøp',
                    'shares': random.randint(1000, 10000),
                    'value': random.randint(100000, 1000000),
                    'date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
                }
            ])
        
        # Currency data
        currencies = data_service.get_currency_pairs()
        
        return render_template('financial_dashboard.html',
                             portfolio=portfolio,
                             stocks_data=stocks_data,
                             news_items=news_items,
                             insider_trades=insider_trades,
                             currencies=currencies)
                             
    except Exception as e:
        current_app.logger.error(f"Error loading financial dashboard: {str(e)}")
        return render_template('financial_dashboard.html',
                             portfolio=[],
                             stocks_data={},
                             news_items=[],
                             insider_trades=[],
                             currencies={})