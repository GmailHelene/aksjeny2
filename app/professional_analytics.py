"""
Professional Analytics Dashboard for CMC Markets-style MT4 functionality
Integrates Expert Advisors, advanced orders, risk management, backtesting, indicators, alerts, and pattern recognition
"""

from flask import Blueprint, render_template, jsonify, request, session, current_app
from datetime import datetime, timedelta
import json
# import pandas as pd
# import numpy as np
from typing import Dict, List, Any, Optional
import logging

# Import our MT4-style modules
from .expert_advisor import expert_advisor_manager, ExpertAdvisor, EABacktester
from .advanced_orders import advanced_order_manager, Order, OrderType, OrderStatus
from .risk_management import risk_calculator, PositionSizer, MonteCarloSimulator
from .strategy_backtester import strategy_backtester, Trade, PerformanceMetrics
from .technical_indicators import technical_indicators, PatternRecognition, TradingSignals
from .alerts_system import alert_manager, Alert, AlertType
from .pattern_scanner import pattern_scanner, PatternResult

# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

class ProfessionalAnalyticsDashboard:
    """Professional analytics dashboard controller"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_dashboard_data(self, symbol: str = "EURUSD", timeframe: str = "1H") -> Dict[str, Any]:
        """Get comprehensive dashboard data for symbol"""
        
        try:
            # Generate sample market data (in production, this would come from your data provider)
            market_data = self._generate_sample_data(symbol, timeframe)
            
            # Get all analytics
            dashboard_data = {
                'symbol': symbol,
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat(),
                'market_data': self._format_market_data(market_data),
                'expert_advisors': self._get_ea_status(),
                'advanced_orders': self._get_advanced_orders(),
                'risk_metrics': self._get_risk_metrics(market_data),
                'technical_analysis': self._get_technical_analysis(market_data, symbol),
                'pattern_recognition': self._get_pattern_analysis(market_data, symbol),
                'performance_metrics': self._get_performance_metrics(),
                'alerts': self._get_active_alerts(),
                'market_overview': self._get_market_overview()
            }
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {'error': str(e)}
            
    def _generate_sample_data(self, symbol: str, timeframe: str, periods: int = 100) -> pd.DataFrame:
        """Generate sample market data for demonstration"""
        
        # Base price for different symbols
        base_prices = {
            'EURUSD': 1.0850,
            'GBPUSD': 1.2750,
            'USDJPY': 149.50,
            'AUDUSD': 0.6450,
            'USDCAD': 1.3680,
            'GOLD': 2045.50,
            'SP500': 4485.30,
            'BITCOIN': 43250.00
        }
        
        base_price = base_prices.get(symbol, 1.0000)
        
        # Generate realistic OHLCV data
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='1H')
        
        # Random walk with trend
        returns = np.random.normal(0.0001, 0.01, periods)
        prices = [base_price]
        
        for return_rate in returns[1:]:
            new_price = prices[-1] * (1 + return_rate)
            prices.append(new_price)
            
        # Generate OHLC from close prices
        data = []
        for i, (date, close) in enumerate(zip(dates, prices)):
            if i == 0:
                open_price = close
            else:
                open_price = prices[i-1]
                
            # Generate high/low with some volatility
            volatility = abs(np.random.normal(0, 0.005))
            high = max(open_price, close) * (1 + volatility)
            low = min(open_price, close) * (1 - volatility)
            
            # Volume (random but realistic)
            volume = np.random.randint(1000, 10000)
            
            data.append({
                'datetime': date,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
            
        df = pd.DataFrame(data)
        df.set_index('datetime', inplace=True)
        return df
        
    def _format_market_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Format market data for frontend"""
        
        latest = data.iloc[-1]
        previous = data.iloc[-2]
        
        change = latest['close'] - previous['close']
        change_pct = (change / previous['close']) * 100
        
        return {
            'current_price': round(latest['close'], 5),
            'open': round(latest['open'], 5),
            'high': round(latest['high'], 5),
            'low': round(latest['low'], 5),
            'volume': int(latest['volume']),
            'change': round(change, 5),
            'change_percent': round(change_pct, 2),
            'bid': round(latest['close'] - 0.0001, 5),  # Simplified spread
            'ask': round(latest['close'] + 0.0001, 5),
            'spread': 0.0002,
            'chart_data': [
                {
                    'time': int(row.name.timestamp()),
                    'open': round(row['open'], 5),
                    'high': round(row['high'], 5),
                    'low': round(row['low'], 5),
                    'close': round(row['close'], 5),
                    'volume': int(row['volume'])
                }
                for _, row in data.tail(50).iterrows()  # Last 50 periods for chart
            ]
        }
        
    def _get_ea_status(self) -> Dict[str, Any]:
        """Get Expert Advisor status and performance"""
        
        active_eas = expert_advisor_manager.get_active_eas()
        
        ea_data = []
        for ea_id, ea in active_eas.items():
            # Get recent performance
            performance = expert_advisor_manager.get_ea_performance(ea_id)
            
            ea_data.append({
                'id': ea_id,
                'name': ea.name,
                'strategy_type': ea.strategy_type,
                'status': 'Active' if ea.enabled else 'Stopped',
                'trades_today': performance.get('trades_today', 0),
                'profit_today': performance.get('profit_today', 0.0),
                'total_trades': performance.get('total_trades', 0),
                'win_rate': performance.get('win_rate', 0.0),
                'total_profit': performance.get('total_profit', 0.0),
                'max_drawdown': performance.get('max_drawdown', 0.0),
                'last_signal': performance.get('last_signal', 'None'),
                'last_update': performance.get('last_update', datetime.now().isoformat())
            })
            
        return {
            'active_count': len(active_eas),
            'total_profit_today': sum(ea.get('profit_today', 0) for ea in ea_data),
            'expert_advisors': ea_data,
            'summary': {
                'running': len([ea for ea in ea_data if ea['status'] == 'Active']),
                'stopped': len([ea for ea in ea_data if ea['status'] == 'Stopped']),
                'profitable': len([ea for ea in ea_data if ea['total_profit'] > 0]),
                'total_trades': sum(ea['total_trades'] for ea in ea_data)
            }
        }
        
    def _get_advanced_orders(self) -> Dict[str, Any]:
        """Get advanced orders status"""
        
        pending_orders = advanced_order_manager.get_pending_orders()
        active_positions = advanced_order_manager.get_active_positions()
        
        orders_data = []
        for order in pending_orders[:10]:  # Last 10 orders
            orders_data.append({
                'id': order.order_id,
                'symbol': order.symbol,
                'type': order.order_type.value,
                'side': order.side,
                'quantity': order.quantity,
                'price': order.price,
                'stop_loss': order.stop_loss,
                'take_profit': order.take_profit,
                'status': order.status.value,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'expires_at': order.expires_at.isoformat() if order.expires_at else None
            })
            
        positions_data = []
        for position in active_positions:
            unrealized_pnl = (position.current_price - position.entry_price) * position.quantity
            if position.side == 'sell':
                unrealized_pnl *= -1
                
            positions_data.append({
                'symbol': position.symbol,
                'side': position.side,
                'quantity': position.quantity,
                'entry_price': position.entry_price,
                'current_price': position.current_price,
                'unrealized_pnl': unrealized_pnl,
                'stop_loss': position.stop_loss,
                'take_profit': position.take_profit,
                'opened_at': position.opened_at.isoformat() if position.opened_at else None
            })
            
        return {
            'pending_orders': orders_data,
            'active_positions': positions_data,
            'summary': {
                'total_orders': len(pending_orders),
                'total_positions': len(active_positions),
                'total_unrealized_pnl': sum(pos['unrealized_pnl'] for pos in positions_data),
                'long_positions': len([p for p in positions_data if p['side'] == 'buy']),
                'short_positions': len([p for p in positions_data if p['side'] == 'sell'])
            }
        }
        
    def _get_risk_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Get risk management metrics"""
        
        # Calculate portfolio risk metrics
        returns = data['close'].pct_change().dropna()
        
        risk_metrics = risk_calculator.calculate_risk_metrics(returns, confidence_level=0.95)
        portfolio_metrics = risk_calculator.calculate_portfolio_metrics([returns], [1.0])
        
        # Position sizing recommendations
        current_price = data['close'].iloc[-1]
        position_sizes = {
            'conservative': risk_calculator.kelly_criterion_position_size(0.6, 2.0, 0.02),
            'moderate': risk_calculator.kelly_criterion_position_size(0.65, 2.5, 0.03),
            'aggressive': risk_calculator.kelly_criterion_position_size(0.7, 3.0, 0.05)
        }
        
        return {
            'value_at_risk': {
                'daily_var_95': risk_metrics.get('daily_var_95', 0),
                'daily_var_99': risk_metrics.get('daily_var_99', 0),
                'expected_shortfall': risk_metrics.get('expected_shortfall', 0)
            },
            'portfolio_metrics': {
                'sharpe_ratio': portfolio_metrics.get('sharpe_ratio', 0),
                'sortino_ratio': portfolio_metrics.get('sortino_ratio', 0),
                'max_drawdown': portfolio_metrics.get('max_drawdown', 0),
                'volatility': portfolio_metrics.get('volatility', 0)
            },
            'position_sizing': position_sizes,
            'risk_score': self._calculate_risk_score(risk_metrics, portfolio_metrics),
            'recommendations': self._get_risk_recommendations(risk_metrics, portfolio_metrics)
        }
        
    def _get_technical_analysis(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Get technical analysis indicators and signals"""
        
        # Calculate all indicators
        indicators = technical_indicators.calculate_all_indicators(data)
        
        # Get trading signals
        signals = TradingSignals()
        current_signals = signals.generate_signals(data, indicators)
        
        # Pattern recognition
        pattern_recognition = PatternRecognition()
        patterns = pattern_recognition.detect_patterns(data)
        
        return {
            'indicators': {
                'trend': {
                    'sma_20': indicators.get('sma_20', {}).get(data.index[-1], 0) if 'sma_20' in indicators else 0,
                    'sma_50': indicators.get('sma_50', {}).get(data.index[-1], 0) if 'sma_50' in indicators else 0,
                    'ema_12': indicators.get('ema_12', {}).get(data.index[-1], 0) if 'ema_12' in indicators else 0,
                    'ema_26': indicators.get('ema_26', {}).get(data.index[-1], 0) if 'ema_26' in indicators else 0,
                },
                'momentum': {
                    'rsi': indicators.get('rsi', {}).get(data.index[-1], 50) if 'rsi' in indicators else 50,
                    'macd': indicators.get('macd', {}).get(data.index[-1], 0) if 'macd' in indicators else 0,
                    'macd_signal': indicators.get('macd_signal', {}).get(data.index[-1], 0) if 'macd_signal' in indicators else 0,
                    'stochastic_k': indicators.get('stochastic_k', {}).get(data.index[-1], 50) if 'stochastic_k' in indicators else 50,
                    'stochastic_d': indicators.get('stochastic_d', {}).get(data.index[-1], 50) if 'stochastic_d' in indicators else 50,
                },
                'volatility': {
                    'bollinger_upper': indicators.get('bollinger_upper', {}).get(data.index[-1], 0) if 'bollinger_upper' in indicators else 0,
                    'bollinger_lower': indicators.get('bollinger_lower', {}).get(data.index[-1], 0) if 'bollinger_lower' in indicators else 0,
                    'atr': indicators.get('atr', {}).get(data.index[-1], 0) if 'atr' in indicators else 0,
                }
            },
            'signals': current_signals,
            'patterns': patterns,
            'trend_analysis': self._analyze_trend(data, indicators),
            'support_resistance': self._get_support_resistance(data)
        }
        
    def _get_pattern_analysis(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Get pattern recognition analysis"""
        
        try:
            # Scan for all patterns
            patterns = pattern_scanner.scan_all_patterns(data, symbol)
            
            # Categorize patterns
            chart_patterns = [p for p in patterns if p.pattern_type in [
                'Head and Shoulders', 'Ascending Triangle', 'Descending Triangle',
                'Double Top', 'Double Bottom', 'Cup and Handle', 'Bull Flag',
                'Bear Flag', 'Bull Pennant', 'Bear Pennant', 'Rising Wedge', 'Falling Wedge'
            ]]
            
            candlestick_patterns = [p for p in patterns if p.pattern_type in [
                'Doji', 'Hammer', 'Hanging Man', 'Shooting Star'
            ]]
            
            breakout_patterns = [p for p in patterns if p.pattern_type in [
                'Resistance Breakout', 'Support Breakdown', 'Volume Breakout', 'Volume Breakdown'
            ]]
            
            # Get highest confidence patterns
            top_patterns = sorted(patterns, key=lambda x: x.confidence, reverse=True)[:5]
            
            return {
                'total_patterns': len(patterns),
                'chart_patterns': [self._format_pattern(p) for p in chart_patterns],
                'candlestick_patterns': [self._format_pattern(p) for p in candlestick_patterns],
                'breakout_patterns': [self._format_pattern(p) for p in breakout_patterns],
                'top_patterns': [self._format_pattern(p) for p in top_patterns],
                'summary': {
                    'bullish_patterns': len([p for p in patterns if self._is_bullish_pattern(p)]),
                    'bearish_patterns': len([p for p in patterns if self._is_bearish_pattern(p)]),
                    'neutral_patterns': len([p for p in patterns if self._is_neutral_pattern(p)]),
                    'high_confidence': len([p for p in patterns if p.confidence >= 0.8]),
                    'average_confidence': sum(p.confidence for p in patterns) / len(patterns) if patterns else 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in pattern analysis: {e}")
            return {'error': str(e), 'total_patterns': 0}
            
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance and backtesting metrics"""
        
        # Get recent backtest results (simulated)
        sample_performance = PerformanceMetrics(
            total_trades=150,
            winning_trades=92,
            losing_trades=58,
            total_return=0.187,
            max_drawdown=0.085,
            sharpe_ratio=1.43,
            sortino_ratio=1.89,
            profit_factor=1.76,
            average_win=0.024,
            average_loss=0.018,
            largest_win=0.089,
            largest_loss=0.041,
            win_rate=0.613,
            average_trade_duration=timedelta(hours=4, minutes=23)
        )
        
        return {
            'overall_performance': {
                'total_return': sample_performance.total_return,
                'total_trades': sample_performance.total_trades,
                'win_rate': sample_performance.win_rate,
                'profit_factor': sample_performance.profit_factor,
                'sharpe_ratio': sample_performance.sharpe_ratio,
                'max_drawdown': sample_performance.max_drawdown
            },
            'recent_performance': {
                'trades_this_week': 23,
                'profit_this_week': 0.034,
                'best_day': 0.018,
                'worst_day': -0.012,
                'current_streak': 4  # winning streak
            },
            'risk_metrics': {
                'var_95': 0.024,
                'expected_shortfall': 0.031,
                'calmar_ratio': 2.2,
                'sterling_ratio': 1.95
            }
        }
        
    def _get_active_alerts(self) -> Dict[str, Any]:
        """Get active alerts and notifications"""
        
        # Get alerts from alert manager
        active_alerts = alert_manager.get_active_alerts()
        recent_alerts = alert_manager.get_recent_alerts(limit=10)
        
        alerts_data = []
        for alert in recent_alerts:
            alerts_data.append({
                'id': alert.alert_id,
                'type': alert.alert_type.value,
                'symbol': alert.symbol,
                'condition': alert.condition,
                'target_value': alert.target_value,
                'current_value': alert.current_value,
                'message': alert.message,
                'priority': alert.priority.value,
                'status': alert.status.value,
                'created_at': alert.created_at.isoformat(),
                'triggered_at': alert.triggered_at.isoformat() if alert.triggered_at else None
            })
            
        return {
            'active_count': len(active_alerts),
            'recent_alerts': alerts_data,
            'alert_summary': {
                'price_alerts': len([a for a in active_alerts if a.alert_type == AlertType.PRICE]),
                'technical_alerts': len([a for a in active_alerts if a.alert_type == AlertType.TECHNICAL_INDICATOR]),
                'news_alerts': len([a for a in active_alerts if a.alert_type == AlertType.NEWS]),
                'system_alerts': len([a for a in active_alerts if a.alert_type == AlertType.SYSTEM])
            },
            'notifications_enabled': True,
            'notification_channels': {
                'email': True,
                'sms': False,
                'push': True,
                'webhook': False
            }
        }
        
    def _get_market_overview(self) -> Dict[str, Any]:
        """Get overall market overview and sentiment"""
        
        # Market indices (simulated)
        indices = {
            'SPX': {'value': 4485.30, 'change': 12.45, 'change_pct': 0.28},
            'NASDAQ': {'value': 13892.15, 'change': -23.67, 'change_pct': -0.17},
            'FTSE': {'value': 7442.78, 'change': 5.23, 'change_pct': 0.07},
            'DAX': {'value': 16234.56, 'change': 89.34, 'change_pct': 0.55},
            'NIKKEI': {'value': 33456.78, 'change': -145.23, 'change_pct': -0.43}
        }
        
        # Currency pairs
        currencies = {
            'EURUSD': {'value': 1.0852, 'change': 0.0023, 'change_pct': 0.21},
            'GBPUSD': {'value': 1.2748, 'change': -0.0034, 'change_pct': -0.27},
            'USDJPY': {'value': 149.45, 'change': 0.78, 'change_pct': 0.52},
            'AUDUSD': {'value': 0.6453, 'change': 0.0012, 'change_pct': 0.19}
        }
        
        # Commodities
        commodities = {
            'GOLD': {'value': 2047.80, 'change': 12.30, 'change_pct': 0.60},
            'SILVER': {'value': 23.45, 'change': -0.23, 'change_pct': -0.97},
            'CRUDE_OIL': {'value': 78.90, 'change': 1.45, 'change_pct': 1.87},
            'NATURAL_GAS': {'value': 2.67, 'change': -0.08, 'change_pct': -2.91}
        }
        
        return {
            'market_sentiment': 'BULLISH',  # BULLISH, BEARISH, NEUTRAL
            'risk_appetite': 'MODERATE',    # HIGH, MODERATE, LOW
            'volatility_index': 18.45,
            'indices': indices,
            'currencies': currencies,
            'commodities': commodities,
            'market_news': [
                {
                    'title': 'Fed maintains hawkish stance on inflation',
                    'time': '2 hours ago',
                    'impact': 'HIGH',
                    'sentiment': 'BEARISH'
                },
                {
                    'title': 'Strong US employment data supports dollar',
                    'time': '4 hours ago',
                    'impact': 'MEDIUM',
                    'sentiment': 'BULLISH'
                },
                {
                    'title': 'ECB signals potential rate cuts in 2024',
                    'time': '6 hours ago',
                    'impact': 'HIGH',
                    'sentiment': 'BEARISH'
                }
            ]
        }
        
    # Helper methods
    def _calculate_risk_score(self, risk_metrics: Dict, portfolio_metrics: Dict) -> int:
        """Calculate overall risk score (1-100)"""
        
        var_score = min(100, abs(risk_metrics.get('daily_var_95', 0)) * 1000)
        drawdown_score = min(100, abs(portfolio_metrics.get('max_drawdown', 0)) * 100)
        volatility_score = min(100, portfolio_metrics.get('volatility', 0) * 200)
        
        risk_score = (var_score + drawdown_score + volatility_score) / 3
        return int(risk_score)
        
    def _get_risk_recommendations(self, risk_metrics: Dict, portfolio_metrics: Dict) -> List[str]:
        """Get risk management recommendations"""
        
        recommendations = []
        
        if portfolio_metrics.get('max_drawdown', 0) > 0.1:
            recommendations.append("Consider reducing position sizes - high drawdown detected")
            
        if portfolio_metrics.get('sharpe_ratio', 0) < 1.0:
            recommendations.append("Strategy risk-adjusted returns below optimal - review strategy")
            
        if abs(risk_metrics.get('daily_var_95', 0)) > 0.05:
            recommendations.append("High daily VaR - consider diversification")
            
        if not recommendations:
            recommendations.append("Risk levels within acceptable ranges")
            
        return recommendations
        
    def _analyze_trend(self, data: pd.DataFrame, indicators: Dict) -> Dict[str, Any]:
        """Analyze overall trend direction"""
        
        current_price = data['close'].iloc[-1]
        sma_20 = indicators.get('sma_20', {}).get(data.index[-1], current_price)
        sma_50 = indicators.get('sma_50', {}).get(data.index[-1], current_price)
        
        if current_price > sma_20 > sma_50:
            trend = 'STRONG_BULLISH'
        elif current_price > sma_20:
            trend = 'BULLISH'
        elif current_price < sma_20 < sma_50:
            trend = 'STRONG_BEARISH'
        elif current_price < sma_20:
            trend = 'BEARISH'
        else:
            trend = 'NEUTRAL'
            
        return {
            'direction': trend,
            'strength': self._calculate_trend_strength(data, indicators),
            'duration': self._estimate_trend_duration(data)
        }
        
    def _calculate_trend_strength(self, data: pd.DataFrame, indicators: Dict) -> float:
        """Calculate trend strength (0-1)"""
        
        # Simple trend strength based on price position relative to moving averages
        current_price = data['close'].iloc[-1]
        sma_20 = indicators.get('sma_20', {}).get(data.index[-1], current_price)
        
        price_distance = abs(current_price - sma_20) / current_price
        return min(1.0, price_distance * 20)  # Normalize to 0-1
        
    def _estimate_trend_duration(self, data: pd.DataFrame) -> str:
        """Estimate how long current trend has been in place"""
        
        # Simple estimation based on consecutive higher/lower closes
        closes = data['close'].tail(20)
        current_trend_days = 0
        
        if len(closes) > 1:
            is_uptrend = closes.iloc[-1] > closes.iloc[-2]
            
            for i in range(len(closes) - 2, 0, -1):
                if is_uptrend and closes.iloc[i] > closes.iloc[i-1]:
                    current_trend_days += 1
                elif not is_uptrend and closes.iloc[i] < closes.iloc[i-1]:
                    current_trend_days += 1
                else:
                    break
                    
        if current_trend_days < 3:
            return 'SHORT'
        elif current_trend_days < 10:
            return 'MEDIUM'
        else:
            return 'LONG'
            
    def _get_support_resistance(self, data: pd.DataFrame) -> Dict[str, List[float]]:
        """Get key support and resistance levels"""
        
        # Simple support/resistance using recent highs/lows
        recent_data = data.tail(50)
        
        # Resistance levels (recent highs)
        resistance_levels = []
        for i in range(2, len(recent_data) - 2):
            if (recent_data['high'].iloc[i] > recent_data['high'].iloc[i-1] and
                recent_data['high'].iloc[i] > recent_data['high'].iloc[i-2] and
                recent_data['high'].iloc[i] > recent_data['high'].iloc[i+1] and
                recent_data['high'].iloc[i] > recent_data['high'].iloc[i+2]):
                resistance_levels.append(recent_data['high'].iloc[i])
                
        # Support levels (recent lows)
        support_levels = []
        for i in range(2, len(recent_data) - 2):
            if (recent_data['low'].iloc[i] < recent_data['low'].iloc[i-1] and
                recent_data['low'].iloc[i] < recent_data['low'].iloc[i-2] and
                recent_data['low'].iloc[i] < recent_data['low'].iloc[i+1] and
                recent_data['low'].iloc[i] < recent_data['low'].iloc[i+2]):
                support_levels.append(recent_data['low'].iloc[i])
                
        return {
            'resistance': sorted(resistance_levels, reverse=True)[:3],
            'support': sorted(support_levels, reverse=True)[:3]
        }
        
    def _format_pattern(self, pattern: PatternResult) -> Dict[str, Any]:
        """Format pattern result for frontend"""
        
        return {
            'type': pattern.pattern_type,
            'confidence': round(pattern.confidence, 2),
            'symbol': pattern.symbol,
            'description': pattern.description,
            'start_date': pattern.start_date.isoformat() if pattern.start_date else None,
            'end_date': pattern.end_date.isoformat() if pattern.end_date else None,
            'entry_price': round(pattern.entry_price, 5) if pattern.entry_price else None,
            'target_price': round(pattern.target_price, 5) if pattern.target_price else None,
            'stop_loss': round(pattern.stop_loss, 5) if pattern.stop_loss else None,
            'risk_reward_ratio': round(pattern.risk_reward_ratio, 2) if pattern.risk_reward_ratio else None,
            'bias': self._get_pattern_bias(pattern)
        }
        
    def _get_pattern_bias(self, pattern: PatternResult) -> str:
        """Get pattern bias (bullish/bearish/neutral)"""
        
        bullish_patterns = [
            'Double Bottom', 'Cup and Handle', 'Bull Flag', 'Bull Pennant',
            'Falling Wedge', 'Hammer', 'Resistance Breakout', 'Volume Breakout'
        ]
        
        bearish_patterns = [
            'Head and Shoulders', 'Double Top', 'Bear Flag', 'Bear Pennant',
            'Rising Wedge', 'Hanging Man', 'Shooting Star', 'Support Breakdown', 'Volume Breakdown'
        ]
        
        if pattern.pattern_type in bullish_patterns:
            return 'BULLISH'
        elif pattern.pattern_type in bearish_patterns:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
            
    def _is_bullish_pattern(self, pattern: PatternResult) -> bool:
        return self._get_pattern_bias(pattern) == 'BULLISH'
        
    def _is_bearish_pattern(self, pattern: PatternResult) -> bool:
        return self._get_pattern_bias(pattern) == 'BEARISH'
        
    def _is_neutral_pattern(self, pattern: PatternResult) -> bool:
        return self._get_pattern_bias(pattern) == 'NEUTRAL'


# Global dashboard instance
dashboard = ProfessionalAnalyticsDashboard()

# Routes
@analytics_bp.route('/')
def analytics_dashboard():
    """Main analytics dashboard page"""
    return render_template('professional_analytics.html')
    
@analytics_bp.route('/api/dashboard/<symbol>')
@analytics_bp.route('/api/dashboard/<symbol>/<timeframe>')
def get_dashboard_data(symbol: str, timeframe: str = '1H'):
    """API endpoint for dashboard data"""
    
    try:
        data = dashboard.get_dashboard_data(symbol, timeframe)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@analytics_bp.route('/api/patterns/<symbol>')
def get_pattern_analysis(symbol: str):
    """API endpoint for pattern analysis"""
    
    try:
        # Generate sample data for pattern analysis
        market_data = dashboard._generate_sample_data(symbol, '1H')
        patterns_data = dashboard._get_pattern_analysis(market_data, symbol)
        return jsonify(patterns_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@analytics_bp.route('/api/backtest', methods=['POST'])
def run_backtest():
    """API endpoint for running backtests"""
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'EURUSD')
        strategy = data.get('strategy', 'moving_average_crossover')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Run backtest using strategy backtester
        market_data = dashboard._generate_sample_data(symbol, '1H', periods=200)
        
        # Simple moving average crossover strategy for demo
        def sample_strategy(data):
            signals = []
            sma_short = data['close'].rolling(10).mean()
            sma_long = data['close'].rolling(20).mean()
            
            for i in range(20, len(data)):
                if sma_short.iloc[i] > sma_long.iloc[i] and sma_short.iloc[i-1] <= sma_long.iloc[i-1]:
                    signals.append(('BUY', data.index[i], data['close'].iloc[i]))
                elif sma_short.iloc[i] < sma_long.iloc[i] and sma_short.iloc[i-1] >= sma_long.iloc[i-1]:
                    signals.append(('SELL', data.index[i], data['close'].iloc[i]))
                    
            return signals
            
        # Run backtest
        backtest_results = strategy_backtester.run_backtest(
            market_data, 
            sample_strategy, 
            initial_capital=10000
        )
        
        return jsonify({
            'performance_metrics': {
                'total_return': backtest_results.total_return,
                'max_drawdown': backtest_results.max_drawdown,
                'sharpe_ratio': backtest_results.sharpe_ratio,
                'total_trades': backtest_results.total_trades,
                'win_rate': backtest_results.win_rate,
                'profit_factor': backtest_results.profit_factor
            },
            'trades': len(backtest_results.trades),
            'equity_curve': []  # Would contain equity curve data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/alerts', methods=['GET', 'POST'])
def manage_alerts():
    """API endpoint for managing alerts"""
    
    if request.method == 'GET':
        try:
            alerts_data = dashboard._get_active_alerts()
            return jsonify(alerts_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Create new alert
            alert = Alert(
                alert_type=AlertType(data['type']),
                symbol=data['symbol'],
                condition=data['condition'],
                target_value=data['target_value'],
                message=data.get('message', ''),
                notification_channels=data.get('channels', ['email'])
            )
            
            alert_manager.add_alert(alert)
            
            return jsonify({'status': 'success', 'alert_id': alert.alert_id})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
