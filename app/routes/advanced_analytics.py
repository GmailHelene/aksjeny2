"""
Advanced Analytics Blueprint
Handles ML predictions, portfolio optimization, and risk management
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from ..utils.access_control import demo_access  # Import demo_access
import logging

logger = logging.getLogger(__name__)

# Create blueprint
advanced_analytics = Blueprint('advanced_analytics', __name__)

@advanced_analytics.route('/')
@demo_access  # Changed from @login_required to @demo_access
def index():
    """Advanced analytics dashboard"""
    return render_template('advanced_analytics.html')

@advanced_analytics.route('/dashboard')
@demo_access  # Changed from @login_required to @demo_access  
def dashboard():
    """Advanced analytics dashboard (alias for index)"""
    return render_template('advanced_analytics.html')

@advanced_analytics.route('/ml-predictions')
@demo_access  # Changed from @login_required to @demo_access
def ml_predictions():
    """ML predictions page"""
    return render_template('advanced_analytics.html', active_tab='ml-predictions')

@advanced_analytics.route('/portfolio-optimization')
@demo_access  # Changed from @login_required to @demo_access
def portfolio_optimization():
    """Portfolio optimization page"""
    return render_template('advanced_analytics.html', active_tab='portfolio-optimization')

@advanced_analytics.route('/risk-management')
@demo_access  # Changed from @login_required to @demo_access
def risk_management():
    """Risk management page"""
    return render_template('advanced_analytics.html', active_tab='risk-management')

# API Endpoints for Advanced Analytics
@advanced_analytics.route('/generate-prediction', methods=['POST'])
@demo_access  # Changed from @login_required to @demo_access
def generate_prediction():
    """Generate AI prediction for a ticker"""
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()
        
        if not ticker:
            return jsonify({'success': False, 'error': 'Ticker is required'})
        
        # Mock prediction for now - can be enhanced with real ML later
        import random
        price_change = round(random.uniform(-10, 15), 2)
        confidence = round(random.uniform(65, 95), 1)
        
        prediction_text = f"AI-prediksjon for {ticker}: Forventet prisendring {'+' if price_change > 0 else ''}{price_change}% over neste 30 dager (konfidensgrad: {confidence}%)"
        
        return jsonify({
            'success': True,
            'prediction': prediction_text,  # Change 'result' to 'prediction' to match JavaScript
            'ticker': ticker,
            'price_change': price_change,
            'confidence': confidence
        })
    except Exception as e:
        logger.error(f"Error generating prediction: {e}")
        return jsonify({'success': False, 'error': str(e)})

@advanced_analytics.route('/batch-predictions', methods=['POST'])
@demo_access  # Changed from @login_required to @demo_access  
def batch_predictions():
    """Generate batch predictions for multiple tickers"""
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        
        if not tickers:
            return jsonify({'success': False, 'error': 'Tickers list is required'})
        
        # Mock batch predictions
        import random
        predictions = {}
        for ticker in tickers:
            price_change = round(random.uniform(-8, 12), 2)
            predictions[ticker] = price_change
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'generated_at': 'now'
        })
    except Exception as e:
        logger.error(f"Error generating batch predictions: {e}")
        return jsonify({'success': False, 'error': str(e)})

@advanced_analytics.route('/market-analysis', methods=['POST'])
@demo_access  # Changed from @login_required to @demo_access
def market_analysis():
    """Generate market analysis"""
    try:
        # Mock market analysis
        import random
        
        sentiments = ['Bullish', 'Bearish', 'Neutral', 'Caution']
        volatility_levels = ['Low', 'Moderate', 'High']
        
        sentiment = random.choice(sentiments)
        volatility = random.choice(volatility_levels)
        
        analysis = f"Nåværende markedssentiment: {sentiment}. Volatilitetsnivå: {volatility}. "
        
        if sentiment == 'Bullish':
            analysis += "Markedet viser positive signaler med økt investor-optimisme."
        elif sentiment == 'Bearish':
            analysis += "Markedet viser negative signaler med økt bekymring blant investorer."
        elif sentiment == 'Neutral':
            analysis += "Markedet er balansert med blandede signaler."
        else:
            analysis += "Markedet viser forsiktighet med økt usikkerhet."
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'sentiment': sentiment,
            'volatility': volatility,
            'timestamp': 'now'
        })
    except Exception as e:
        logger.error(f"Error generating market analysis: {e}")
        return jsonify({'success': False, 'error': str(e)})

@advanced_analytics.route('/api/ml/predict/<symbol>')
@demo_access  # Changed from @login_required to @demo_access
def api_ml_predict(symbol):
    """ML prediction API endpoint"""
    try:
        days = request.args.get('days', 30, type=int)
        # Generate mock prediction data
        import random
        
        # Create deterministic but varied predictions based on symbol
        symbol_hash = sum(ord(c) for c in symbol)
        random.seed(symbol_hash)
        
        # Generate price predictions
        base_price = 100 + (symbol_hash % 200)
        predictions = []
        
        for i in range(days):
            # Generate realistic price movement
            daily_change = random.uniform(-0.05, 0.05)  # -5% to +5% daily
            if i == 0:
                price = base_price
            else:
                price = predictions[-1]['price'] * (1 + daily_change)
            
            predictions.append({
                'date': f"2025-08-{26+i}" if i < 6 else f"2025-09-{i-5}",
                'price': round(price, 2),
                'confidence': round(random.uniform(0.6, 0.9), 2)
            })
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'predictions': predictions,
            'model_accuracy': round(random.uniform(0.75, 0.92), 2),
            'trend': 'bullish' if predictions[-1]['price'] > base_price else 'bearish'
        })
        
    except Exception as e:
        logger.error(f"Error in ML prediction API: {e}")
        return jsonify({
            'success': False,
            'error': 'Prediction temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/portfolio/optimize', methods=['POST'])
@demo_access  # Changed from @login_required to @demo_access
def api_portfolio_optimize():
    """Portfolio optimization API endpoint"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        amount = data.get('amount', 100000)
        
        # Generate mock optimization results
        import random
        random.seed(sum(ord(c) for s in symbols for c in s))
        
        allocations = []
        remaining = 100
        
        for i, symbol in enumerate(symbols):
            if i == len(symbols) - 1:
                allocation = remaining
            else:
                allocation = random.randint(5, min(40, remaining - 5*(len(symbols)-i-1)))
                remaining -= allocation
            
            allocations.append({
                'symbol': symbol,
                'allocation_percent': allocation,
                'allocation_amount': round(amount * allocation / 100, 2),
                'expected_return': round(random.uniform(0.08, 0.18), 3),
                'risk_score': round(random.uniform(0.1, 0.8), 2)
            })
        
        return jsonify({
            'success': True,
            'optimized_portfolio': allocations,
            'expected_annual_return': round(random.uniform(0.10, 0.15), 3),
            'portfolio_risk': round(random.uniform(0.15, 0.25), 3),
            'sharpe_ratio': round(random.uniform(0.8, 1.5), 2)
        })
        
    except Exception as e:
        logger.error(f"Error in portfolio optimization API: {e}")
        return jsonify({
            'success': False,
            'error': 'Optimization temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/risk/analysis', methods=['POST'])
@login_required
def api_risk_analysis():
    """Risk analysis API endpoint"""
    try:
        data = request.get_json()
        portfolio = data.get('portfolio', [])
        
        # Generate mock risk analysis
        import random
        
        risk_metrics = {
            'var_95': round(random.uniform(0.15, 0.35), 3),
            'var_99': round(random.uniform(0.25, 0.45), 3),
            'expected_shortfall': round(random.uniform(0.20, 0.40), 3),
            'max_drawdown': round(random.uniform(0.10, 0.30), 3),
            'volatility': round(random.uniform(0.15, 0.25), 3),
            'beta': round(random.uniform(0.8, 1.2), 2),
            'correlation_sp500': round(random.uniform(0.6, 0.9), 2)
        }
        
        return jsonify({
            'success': True,
            'risk_metrics': risk_metrics,
            'risk_level': 'Moderate' if risk_metrics['volatility'] < 0.2 else 'High',
            'recommendations': [
                'Consider diversifying across sectors',
                'Monitor correlation with market index',
                'Review position sizing'
            ]
        })
        
    except Exception as e:
        logger.error(f"Error in risk analysis API: {e}")
        return jsonify({
            'success': False,
            'error': 'Risk analysis temporarily unavailable'
        }), 500

# Error handlers for this blueprint
@advanced_analytics.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors within advanced analytics"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Siden ble ikke funnet"), 404

@advanced_analytics.errorhandler(500)
def internal_error(error):
    """Handle 500 errors within advanced analytics"""
    logger.error(f"Advanced analytics internal error: {error}")
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Intern serverfeil"), 500
