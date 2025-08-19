from flask import jsonify, request
from flask_login import login_required
from . import api_bp
from ..services import data_service

@api_bp.route('/insider-trades/<symbol>')
@login_required
def get_insider_trades(symbol):
    try:
        trades = data_service.get_insider_trades(symbol)
        return jsonify({
            'success': True,
            'symbol': symbol,
            'trades': trades
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500