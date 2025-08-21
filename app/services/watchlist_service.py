"""
Unified watchlist service that handles both old and new watchlist models.
"""
from ..extensions import db
from ..models.watchlist import Watchlist, WatchlistItem, WatchlistStock
from .data_service import DataService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WatchlistService:
    @staticmethod
    def get_user_watchlist(user_id):
        """Get all watchlist items for a user, handling both old and new models"""
        try:
            # Try new model first
            watchlist = Watchlist.query.filter_by(user_id=user_id).first()
            if watchlist and watchlist.items:
                return watchlist
                
            # Try old model
            watchlist = Watchlist.query.filter_by(user_id=user_id).first()
            if watchlist and watchlist.stocks:
                return watchlist
                
            # Create new watchlist if none exists
            watchlist = Watchlist(
                name="Min Watchlist",
                user_id=user_id,
                created_at=datetime.utcnow()
            )
            db.session.add(watchlist)
            db.session.commit()
            return watchlist
            
        except Exception as e:
            logger.error(f"Error getting watchlist: {e}")
            return None

    @staticmethod
    def add_to_watchlist(user_id, symbol, name=None):
        """Add a symbol to user's watchlist"""
        try:
            watchlist = WatchlistService.get_user_watchlist(user_id)
            if not watchlist:
                return False, "Kunne ikke finne eller opprette watchlist"

            # Check if symbol already exists
            if any(s.ticker == symbol for s in watchlist.stocks):
                return False, "Aksjen er allerede i watchlist"

            # Get stock info to validate symbol
            stock_info = DataService.get_stock_info(symbol)
            if not stock_info:
                return False, "Kunne ikke finne aksjen"

            # Add using current model
            stock = WatchlistStock(
                watchlist_id=watchlist.id,
                ticker=symbol
            )
            db.session.add(stock)
            db.session.commit()
            return True, "Aksjen ble lagt til i watchlist"

        except Exception as e:
            logger.error(f"Error adding to watchlist: {e}")
            db.session.rollback()
            return False, f"En feil oppstod: {str(e)}"

    @staticmethod
    def remove_from_watchlist(user_id, symbol):
        """Remove a symbol from user's watchlist"""
        try:
            watchlist = WatchlistService.get_user_watchlist(user_id)
            if not watchlist:
                return False, "Kunne ikke finne watchlist"

            # Find and remove stock
            stock = WatchlistStock.query.filter_by(
                watchlist_id=watchlist.id,
                ticker=symbol
            ).first()

            if stock:
                db.session.delete(stock)
                db.session.commit()
                return True, "Aksjen ble fjernet fra watchlist"
            return False, "Aksjen ble ikke funnet i watchlist"

        except Exception as e:
            logger.error(f"Error removing from watchlist: {e}")
            db.session.rollback()
            return False, f"En feil oppstod: {str(e)}"

    @staticmethod
    def get_watchlist_data(user_id):
        """Get full watchlist data including real-time prices and info"""
        try:
            watchlist = WatchlistService.get_user_watchlist(user_id)
            if not watchlist:
                return []

            stocks_data = []
            for stock in watchlist.stocks:
                try:
                    # Get real-time data
                    stock_info = DataService.get_stock_info(stock.ticker)
                    current_price = stock_info.get('regularMarketPrice', 0) if stock_info else 0
                    prev_close = stock_info.get('regularMarketPreviousClose', current_price) if stock_info else current_price
                    change = current_price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                    stocks_data.append({
                        'ticker': stock.ticker,
                        'name': stock_info.get('longName', stock.ticker) if stock_info else stock.ticker,
                        'current_price': current_price,
                        'change': change,
                        'change_percent': change_percent,
                        'volume': stock_info.get('regularMarketVolume', 0) if stock_info else 0,
                        'market_cap': stock_info.get('marketCap', 0) if stock_info else 0,
                        'pe_ratio': stock_info.get('trailingPE', None) if stock_info else None,
                        'added_at': stock.added_at.strftime('%Y-%m-%d') if stock.added_at else None
                    })
                except Exception as e:
                    logger.error(f"Error processing stock {stock.ticker}: {e}")
                    # Add basic info even if data fetch fails
                    stocks_data.append({
                        'ticker': stock.ticker,
                        'name': stock.ticker,
                        'error': True,
                        'error_message': 'Kunne ikke hente data'
                    })

            return stocks_data

        except Exception as e:
            logger.error(f"Error getting watchlist data: {e}")
            return []
