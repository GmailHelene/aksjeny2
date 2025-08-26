"""
Advanced Analytics Blueprint
Handles ML predictions, portfolio optimization, and risk management
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import logging

logger = logging.getLogger(__name__)

# Create blueprint
advanced_analytics = Blueprint('advanced_analytics', __name__)

@advanced_analytics.route('/')
@login_required
def index():
    """Advanced analytics dashboard"""
    return render_template('advanced_analytics.html')

@advanced_analytics.route('/dashboard')
@login_required  
def dashboard():
    """Advanced analytics dashboard (alias for index)"""
    return render_template('advanced_analytics.html')

@advanced_analytics.route('/ml-predictions')
@login_required
def ml_predictions():
    """ML predictions page"""
    return render_template('advanced_analytics.html', active_tab='ml-predictions')

@advanced_analytics.route('/portfolio-optimization')
@login_required
def portfolio_optimization():
    """Portfolio optimization page"""
    return render_template('advanced_analytics.html', active_tab='portfolio-optimization')

@advanced_analytics.route('/risk-management')
@login_required
def risk_management():
    """Risk management page"""
    return render_template('advanced_analytics.html', active_tab='risk-management')

# API Endpoints for Advanced Analytics
@advanced_analytics.route('/api/ml/predict/<symbol>')
@login_required
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
            'prediction': {
                'symbol': symbol,
                'current_price': base_price,
                'predicted_price': predictions[-1]['price'],
                'price_change_percent': ((predictions[-1]['price'] - base_price) / base_price) * 100,
                'confidence': predictions[-1]['confidence'],
                'trend': 'bullish' if predictions[-1]['price'] > base_price else 'bearish',
                'volatility': random.uniform(0.15, 0.35)
            },
            'predictions': predictions,
            'model_accuracy': round(random.uniform(0.75, 0.92), 2)
        })
        
    except Exception as e:
        logger.error(f"Error in ML prediction API: {e}")
        return jsonify({
            'success': False,
            'message': 'Prediction temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/portfolio/optimize', methods=['POST'])
@login_required
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
            'optimization': {
                'optimal_weights': dict(zip(symbols, [a['allocation_percent']/100 for a in allocations])),
                'expected_return': round(random.uniform(0.10, 0.15), 3),
                'volatility': round(random.uniform(0.15, 0.25), 3),
                'sharpe_ratio': round(random.uniform(0.8, 1.5), 2)
            },
            'allocations': allocations
        })
        
    except Exception as e:
        logger.error(f"Error in portfolio optimization API: {e}")
        return jsonify({
            'success': False,
            'message': 'Optimization temporarily unavailable'
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
            'message': 'Risk analysis temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/ml/batch-predict', methods=['POST'])
@login_required
def api_ml_batch_predict():
    """Batch ML prediction API endpoint"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        days = data.get('days', 30)
        
        predictions = {}
        for symbol in symbols:
            # Generate mock prediction for each symbol
            symbol_hash = sum(ord(c) for c in symbol)
            import random
            random.seed(symbol_hash)
            
            base_price = 100 + (symbol_hash % 200)
            predicted_price = base_price * random.uniform(0.85, 1.15)
            
            predictions[symbol] = {
                'current_price': base_price,
                'predicted_price': round(predicted_price, 2),
                'price_change_percent': round(((predicted_price - base_price) / base_price) * 100, 2),
                'confidence': round(random.uniform(0.6, 0.9), 2),
                'trend': 'bullish' if predicted_price > base_price else 'bearish'
            }
        
        return jsonify({
            'success': True,
            'predictions': predictions
        })
        
    except Exception as e:
        logger.error(f"Error in batch prediction API: {e}")
        return jsonify({
            'success': False,
            'message': 'Batch prediction temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/ml/market-analysis')
@login_required
def api_market_analysis():
    """Market analysis API endpoint"""
    try:
        import random
        
        market_data = {
            'overall_sentiment': random.choice(['bullish', 'bearish', 'neutral']),
            'market_volatility': round(random.uniform(0.15, 0.35), 3),
            'fear_greed_index': random.randint(20, 80),
            'sector_performance': {
                'Technology': round(random.uniform(-5, 10), 2),
                'Healthcare': round(random.uniform(-3, 8), 2),
                'Finance': round(random.uniform(-4, 6), 2),
                'Energy': round(random.uniform(-8, 12), 2),
                'Consumer': round(random.uniform(-2, 5), 2)
            },
            'market_trends': [
                'Increased tech sector volatility',
                'Rising interest rate concerns',
                'Global supply chain improvements'
            ]
        }
        
        return jsonify({
            'success': True,
            'analysis': market_data
        })
        
    except Exception as e:
        logger.error(f"Error in market analysis API: {e}")
        return jsonify({
            'success': False,
            'message': 'Market analysis temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/portfolio/efficient-frontier', methods=['POST'])
@login_required
def api_efficient_frontier():
    """Efficient frontier API endpoint"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        num_portfolios = data.get('num_portfolios', 10000)
        
        import random
        
        # Generate mock efficient frontier data
        frontier_data = []
        for i in range(50):  # 50 points on the frontier
            risk = 0.1 + (i * 0.01)  # Risk from 10% to 60%
            ret = 0.05 + (risk * 0.8) + random.uniform(-0.02, 0.02)  # Return correlated with risk
            frontier_data.append({
                'risk': round(risk, 3),
                'return': round(ret, 3)
            })
        
        return jsonify({
            'success': True,
            'frontier': {
                'data': frontier_data,
                'optimal_portfolio': {
                    'risk': round(random.uniform(0.15, 0.25), 3),
                    'return': round(random.uniform(0.10, 0.15), 3),
                    'sharpe_ratio': round(random.uniform(0.8, 1.5), 2)
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error in efficient frontier API: {e}")
        return jsonify({
            'success': False,
            'message': 'Efficient frontier generation temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/portfolio/rebalance', methods=['POST'])
@login_required
def api_portfolio_rebalance():
    """Portfolio rebalancing API endpoint"""
    try:
        data = request.get_json()
        current_portfolio = data.get('current_portfolio', {})
        target_allocation = data.get('target_allocation', {})
        
        import random
        
        # Generate mock rebalancing recommendations
        rebalancing_actions = []
        for symbol in set(list(current_portfolio.keys()) + list(target_allocation.keys())):
            current = current_portfolio.get(symbol, 0)
            target = target_allocation.get(symbol, 0)
            difference = target - current
            
            if abs(difference) > 0.01:  # If difference > 1%
                action = 'buy' if difference > 0 else 'sell'
                rebalancing_actions.append({
                    'symbol': symbol,
                    'action': action,
                    'amount_percent': abs(difference) * 100,
                    'estimated_cost': random.uniform(100, 5000)
                })
        
        return jsonify({
            'success': True,
            'rebalancing': {
                'actions': rebalancing_actions,
                'total_transactions': len(rebalancing_actions),
                'estimated_cost': sum(action['estimated_cost'] for action in rebalancing_actions)
            }
        })
        
    except Exception as e:
        logger.error(f"Error in rebalancing API: {e}")
        return jsonify({
            'success': False,
            'message': 'Rebalancing analysis temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/risk/portfolio-risk', methods=['POST'])
@login_required
def api_portfolio_risk():
    """Portfolio risk calculation API endpoint"""
    try:
        data = request.get_json()
        portfolio = data.get('portfolio', {})
        timeframe = data.get('timeframe', 252)
        
        import random
        
        risk_metrics = {
            'volatility': round(random.uniform(0.15, 0.35), 3),
            'beta': round(random.uniform(0.7, 1.3), 2),
            'treynor_ratio': round(random.uniform(0.05, 0.15), 3),
            'max_drawdown': round(random.uniform(0.10, 0.40), 3),
            'var_95': round(random.uniform(0.15, 0.35), 3),
            'cvar_95': round(random.uniform(0.20, 0.45), 3),
            'information_ratio': round(random.uniform(-0.5, 1.0), 2),
            'tracking_error': round(random.uniform(0.05, 0.20), 3)
        }
        
        return jsonify({
            'success': True,
            'risk_metrics': risk_metrics
        })
        
    except Exception as e:
        logger.error(f"Error in portfolio risk calculation: {e}")
        return jsonify({
            'success': False,
            'message': 'Portfolio risk calculation temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/risk/var-analysis', methods=['POST'])
@login_required
def api_var_analysis():
    """VaR analysis API endpoint"""
    try:
        data = request.get_json()
        portfolio = data.get('portfolio', {})
        confidence_level = data.get('confidence_level', 0.95)
        time_horizon = data.get('time_horizon', 1)
        
        import random
        
        var_data = {
            'historical_var': round(random.uniform(0.15, 0.35), 3),
            'parametric_var': round(random.uniform(0.14, 0.36), 3),
            'monte_carlo_var': round(random.uniform(0.13, 0.37), 3),
            'expected_shortfall': round(random.uniform(0.20, 0.45), 3),
            'confidence_level': confidence_level,
            'time_horizon': time_horizon
        }
        
        return jsonify({
            'success': True,
            'var_analysis': var_data
        })
        
    except Exception as e:
        logger.error(f"Error in VaR analysis: {e}")
        return jsonify({
            'success': False,
            'message': 'VaR analysis temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/risk/stress-test', methods=['POST'])
@login_required
def api_stress_test():
    """Stress test API endpoint"""
    try:
        data = request.get_json()
        portfolio = data.get('portfolio', {})
        scenario = data.get('scenario', 'market_crash')
        
        import random
        
        scenario_impacts = {
            'market_crash': {'factor': -0.30, 'description': '30% market decline'},
            'interest_rate_shock': {'factor': -0.15, 'description': '2% interest rate increase'},
            'recession': {'factor': -0.25, 'description': 'Economic recession scenario'},
            'high_volatility': {'factor': -0.10, 'description': 'Increased market volatility'}
        }
        
        scenario_info = scenario_impacts.get(scenario, scenario_impacts['market_crash'])
        
        stress_results = {
            'scenario': scenario,
            'description': scenario_info['description'],
            'portfolio_impact': round(scenario_info['factor'] + random.uniform(-0.05, 0.05), 3),
            'value_at_risk': round(abs(scenario_info['factor']) * random.uniform(0.8, 1.2), 3),
            'recovery_time_days': random.randint(30, 365),
            'asset_impacts': {}
        }
        
        # Generate individual asset impacts
        for symbol in portfolio.keys():
            impact = scenario_info['factor'] + random.uniform(-0.1, 0.1)
            stress_results['asset_impacts'][symbol] = round(impact, 3)
        
        return jsonify({
            'success': True,
            'stress_test': stress_results
        })
        
    except Exception as e:
        logger.error(f"Error in stress test: {e}")
        return jsonify({
            'success': False,
            'message': 'Stress test temporarily unavailable'
        }), 500

@advanced_analytics.route('/api/risk/monte-carlo', methods=['POST'])
@login_required
def api_monte_carlo():
    """Monte Carlo simulation API endpoint"""
    try:
        data = request.get_json()
        portfolio = data.get('portfolio', {})
        simulations = data.get('simulations', 10000)
        time_horizon = data.get('time_horizon', 252)
        
        import random
        
        # Generate mock Monte Carlo results
        returns = []
        for _ in range(min(simulations, 1000)):  # Limit for performance
            annual_return = random.normalvariate(0.08, 0.20)  # 8% mean, 20% std
            returns.append(annual_return)
        
        returns.sort()
        
        def percentile(data, p):
            """Calculate percentile without numpy"""
            k = (len(data) - 1) * p / 100
            f = int(k)
            c = k - f
            if f == len(data) - 1:
                return data[f]
            return data[f] * (1 - c) + data[f + 1] * c
        
        mean_return = sum(returns) / len(returns)
        variance = sum((x - mean_return) ** 2 for x in returns) / len(returns)
        std_deviation = variance ** 0.5
        
        monte_carlo_data = {
            'simulations': len(returns),
            'time_horizon_days': time_horizon,
            'mean_return': round(mean_return, 4),
            'std_deviation': round(std_deviation, 4),
            'percentiles': {
                '5th': round(percentile(returns, 5), 4),
                '25th': round(percentile(returns, 25), 4),
                '50th': round(percentile(returns, 50), 4),
                '75th': round(percentile(returns, 75), 4),
                '95th': round(percentile(returns, 95), 4)
            },
            'probability_positive': round(sum(1 for r in returns if r > 0) / len(returns), 3),
            'probability_loss_5pct': round(sum(1 for r in returns if r < -0.05) / len(returns), 3),
            'probability_loss_10pct': round(sum(1 for r in returns if r < -0.10) / len(returns), 3)
        }
        
        return jsonify({
            'success': True,
            'monte_carlo': monte_carlo_data
        })
        
    except Exception as e:
        logger.error(f"Error in Monte Carlo simulation: {e}")
        return jsonify({
            'success': False,
            'message': 'Monte Carlo simulation temporarily unavailable'
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
