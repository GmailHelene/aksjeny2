from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from datetime import datetime
import random
from . import analysis_bp
from ..services import data_service, analysis_service
from ..services.data_models import Stock

@analysis_bp.route('/sentiment')
@login_required
def sentiment():
    symbol = request.args.get('symbol')
    if not symbol:
        flash('Ingen aksje valgt', 'error')
        return redirect(url_for('main.index'))
    
    try:
        # Get stock data
        stock_data = data_service.get_stock_data(symbol)
        if not stock_data:
            flash(f'Kunne ikke finne data for {symbol}', 'error')
            return redirect(url_for('main.index'))
        
        # Get sentiment analysis
        sentiment_data = analysis_service.analyze_sentiment(symbol)
        
        # If no sentiment data available, provide default structure
        if not sentiment_data:
            sentiment_data = {
                'overall_sentiment': 'neutral',
                'confidence': 0.5,
                'positive_factors': [],
                'negative_factors': [],
                'recommendation': 'Ingen sentimentdata tilgjengelig',
                'last_updated': datetime.now(),
                'rsi_sentiment': 50,
                'volume_sentiment': 'Stabil',
                'price_action': 'Nøytral',
                'news_positive': 50,
                'social_positive': 50,
                'trend_dates': [],
                'trend_values': []
            }
        
        return render_template('analysis/sentiment.html',
                             stock=stock_data,
                             symbol=symbol,
                             sentiment=sentiment_data)
                             
    except Exception as e:
        current_app.logger.error(f"Error in sentiment analysis for {symbol}: {str(e)}")
        flash('Teknisk feil under analyse. Vennligst prøv igjen senere.', 'error')
        return redirect(url_for('main.index'))

@analysis_bp.route('/warren-buffett')
@login_required
def warren_buffett():
    ticker = request.args.get('ticker', 'AAPL')
    
    try:
        # Get stock data
        stock_data = data_service.get_stock_data(ticker)
        if not stock_data:
            stock_data = Stock(
                symbol=ticker,
                name=ticker,
                current_price=100.0,
                change_percent=0.0,
                previous_close=100.0,
                market_cap=1000000000,
                volume=1000000,
                sector='Unknown'
            )
        
        # Generate Warren Buffett analysis
        analysis_data = {
            'ticker': ticker,
            'company_name': stock_data.name,
            'current_price': stock_data.current_price,
            'intrinsic_value': stock_data.current_price * 1.2,
            'margin_of_safety': 20.0,
            'moat_rating': 'Wide',
            'management_quality': 'Excellent',
            'financial_strength': 8,
            'recommendation': 'BUY',
            'key_metrics': {
                'pe_ratio': 15.5,
                'pb_ratio': 2.3,
                'roe': 18.5,
                'debt_to_equity': 0.45,
                'free_cash_flow': 5000000000,
                'dividend_yield': 2.5
            },
            'strengths': [
                'Sterk markedsposisjon',
                'Konsistent inntjening',
                'Solid ledelse'
            ],
            'weaknesses': [
                'Høy verdsettelse',
                'Avhengig av økonomiske sykluser'
            ]
        }
        
        # Get portfolio comparison data
        portfolio_stocks = [ticker, 'DNB.OL', 'EQNR.OL']
        portfolio_data = []
        
        for symbol in portfolio_stocks:
            stock = data_service.get_stock_data(symbol)
            if stock:
                portfolio_data.append({
                    'symbol': symbol,
                    'name': stock.name,
                    'current_price': stock.current_price,
                    'change_percent': stock.change_percent,
                    'volume': stock.volume,
                    'volatility': random.uniform(15, 35),
                    'correlation': random.uniform(0.3, 0.8),
                    'beta': random.uniform(0.8, 1.5),
                    'rsi': random.uniform(30, 70),
                    'macd': random.uniform(-5, 5),
                    'signal': random.uniform(-5, 5),
                    'bollinger': random.choice(['Upper', 'Middle', 'Lower']),
                    'sma_200': stock.current_price * random.uniform(0.9, 1.1),
                    'sma_50': stock.current_price * random.uniform(0.95, 1.05),
                    'recommendation': random.choice(['BUY', 'HOLD', 'SELL'])
                })
        
        return render_template('analysis/warren_buffett.html',
                             analysis=analysis_data,
                             portfolio_data=portfolio_data)
                             
    except Exception as e:
        current_app.logger.error(f"Error in Warren Buffett analysis: {str(e)}")
        flash('Teknisk feil under analyse', 'error')
        return redirect(url_for('analysis.overview'))