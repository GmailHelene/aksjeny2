"""
Expert Advisor (EA) Simulation Engine for CMC Markets-style MT4 functionality
Provides automated trading strategy simulation and backtesting capabilities
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Any
import logging

class ExpertAdvisor:
    """Base class for Expert Advisor trading strategies"""
    
    def __init__(self, name: str, symbol: str, timeframe: str = 'D', initial_capital: float = 10000):
        self.name = name
        self.symbol = symbol
        self.timeframe = timeframe
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = []
        self.trades_history = []
        self.indicators = {}
        self.parameters = {}
        self.signals = []
        
    def set_parameters(self, **kwargs):
        """Set EA parameters"""
        self.parameters.update(kwargs)
        
    def add_indicator(self, name: str, values: List[float]):
        """Add technical indicator values"""
        self.indicators[name] = values
        
    def calculate_sma(self, prices: List[float], period: int) -> List[float]:
        """Calculate Simple Moving Average"""
        sma = []
        for i in range(len(prices)):
            if i < period - 1:
                sma.append(np.nan)
            else:
                sma.append(np.mean(prices[i-period+1:i+1]))
        return sma
        
    def calculate_ema(self, prices: List[float], period: int) -> List[float]:
        """Calculate Exponential Moving Average"""
        ema = []
        multiplier = 2 / (period + 1)
        
        for i, price in enumerate(prices):
            if i == 0:
                ema.append(price)
            else:
                ema.append((price - ema[i-1]) * multiplier + ema[i-1])
        return ema
        
    def calculate_rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """Calculate Relative Strength Index"""
        deltas = np.diff(prices)
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        rsi = [np.nan] * (period)
        
        for i in range(period, len(prices)):
            if i == period:
                rs = avg_gain / avg_loss if avg_loss != 0 else 0
            else:
                avg_gain = (avg_gain * (period - 1) + gains[i-1]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i-1]) / period
                rs = avg_gain / avg_loss if avg_loss != 0 else 0
                
            rsi.append(100 - (100 / (1 + rs)))
            
        return rsi
        
    def calculate_macd(self, prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9):
        """Calculate MACD indicator"""
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        
        macd_line = [f - s if not np.isnan(f) and not np.isnan(s) else np.nan 
                     for f, s in zip(ema_fast, ema_slow)]
        
        # Remove NaN values for signal calculation
        macd_clean = [x for x in macd_line if not np.isnan(x)]
        signal_line_clean = self.calculate_ema(macd_clean, signal)
        
        # Pad signal line with NaN to match original length
        nan_count = len(macd_line) - len(signal_line_clean)
        signal_line = [np.nan] * nan_count + signal_line_clean
        
        histogram = [m - s if not np.isnan(m) and not np.isnan(s) else np.nan 
                    for m, s in zip(macd_line, signal_line)]
                    
        return macd_line, signal_line, histogram
        
    def generate_signal(self, data: Dict[str, Any], index: int) -> Optional[str]:
        """Generate trading signal (BUY/SELL/HOLD) - Override in subclasses"""
        return "HOLD"
        
    def open_position(self, signal: str, price: float, size: float, stop_loss: float = None, take_profit: float = None):
        """Open a new position"""
        position = {
            'id': len(self.positions) + 1,
            'signal': signal,
            'entry_price': price,
            'size': size,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'open_time': datetime.now(),
            'status': 'OPEN'
        }
        self.positions.append(position)
        return position
        
    def close_position(self, position_id: int, exit_price: float, reason: str = "MANUAL"):
        """Close an existing position"""
        for position in self.positions:
            if position['id'] == position_id and position['status'] == 'OPEN':
                position['exit_price'] = exit_price
                position['close_time'] = datetime.now()
                position['status'] = 'CLOSED'
                position['close_reason'] = reason
                
                # Calculate P&L
                if position['signal'] == 'BUY':
                    pnl = (exit_price - position['entry_price']) * position['size']
                else:  # SELL
                    pnl = (position['entry_price'] - exit_price) * position['size']
                    
                position['pnl'] = pnl
                self.current_capital += pnl
                
                # Add to trade history
                self.trades_history.append(position.copy())
                return True
        return False
        
    def check_stop_loss_take_profit(self, current_price: float):
        """Check if any positions should be closed due to SL/TP"""
        for position in self.positions:
            if position['status'] == 'OPEN':
                if position['signal'] == 'BUY':
                    # Check stop loss
                    if position['stop_loss'] and current_price <= position['stop_loss']:
                        self.close_position(position['id'], position['stop_loss'], "STOP_LOSS")
                    # Check take profit
                    elif position['take_profit'] and current_price >= position['take_profit']:
                        self.close_position(position['id'], position['take_profit'], "TAKE_PROFIT")
                        
                elif position['signal'] == 'SELL':
                    # Check stop loss (price goes up)
                    if position['stop_loss'] and current_price >= position['stop_loss']:
                        self.close_position(position['id'], position['stop_loss'], "STOP_LOSS")
                    # Check take profit (price goes down)
                    elif position['take_profit'] and current_price <= position['take_profit']:
                        self.close_position(position['id'], position['take_profit'], "TAKE_PROFIT")
        
    def get_performance_metrics(self) -> Dict[str, float]:
        """Calculate performance metrics"""
        if not self.trades_history:
            return {}
            
        total_trades = len(self.trades_history)
        winning_trades = [t for t in self.trades_history if t['pnl'] > 0]
        losing_trades = [t for t in self.trades_history if t['pnl'] < 0]
        
        win_rate = len(winning_trades) / total_trades * 100 if total_trades > 0 else 0
        
        total_profit = sum(t['pnl'] for t in winning_trades)
        total_loss = sum(t['pnl'] for t in losing_trades)
        net_profit = total_profit + total_loss
        
        profit_factor = abs(total_profit / total_loss) if total_loss != 0 else float('inf')
        
        avg_win = total_profit / len(winning_trades) if winning_trades else 0
        avg_loss = total_loss / len(losing_trades) if losing_trades else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'net_profit': net_profit,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'profit_factor': profit_factor,
            'average_win': avg_win,
            'average_loss': avg_loss,
            'return_percentage': (self.current_capital - self.initial_capital) / self.initial_capital * 100
        }


class MovingAverageCrossoverEA(ExpertAdvisor):
    """Simple Moving Average Crossover Expert Advisor"""
    
    def __init__(self, symbol: str, fast_period: int = 10, slow_period: int = 20):
        super().__init__("MA Crossover", symbol)
        self.set_parameters(fast_period=fast_period, slow_period=slow_period)
        
    def generate_signal(self, data: Dict[str, Any], index: int) -> Optional[str]:
        """Generate signal based on MA crossover"""
        if index < self.parameters['slow_period']:
            return "HOLD"
            
        prices = data['close'][:index+1]
        
        fast_ma = self.calculate_sma(prices, self.parameters['fast_period'])
        slow_ma = self.calculate_sma(prices, self.parameters['slow_period'])
        
        if len(fast_ma) < 2 or len(slow_ma) < 2:
            return "HOLD"
            
        # Current and previous values
        fast_current = fast_ma[-1]
        fast_previous = fast_ma[-2]
        slow_current = slow_ma[-1]
        slow_previous = slow_ma[-2]
        
        # Check for crossover
        if (fast_previous <= slow_previous and fast_current > slow_current):
            return "BUY"
        elif (fast_previous >= slow_previous and fast_current < slow_current):
            return "SELL"
            
        return "HOLD"


class RSIOverboughtOversoldEA(ExpertAdvisor):
    """RSI Overbought/Oversold Expert Advisor"""
    
    def __init__(self, symbol: str, rsi_period: int = 14, oversold: float = 30, overbought: float = 70):
        super().__init__("RSI Strategy", symbol)
        self.set_parameters(rsi_period=rsi_period, oversold=oversold, overbought=overbought)
        
    def generate_signal(self, data: Dict[str, Any], index: int) -> Optional[str]:
        """Generate signal based on RSI levels"""
        if index < self.parameters['rsi_period']:
            return "HOLD"
            
        prices = data['close'][:index+1]
        rsi = self.calculate_rsi(prices, self.parameters['rsi_period'])
        
        if len(rsi) < 1 or np.isnan(rsi[-1]):
            return "HOLD"
            
        current_rsi = rsi[-1]
        
        if current_rsi < self.parameters['oversold']:
            return "BUY"
        elif current_rsi > self.parameters['overbought']:
            return "SELL"
            
        return "HOLD"


class EABacktester:
    """Backtesting engine for Expert Advisors"""
    
    def __init__(self, ea: ExpertAdvisor):
        self.ea = ea
        self.results = {}
        
    def run_backtest(self, data: pd.DataFrame, position_size: float = 100, 
                    stop_loss_pct: float = 0.02, take_profit_pct: float = 0.04) -> Dict[str, Any]:
        """Run backtest on historical data"""
        
        # Reset EA state
        self.ea.current_capital = self.ea.initial_capital
        self.ea.positions = []
        self.ea.trades_history = []
        
        data_dict = {
            'open': data['open'].tolist(),
            'high': data['high'].tolist(),
            'low': data['low'].tolist(),
            'close': data['close'].tolist(),
            'volume': data['volume'].tolist() if 'volume' in data.columns else [0] * len(data)
        }
        
        for i in range(len(data)):
            current_price = data_dict['close'][i]
            
            # Check existing positions for SL/TP
            self.ea.check_stop_loss_take_profit(current_price)
            
            # Generate new signal
            signal = self.ea.generate_signal(data_dict, i)
            
            if signal in ['BUY', 'SELL'] and len([p for p in self.ea.positions if p['status'] == 'OPEN']) == 0:
                # Calculate stop loss and take profit levels
                if signal == 'BUY':
                    stop_loss = current_price * (1 - stop_loss_pct)
                    take_profit = current_price * (1 + take_profit_pct)
                else:  # SELL
                    stop_loss = current_price * (1 + stop_loss_pct)
                    take_profit = current_price * (1 - take_profit_pct)
                    
                self.ea.open_position(signal, current_price, position_size, stop_loss, take_profit)
        
        # Close any remaining open positions
        for position in self.ea.positions:
            if position['status'] == 'OPEN':
                self.ea.close_position(position['id'], data_dict['close'][-1], "END_OF_TEST")
        
        # Calculate results
        metrics = self.ea.get_performance_metrics()
        
        self.results = {
            'ea_name': self.ea.name,
            'symbol': self.ea.symbol,
            'backtest_period': f"{data.index[0]} to {data.index[-1]}",
            'metrics': metrics,
            'trades': self.ea.trades_history,
            'equity_curve': self.calculate_equity_curve(data_dict['close'])
        }
        
        return self.results
        
    def calculate_equity_curve(self, prices: List[float]) -> List[float]:
        """Calculate equity curve over time"""
        equity = [self.ea.initial_capital]
        running_capital = self.ea.initial_capital
        
        for trade in self.ea.trades_history:
            # Find the index where this trade was closed
            running_capital += trade['pnl']
            equity.append(running_capital)
            
        # Pad to match price length if needed
        while len(equity) < len(prices):
            equity.append(equity[-1])
            
        return equity[:len(prices)]


def get_available_strategies() -> List[Dict[str, Any]]:
    """Get list of available EA strategies"""
    return [
        {
            'name': 'Moving Average Crossover',
            'class': 'MovingAverageCrossoverEA',
            'description': 'Kjøper når rask MA krysser over langsom MA, selger ved motsatt',
            'parameters': [
                {'name': 'fast_period', 'label': 'Rask MA periode', 'type': 'int', 'default': 10, 'min': 5, 'max': 50},
                {'name': 'slow_period', 'label': 'Langsom MA periode', 'type': 'int', 'default': 20, 'min': 10, 'max': 100}
            ]
        },
        {
            'name': 'RSI Overbought/Oversold',
            'class': 'RSIOverboughtOversoldEA',
            'description': 'Kjøper når RSI < oversold nivå, selger når RSI > overkjøpt nivå',
            'parameters': [
                {'name': 'rsi_period', 'label': 'RSI periode', 'type': 'int', 'default': 14, 'min': 5, 'max': 30},
                {'name': 'oversold', 'label': 'Oversolgt nivå', 'type': 'float', 'default': 30, 'min': 10, 'max': 40},
                {'name': 'overbought', 'label': 'Overkjøpt nivå', 'type': 'float', 'default': 70, 'min': 60, 'max': 90}
            ]
        }
    ]


def create_ea_from_strategy(strategy_name: str, symbol: str, **parameters) -> Optional[ExpertAdvisor]:
    """Factory function to create EA instances"""
    strategies = {
        'MovingAverageCrossoverEA': MovingAverageCrossoverEA,
        'RSIOverboughtOversoldEA': RSIOverboughtOversoldEA
    }
    
    if strategy_name in strategies:
        return strategies[strategy_name](symbol, **parameters)
    
    return None


class ExpertAdvisorManager:
    """Manager class for Expert Advisors"""
    
    def __init__(self):
        self.active_eas = {}
        self.ea_performance = {}
        
    def add_ea(self, ea_id: str, ea: ExpertAdvisor):
        """Add an Expert Advisor to the manager"""
        self.active_eas[ea_id] = ea
        
    def remove_ea(self, ea_id: str):
        """Remove an Expert Advisor from the manager"""
        if ea_id in self.active_eas:
            del self.active_eas[ea_id]
        if ea_id in self.ea_performance:
            del self.ea_performance[ea_id]
            
    def get_active_eas(self) -> Dict[str, ExpertAdvisor]:
        """Get all active Expert Advisors"""
        return self.active_eas
        
    def get_ea_performance(self, ea_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific EA"""
        if ea_id in self.active_eas:
            ea = self.active_eas[ea_id]
            return {
                'ea_id': ea_id,
                'name': ea.name,
                'symbol': ea.symbol,
                'current_capital': ea.current_capital,
                'initial_capital': ea.initial_capital,
                'total_trades': len(ea.trades_history),
                'open_positions': len([p for p in ea.positions if p['status'] == 'OPEN']),
                'performance_metrics': ea.get_performance_metrics() if hasattr(ea, 'get_performance_metrics') else {}
            }
        return None


# Create a global instance of the Expert Advisor Manager
expert_advisor_manager = ExpertAdvisorManager()
