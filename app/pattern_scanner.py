"""
Pattern Recognition Scanner for CMC Markets-style MT4 functionality
Advanced pattern detection and technical analysis scanning
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
from scipy import stats
from sklearn.cluster import DBSCAN
import math

@dataclass
class PatternResult:
    """Pattern detection result"""
    symbol: str
    pattern_type: str
    confidence: float
    start_date: datetime
    end_date: datetime
    entry_price: Optional[float] = None
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    risk_reward_ratio: Optional[float] = None
    pattern_data: Dict[str, Any] = None
    description: str = ""

class AdvancedPatternScanner:
    """Professional pattern recognition scanner"""
    
    def __init__(self):
        self.min_confidence = 0.6
        self.lookback_periods = 50
        self.price_tolerance = 0.02  # 2% tolerance for pattern matching
        
    def scan_all_patterns(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Scan for all supported patterns"""
        
        patterns = []
        
        try:
            # Chart patterns
            patterns.extend(self.detect_head_and_shoulders(data, symbol))
            patterns.extend(self.detect_triangles(data, symbol))
            patterns.extend(self.detect_double_tops_bottoms(data, symbol))
            patterns.extend(self.detect_cup_and_handle(data, symbol))
            patterns.extend(self.detect_flags_pennants(data, symbol))
            patterns.extend(self.detect_wedges(data, symbol))
            
            # Candlestick patterns
            patterns.extend(self.detect_candlestick_patterns(data, symbol))
            
            # Support and resistance
            patterns.extend(self.detect_breakouts(data, symbol))
            
            # Volume patterns
            if 'volume' in data.columns:
                patterns.extend(self.detect_volume_patterns(data, symbol))
                
        except Exception as e:
            logging.error(f"Error scanning patterns for {symbol}: {e}")
            
        return sorted(patterns, key=lambda x: x.confidence, reverse=True)
        
    def detect_head_and_shoulders(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect head and shoulders patterns"""
        
        patterns = []
        
        if len(data) < 30:
            return patterns
            
        # Find peaks and troughs
        peaks = self._find_peaks(data['high'], window=5)
        troughs = self._find_troughs(data['low'], window=5)
        
        # Need at least 3 peaks for head and shoulders
        if len(peaks) < 3:
            return patterns
            
        # Check each combination of 3 consecutive peaks
        for i in range(len(peaks) - 2):
            left_shoulder = peaks[i]
            head = peaks[i + 1]
            right_shoulder = peaks[i + 2]
            
            # Head should be higher than both shoulders
            if head[1] <= left_shoulder[1] or head[1] <= right_shoulder[1]:
                continue
                
            # Shoulders should be approximately equal
            shoulder_diff = abs(left_shoulder[1] - right_shoulder[1]) / left_shoulder[1]
            if shoulder_diff > self.price_tolerance * 2:
                continue
                
            # Find neckline (lowest point between shoulders)
            neckline_data = data.iloc[left_shoulder[0]:right_shoulder[0] + 1]
            neckline_price = neckline_data['low'].min()
            
            # Calculate confidence based on pattern quality
            confidence = self._calculate_hns_confidence(left_shoulder, head, right_shoulder, neckline_price)
            
            if confidence >= self.min_confidence:
                # Calculate targets
                head_to_neckline = head[1] - neckline_price
                target_price = neckline_price - head_to_neckline
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Head and Shoulders",
                    confidence=confidence,
                    start_date=data.index[left_shoulder[0]],
                    end_date=data.index[right_shoulder[0]],
                    entry_price=neckline_price * 0.99,  # Enter slightly below neckline
                    target_price=target_price,
                    stop_loss=right_shoulder[1] * 1.02,
                    pattern_data={
                        'left_shoulder': left_shoulder,
                        'head': head,
                        'right_shoulder': right_shoulder,
                        'neckline': neckline_price
                    },
                    description=f"Bearish head and shoulders pattern with neckline at {neckline_price:.2f}"
                )
                
                # Calculate risk/reward ratio
                if pattern.entry_price and pattern.target_price and pattern.stop_loss:
                    risk = abs(pattern.entry_price - pattern.stop_loss)
                    reward = abs(pattern.target_price - pattern.entry_price)
                    pattern.risk_reward_ratio = reward / risk if risk > 0 else 0
                    
                patterns.append(pattern)
                
        return patterns
        
    def detect_triangles(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect triangle patterns (ascending, descending, symmetrical)"""
        
        patterns = []
        
        if len(data) < 20:
            return patterns
            
        # Find peaks and troughs
        peaks = self._find_peaks(data['high'], window=3)
        troughs = self._find_troughs(data['low'], window=3)
        
        if len(peaks) < 2 or len(troughs) < 2:
            return patterns
            
        # Get recent peaks and troughs
        recent_peaks = peaks[-3:] if len(peaks) >= 3 else peaks[-2:]
        recent_troughs = troughs[-3:] if len(troughs) >= 3 else troughs[-2:]
        
        # Ascending Triangle (horizontal resistance, rising support)
        if len(recent_peaks) >= 2:
            resistance_level = np.mean([p[1] for p in recent_peaks])
            resistance_variance = np.var([p[1] for p in recent_peaks])
            
            if resistance_variance < (resistance_level * 0.01) ** 2:  # Low variance = horizontal
                # Check if support is rising
                if len(recent_troughs) >= 2:
                    trough_trend = self._calculate_trend(recent_troughs)
                    if trough_trend > 0:  # Rising support
                        confidence = self._calculate_triangle_confidence(recent_peaks, recent_troughs, "ascending")
                        
                        if confidence >= self.min_confidence:
                            # Breakout target
                            triangle_height = resistance_level - recent_troughs[0][1]
                            target_price = resistance_level + triangle_height
                            
                            pattern = PatternResult(
                                symbol=symbol,
                                pattern_type="Ascending Triangle",
                                confidence=confidence,
                                start_date=data.index[min(recent_peaks[0][0], recent_troughs[0][0])],
                                end_date=data.index[max(recent_peaks[-1][0], recent_troughs[-1][0])],
                                entry_price=resistance_level * 1.01,  # Break above resistance
                                target_price=target_price,
                                stop_loss=recent_troughs[-1][1] * 0.98,
                                pattern_data={
                                    'resistance_level': resistance_level,
                                    'rising_support': True,
                                    'peaks': recent_peaks,
                                    'troughs': recent_troughs
                                },
                                description=f"Bullish ascending triangle with resistance at {resistance_level:.2f}"
                            )
                            
                            patterns.append(pattern)
                            
        # Descending Triangle (falling resistance, horizontal support)
        if len(recent_troughs) >= 2:
            support_level = np.mean([t[1] for t in recent_troughs])
            support_variance = np.var([t[1] for t in recent_troughs])
            
            if support_variance < (support_level * 0.01) ** 2:  # Low variance = horizontal
                # Check if resistance is falling
                if len(recent_peaks) >= 2:
                    peak_trend = self._calculate_trend(recent_peaks)
                    if peak_trend < 0:  # Falling resistance
                        confidence = self._calculate_triangle_confidence(recent_peaks, recent_troughs, "descending")
                        
                        if confidence >= self.min_confidence:
                            # Breakout target
                            triangle_height = recent_peaks[0][1] - support_level
                            target_price = support_level - triangle_height
                            
                            pattern = PatternResult(
                                symbol=symbol,
                                pattern_type="Descending Triangle",
                                confidence=confidence,
                                start_date=data.index[min(recent_peaks[0][0], recent_troughs[0][0])],
                                end_date=data.index[max(recent_peaks[-1][0], recent_troughs[-1][0])],
                                entry_price=support_level * 0.99,  # Break below support
                                target_price=target_price,
                                stop_loss=recent_peaks[-1][1] * 1.02,
                                pattern_data={
                                    'support_level': support_level,
                                    'falling_resistance': True,
                                    'peaks': recent_peaks,
                                    'troughs': recent_troughs
                                },
                                description=f"Bearish descending triangle with support at {support_level:.2f}"
                            )
                            
                            patterns.append(pattern)
                            
        return patterns
        
    def detect_double_tops_bottoms(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect double top and double bottom patterns"""
        
        patterns = []
        
        if len(data) < 20:
            return patterns
            
        peaks = self._find_peaks(data['high'], window=5)
        troughs = self._find_troughs(data['low'], window=5)
        
        # Double Top
        if len(peaks) >= 2:
            for i in range(len(peaks) - 1):
                peak1 = peaks[i]
                peak2 = peaks[i + 1]
                
                # Peaks should be approximately equal
                price_diff = abs(peak1[1] - peak2[1]) / peak1[1]
                if price_diff <= self.price_tolerance:
                    
                    # Find valley between peaks
                    valley_data = data.iloc[peak1[0]:peak2[0] + 1]
                    valley_price = valley_data['low'].min()
                    
                    # Pattern should have minimum height
                    pattern_height = min(peak1[1], peak2[1]) - valley_price
                    if pattern_height / peak1[1] >= 0.03:  # Minimum 3% height
                        
                        confidence = self._calculate_double_pattern_confidence(peak1, peak2, valley_price, "top")
                        
                        if confidence >= self.min_confidence:
                            target_price = valley_price - pattern_height
                            
                            pattern = PatternResult(
                                symbol=symbol,
                                pattern_type="Double Top",
                                confidence=confidence,
                                start_date=data.index[peak1[0]],
                                end_date=data.index[peak2[0]],
                                entry_price=valley_price * 0.99,
                                target_price=target_price,
                                stop_loss=max(peak1[1], peak2[1]) * 1.02,
                                pattern_data={
                                    'peak1': peak1,
                                    'peak2': peak2,
                                    'valley': valley_price,
                                    'pattern_height': pattern_height
                                },
                                description=f"Bearish double top with peaks at {peak1[1]:.2f} and {peak2[1]:.2f}"
                            )
                            
                            patterns.append(pattern)
                            
        # Double Bottom
        if len(troughs) >= 2:
            for i in range(len(troughs) - 1):
                trough1 = troughs[i]
                trough2 = troughs[i + 1]
                
                # Troughs should be approximately equal
                price_diff = abs(trough1[1] - trough2[1]) / trough1[1]
                if price_diff <= self.price_tolerance:
                    
                    # Find peak between troughs
                    peak_data = data.iloc[trough1[0]:trough2[0] + 1]
                    peak_price = peak_data['high'].max()
                    
                    # Pattern should have minimum height
                    pattern_height = peak_price - max(trough1[1], trough2[1])
                    if pattern_height / trough1[1] >= 0.03:  # Minimum 3% height
                        
                        confidence = self._calculate_double_pattern_confidence(trough1, trough2, peak_price, "bottom")
                        
                        if confidence >= self.min_confidence:
                            target_price = peak_price + pattern_height
                            
                            pattern = PatternResult(
                                symbol=symbol,
                                pattern_type="Double Bottom",
                                confidence=confidence,
                                start_date=data.index[trough1[0]],
                                end_date=data.index[trough2[0]],
                                entry_price=peak_price * 1.01,
                                target_price=target_price,
                                stop_loss=min(trough1[1], trough2[1]) * 0.98,
                                pattern_data={
                                    'trough1': trough1,
                                    'trough2': trough2,
                                    'peak': peak_price,
                                    'pattern_height': pattern_height
                                },
                                description=f"Bullish double bottom with troughs at {trough1[1]:.2f} and {trough2[1]:.2f}"
                            )
                            
                            patterns.append(pattern)
                            
        return patterns
        
    def detect_cup_and_handle(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect cup and handle patterns"""
        
        patterns = []
        
        if len(data) < 30:
            return patterns
            
        # Look for cup formation (U-shaped pattern)
        for start_idx in range(len(data) - 25):
            end_idx = start_idx + 20
            if end_idx >= len(data):
                break
                
            cup_data = data.iloc[start_idx:end_idx]
            
            # Cup should start and end at similar highs
            left_rim = cup_data['high'].iloc[0]
            right_rim = cup_data['high'].iloc[-1]
            
            if abs(left_rim - right_rim) / left_rim > self.price_tolerance:
                continue
                
            # Find the bottom of the cup
            cup_bottom = cup_data['low'].min()
            cup_depth = ((left_rim + right_rim) / 2 - cup_bottom) / left_rim
            
            # Cup should be 12-33% deep
            if cup_depth < 0.12 or cup_depth > 0.33:
                continue
                
            # Look for handle formation after cup
            handle_start = end_idx
            handle_end = min(handle_start + 10, len(data) - 1)
            
            if handle_end <= handle_start:
                continue
                
            handle_data = data.iloc[handle_start:handle_end]
            handle_high = handle_data['high'].max()
            handle_low = handle_data['low'].min()
            
            # Handle should not exceed cup rim and should be shallower than cup
            if handle_high > right_rim * 1.01:
                continue
                
            handle_depth = (right_rim - handle_low) / right_rim
            if handle_depth > cup_depth * 0.5:  # Handle should be less than half cup depth
                continue
                
            # Calculate confidence
            confidence = self._calculate_cup_handle_confidence(cup_data, handle_data, cup_depth, handle_depth)
            
            if confidence >= self.min_confidence:
                # Breakout point is above handle high
                entry_price = handle_high * 1.01
                target_price = entry_price + (left_rim - cup_bottom)  # Cup depth as target
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Cup and Handle",
                    confidence=confidence,
                    start_date=data.index[start_idx],
                    end_date=data.index[handle_end],
                    entry_price=entry_price,
                    target_price=target_price,
                    stop_loss=handle_low * 0.95,
                    pattern_data={
                        'cup_start': start_idx,
                        'cup_end': end_idx,
                        'cup_bottom': cup_bottom,
                        'cup_depth': cup_depth,
                        'handle_high': handle_high,
                        'handle_low': handle_low,
                        'handle_depth': handle_depth
                    },
                    description=f"Bullish cup and handle with {cup_depth:.1%} cup depth"
                )
                
                patterns.append(pattern)
                
        return patterns
        
    def detect_flags_pennants(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect flag and pennant continuation patterns"""
        
        patterns = []
        
        if len(data) < 15:
            return patterns
            
        # Look for strong moves followed by consolidation
        for i in range(10, len(data) - 5):
            # Check for strong move (flagpole)
            flagpole_start = max(0, i - 10)
            flagpole_data = data.iloc[flagpole_start:i]
            
            price_change = (flagpole_data['close'].iloc[-1] - flagpole_data['close'].iloc[0]) / flagpole_data['close'].iloc[0]
            
            # Need at least 5% move to form flagpole
            if abs(price_change) < 0.05:
                continue
                
            # Check consolidation period (flag/pennant)
            consolidation_end = min(i + 8, len(data) - 1)
            consolidation_data = data.iloc[i:consolidation_end]
            
            if len(consolidation_data) < 3:
                continue
                
            # Calculate consolidation characteristics
            cons_high = consolidation_data['high'].max()
            cons_low = consolidation_data['low'].min()
            cons_range = (cons_high - cons_low) / cons_low
            
            # Consolidation should be relatively tight
            if cons_range > 0.08:  # Max 8% range
                continue
                
            # Determine pattern type based on trend
            if price_change > 0:  # Bullish flagpole
                # Look for slight downward drift in consolidation (flag) or converging lines (pennant)
                pattern_type = "Bull Flag" if self._is_flag_pattern(consolidation_data) else "Bull Pennant"
                entry_price = cons_high * 1.01
                target_price = entry_price + abs(flagpole_data['close'].iloc[-1] - flagpole_data['close'].iloc[0])
                stop_loss = cons_low * 0.98
                
            else:  # Bearish flagpole
                pattern_type = "Bear Flag" if self._is_flag_pattern(consolidation_data) else "Bear Pennant"
                entry_price = cons_low * 0.99
                target_price = entry_price - abs(flagpole_data['close'].iloc[-1] - flagpole_data['close'].iloc[0])
                stop_loss = cons_high * 1.02
                
            confidence = self._calculate_flag_pennant_confidence(flagpole_data, consolidation_data, price_change)
            
            if confidence >= self.min_confidence:
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type=pattern_type,
                    confidence=confidence,
                    start_date=data.index[flagpole_start],
                    end_date=data.index[consolidation_end],
                    entry_price=entry_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    pattern_data={
                        'flagpole_start': flagpole_start,
                        'flagpole_move': price_change,
                        'consolidation_range': cons_range,
                        'breakout_direction': 'bullish' if price_change > 0 else 'bearish'
                    },
                    description=f"{pattern_type} with {abs(price_change):.1%} flagpole move"
                )
                
                patterns.append(pattern)
                
        return patterns
        
    def detect_wedges(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect rising and falling wedge patterns"""
        
        patterns = []
        
        if len(data) < 20:
            return patterns
            
        # Find peaks and troughs for wedge lines
        peaks = self._find_peaks(data['high'], window=3)
        troughs = self._find_troughs(data['low'], window=3)
        
        if len(peaks) < 3 or len(troughs) < 3:
            return patterns
            
        # Check for wedge patterns using recent peaks and troughs
        recent_peaks = peaks[-4:] if len(peaks) >= 4 else peaks
        recent_troughs = troughs[-4:] if len(troughs) >= 4 else troughs
        
        # Calculate trend lines
        peak_trend = self._calculate_trend(recent_peaks)
        trough_trend = self._calculate_trend(recent_troughs)
        
        # Rising Wedge (both lines rising, converging - bearish)
        if peak_trend > 0 and trough_trend > 0 and peak_trend < trough_trend * 2:
            confidence = self._calculate_wedge_confidence(recent_peaks, recent_troughs, "rising")
            
            if confidence >= self.min_confidence:
                # Bearish breakout expected
                support_line = self._extrapolate_trendline(recent_troughs, len(data) - 1)
                entry_price = support_line * 0.99
                
                # Target based on wedge height
                wedge_height = recent_peaks[-1][1] - recent_troughs[0][1]
                target_price = entry_price - wedge_height
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Rising Wedge",
                    confidence=confidence,
                    start_date=data.index[min(recent_peaks[0][0], recent_troughs[0][0])],
                    end_date=data.index[max(recent_peaks[-1][0], recent_troughs[-1][0])],
                    entry_price=entry_price,
                    target_price=target_price,
                    stop_loss=recent_peaks[-1][1] * 1.02,
                    pattern_data={
                        'peak_trend': peak_trend,
                        'trough_trend': trough_trend,
                        'wedge_type': 'rising'
                    },
                    description="Bearish rising wedge pattern - expect downward breakout"
                )
                
                patterns.append(pattern)
                
        # Falling Wedge (both lines falling, converging - bullish)
        elif peak_trend < 0 and trough_trend < 0 and abs(peak_trend) < abs(trough_trend) * 2:
            confidence = self._calculate_wedge_confidence(recent_peaks, recent_troughs, "falling")
            
            if confidence >= self.min_confidence:
                # Bullish breakout expected
                resistance_line = self._extrapolate_trendline(recent_peaks, len(data) - 1)
                entry_price = resistance_line * 1.01
                
                # Target based on wedge height
                wedge_height = recent_peaks[0][1] - recent_troughs[-1][1]
                target_price = entry_price + wedge_height
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Falling Wedge",
                    confidence=confidence,
                    start_date=data.index[min(recent_peaks[0][0], recent_troughs[0][0])],
                    end_date=data.index[max(recent_peaks[-1][0], recent_troughs[-1][0])],
                    entry_price=entry_price,
                    target_price=target_price,
                    stop_loss=recent_troughs[-1][1] * 0.98,
                    pattern_data={
                        'peak_trend': peak_trend,
                        'trough_trend': trough_trend,
                        'wedge_type': 'falling'
                    },
                    description="Bullish falling wedge pattern - expect upward breakout"
                )
                
                patterns.append(pattern)
                
        return patterns
        
    def detect_candlestick_patterns(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect candlestick patterns"""
        
        patterns = []
        
        if len(data) < 3 or 'open' not in data.columns:
            return patterns
            
        # Calculate candlestick metrics
        body_size = abs(data['close'] - data['open'])
        total_range = data['high'] - data['low']
        upper_shadow = data['high'] - np.maximum(data['open'], data['close'])
        lower_shadow = np.minimum(data['open'], data['close']) - data['low']
        
        # Doji patterns
        doji_threshold = 0.1
        is_doji = (body_size / total_range) < doji_threshold
        
        for i in range(len(data)):
            if i == 0:
                continue
                
            current_date = data.index[i]
            
            # Doji
            if is_doji.iloc[i]:
                confidence = 0.7 if total_range.iloc[i] > total_range.iloc[max(0, i-5):i].mean() else 0.6
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Doji",
                    confidence=confidence,
                    start_date=current_date,
                    end_date=current_date,
                    pattern_data={'doji_type': 'standard'},
                    description="Doji candlestick - potential reversal signal"
                )
                patterns.append(pattern)
                
            # Hammer/Hanging Man
            elif (lower_shadow.iloc[i] > 2 * body_size.iloc[i] and 
                  upper_shadow.iloc[i] < body_size.iloc[i]):
                
                is_hammer = data['close'].iloc[i] > data['close'].iloc[i-1]  # After downtrend
                pattern_type = "Hammer" if is_hammer else "Hanging Man"
                confidence = 0.75 if is_hammer else 0.70
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type=pattern_type,
                    confidence=confidence,
                    start_date=current_date,
                    end_date=current_date,
                    pattern_data={'shadow_ratio': lower_shadow.iloc[i] / body_size.iloc[i]},
                    description=f"{pattern_type} candlestick pattern"
                )
                patterns.append(pattern)
                
            # Shooting Star
            elif (upper_shadow.iloc[i] > 2 * body_size.iloc[i] and 
                  lower_shadow.iloc[i] < body_size.iloc[i]):
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Shooting Star",
                    confidence=0.72,
                    start_date=current_date,
                    end_date=current_date,
                    pattern_data={'shadow_ratio': upper_shadow.iloc[i] / body_size.iloc[i]},
                    description="Shooting star - bearish reversal signal"
                )
                patterns.append(pattern)
                
        return patterns
        
    def detect_breakouts(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect breakout patterns from support/resistance levels"""
        
        patterns = []
        
        if len(data) < 20:
            return patterns
            
        # Find support and resistance levels
        support_resistance = self._find_support_resistance_levels(data)
        
        current_price = data['close'].iloc[-1]
        recent_volume = data['volume'].iloc[-5:].mean() if 'volume' in data.columns else None
        avg_volume = data['volume'].mean() if 'volume' in data.columns else None
        
        for level in support_resistance:
            price_level = level['price']
            level_type = level['type']  # 'support' or 'resistance'
            strength = level['strength']
            
            # Check for breakout
            if level_type == 'resistance' and current_price > price_level * 1.005:  # 0.5% above resistance
                # Bullish breakout
                confidence = min(0.9, 0.5 + strength * 0.4)
                
                # Volume confirmation
                if recent_volume and avg_volume and recent_volume > avg_volume * 1.2:
                    confidence += 0.1
                    
                target_price = price_level + (price_level - level.get('nearest_support', price_level * 0.95))
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Resistance Breakout",
                    confidence=confidence,
                    start_date=data.index[-1],
                    end_date=data.index[-1],
                    entry_price=current_price,
                    target_price=target_price,
                    stop_loss=price_level * 0.98,
                    pattern_data={
                        'resistance_level': price_level,
                        'strength': strength,
                        'volume_confirmation': recent_volume > avg_volume * 1.2 if recent_volume else False
                    },
                    description=f"Bullish breakout above resistance at {price_level:.2f}"
                )
                patterns.append(pattern)
                
            elif level_type == 'support' and current_price < price_level * 0.995:  # 0.5% below support
                # Bearish breakdown
                confidence = min(0.9, 0.5 + strength * 0.4)
                
                # Volume confirmation
                if recent_volume and avg_volume and recent_volume > avg_volume * 1.2:
                    confidence += 0.1
                    
                target_price = price_level - (level.get('nearest_resistance', price_level * 1.05) - price_level)
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type="Support Breakdown",
                    confidence=confidence,
                    start_date=data.index[-1],
                    end_date=data.index[-1],
                    entry_price=current_price,
                    target_price=target_price,
                    stop_loss=price_level * 1.02,
                    pattern_data={
                        'support_level': price_level,
                        'strength': strength,
                        'volume_confirmation': recent_volume > avg_volume * 1.2 if recent_volume else False
                    },
                    description=f"Bearish breakdown below support at {price_level:.2f}"
                )
                patterns.append(pattern)
                
        return patterns
        
    def detect_volume_patterns(self, data: pd.DataFrame, symbol: str) -> List[PatternResult]:
        """Detect volume-based patterns"""
        
        patterns = []
        
        if 'volume' not in data.columns or len(data) < 10:
            return patterns
            
        # Volume spike with price movement
        avg_volume = data['volume'].rolling(20).mean()
        current_volume = data['volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume.iloc[-1] if avg_volume.iloc[-1] > 0 else 0
        
        if volume_ratio > 2.0:  # Volume spike
            price_change = (data['close'].iloc[-1] - data['close'].iloc[-2]) / data['close'].iloc[-2]
            
            if abs(price_change) > 0.02:  # Significant price movement
                pattern_type = "Volume Breakout" if price_change > 0 else "Volume Breakdown"
                confidence = min(0.85, 0.5 + volume_ratio * 0.1)
                
                pattern = PatternResult(
                    symbol=symbol,
                    pattern_type=pattern_type,
                    confidence=confidence,
                    start_date=data.index[-1],
                    end_date=data.index[-1],
                    pattern_data={
                        'volume_ratio': volume_ratio,
                        'price_change': price_change,
                        'current_volume': current_volume,
                        'avg_volume': avg_volume.iloc[-1]
                    },
                    description=f"High volume {pattern_type.lower()} with {volume_ratio:.1f}x normal volume"
                )
                patterns.append(pattern)
                
        return patterns
        
    # Helper methods
    def _find_peaks(self, prices: pd.Series, window: int) -> List[Tuple[int, float]]:
        """Find local peaks in price series"""
        peaks = []
        for i in range(window, len(prices) - window):
            if prices.iloc[i] == prices.iloc[i-window:i+window+1].max():
                peaks.append((i, prices.iloc[i]))
        return peaks
        
    def _find_troughs(self, prices: pd.Series, window: int) -> List[Tuple[int, float]]:
        """Find local troughs in price series"""
        troughs = []
        for i in range(window, len(prices) - window):
            if prices.iloc[i] == prices.iloc[i-window:i+window+1].min():
                troughs.append((i, prices.iloc[i]))
        return troughs
        
    def _calculate_trend(self, points: List[Tuple[int, float]]) -> float:
        """Calculate trend slope from points"""
        if len(points) < 2:
            return 0
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        slope, _, _, _, _ = stats.linregress(x, y)
        return slope
        
    def _calculate_hns_confidence(self, left_shoulder, head, right_shoulder, neckline) -> float:
        """Calculate confidence for head and shoulders pattern"""
        base_confidence = 0.6
        
        # Symmetry bonus
        shoulder_ratio = min(left_shoulder[1], right_shoulder[1]) / max(left_shoulder[1], right_shoulder[1])
        symmetry_bonus = (shoulder_ratio - 0.9) * 2 if shoulder_ratio > 0.9 else 0
        
        # Head prominence bonus
        head_prominence = (head[1] - max(left_shoulder[1], right_shoulder[1])) / head[1]
        prominence_bonus = min(0.2, head_prominence * 2)
        
        return min(0.95, base_confidence + symmetry_bonus + prominence_bonus)
        
    def _calculate_triangle_confidence(self, peaks, troughs, triangle_type) -> float:
        """Calculate confidence for triangle patterns"""
        base_confidence = 0.65
        
        # More touches = higher confidence
        touch_bonus = (len(peaks) + len(troughs) - 4) * 0.05
        
        # Volume should decrease in triangle
        volume_bonus = 0.05  # Simplified
        
        return min(0.9, base_confidence + touch_bonus + volume_bonus)
        
    def _calculate_double_pattern_confidence(self, point1, point2, middle_point, pattern_type) -> float:
        """Calculate confidence for double top/bottom patterns"""
        base_confidence = 0.7
        
        # Price similarity bonus
        price_similarity = 1 - abs(point1[1] - point2[1]) / point1[1]
        similarity_bonus = (price_similarity - 0.95) * 2 if price_similarity > 0.95 else 0
        
        # Time separation bonus (not too close, not too far)
        time_diff = abs(point1[0] - point2[0])
        if 5 <= time_diff <= 25:
            time_bonus = 0.1
        else:
            time_bonus = 0
            
        return min(0.9, base_confidence + similarity_bonus + time_bonus)
        
    def _calculate_cup_handle_confidence(self, cup_data, handle_data, cup_depth, handle_depth) -> float:
        """Calculate confidence for cup and handle pattern"""
        base_confidence = 0.6
        
        # Optimal cup depth bonus
        if 0.15 <= cup_depth <= 0.25:
            depth_bonus = 0.15
        else:
            depth_bonus = 0
            
        # Handle characteristics bonus
        if handle_depth < cup_depth * 0.3:  # Shallow handle
            handle_bonus = 0.1
        else:
            handle_bonus = 0
            
        return min(0.9, base_confidence + depth_bonus + handle_bonus)
        
    def _calculate_flag_pennant_confidence(self, flagpole_data, consolidation_data, price_change) -> float:
        """Calculate confidence for flag and pennant patterns"""
        base_confidence = 0.65
        
        # Strong flagpole bonus
        flagpole_strength = abs(price_change)
        if flagpole_strength > 0.08:  # > 8% move
            strength_bonus = 0.15
        else:
            strength_bonus = flagpole_strength * 1.5
            
        # Tight consolidation bonus
        cons_tightness = 1 - ((consolidation_data['high'].max() - consolidation_data['low'].min()) / 
                             consolidation_data['close'].mean())
        tightness_bonus = cons_tightness * 0.1
        
        return min(0.9, base_confidence + strength_bonus + tightness_bonus)
        
    def _calculate_wedge_confidence(self, peaks, troughs, wedge_type) -> float:
        """Calculate confidence for wedge patterns"""
        base_confidence = 0.6
        
        # Convergence quality bonus
        peak_r2 = self._calculate_trendline_r2(peaks)
        trough_r2 = self._calculate_trendline_r2(troughs)
        convergence_bonus = (peak_r2 + trough_r2) * 0.15
        
        return min(0.9, base_confidence + convergence_bonus)
        
    def _calculate_trendline_r2(self, points) -> float:
        """Calculate R² for trendline fit"""
        if len(points) < 3:
            return 0
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        _, _, r_value, _, _ = stats.linregress(x, y)
        return r_value ** 2
        
    def _is_flag_pattern(self, data) -> bool:
        """Determine if consolidation is more flag-like (parallel) vs pennant-like (converging)"""
        # Simplified: check if range is relatively stable
        ranges = data['high'] - data['low']
        range_stability = 1 - (ranges.std() / ranges.mean())
        return range_stability > 0.7
        
    def _extrapolate_trendline(self, points, target_x) -> float:
        """Extrapolate trendline to target x value"""
        if len(points) < 2:
            return points[0][1] if points else 0
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        slope, intercept, _, _, _ = stats.linregress(x, y)
        return slope * target_x + intercept
        
    def _find_support_resistance_levels(self, data) -> List[Dict]:
        """Find support and resistance levels using clustering"""
        # Get all highs and lows
        all_prices = list(data['high']) + list(data['low'])
        
        # Use DBSCAN clustering to find price levels
        prices_array = np.array(all_prices).reshape(-1, 1)
        clustering = DBSCAN(eps=np.std(all_prices) * 0.5, min_samples=3).fit(prices_array)
        
        levels = []
        for cluster_id in set(clustering.labels_):
            if cluster_id == -1:  # Noise
                continue
                
            cluster_prices = [all_prices[i] for i, label in enumerate(clustering.labels_) if label == cluster_id]
            avg_price = np.mean(cluster_prices)
            
            # Determine if support or resistance based on recent price action
            recent_price = data['close'].iloc[-1]
            level_type = 'resistance' if avg_price > recent_price else 'support'
            
            # Calculate strength based on number of touches
            strength = len(cluster_prices) / len(all_prices)
            
            levels.append({
                'price': avg_price,
                'type': level_type,
                'strength': strength,
                'touches': len(cluster_prices)
            })
            
        return sorted(levels, key=lambda x: x['strength'], reverse=True)


# Global pattern scanner instance
pattern_scanner = AdvancedPatternScanner()
