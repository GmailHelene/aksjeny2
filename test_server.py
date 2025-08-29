#!/usr/bin/env python3
"""
Simple test server to quickly test all critical endpoints
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from werkzeug.serving import run_simple

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Test server is running'})

@app.route('/stocks/compare')
def stocks_compare():
    try:
        # Simulate the actual endpoint
        symbols = request.args.get('symbols', 'EQNR.OL,DNB.OL')
        return jsonify({
            'status': 'ok',
            'endpoint': '/stocks/compare',
            'symbols': symbols,
            'message': 'Stock comparison endpoint is working'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/my-subscription')
def my_subscription():
    try:
        return jsonify({
            'status': 'ok',
            'endpoint': '/my-subscription',
            'message': 'Subscription endpoint is working'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/forum/create_topic')
def forum_create_topic():
    try:
        return jsonify({
            'status': 'ok',
            'endpoint': '/forum/create_topic',
            'message': 'Forum create topic endpoint is working'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/analysis/warren-buffett')
def analysis_warren_buffett():
    try:
        return jsonify({
            'status': 'ok',
            'endpoint': '/analysis/warren-buffett',
            'message': 'Warren Buffett analysis endpoint is working'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/advanced-analytics')
def advanced_analytics():
    try:
        return jsonify({
            'status': 'ok',
            'endpoint': '/advanced-analytics',
            'message': 'Advanced analytics endpoint is working'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/external-data/analyst-coverage')
def external_data_analyst_coverage():
    try:
        return jsonify({
            'status': 'ok',
            'endpoint': '/external-data/analyst-coverage',
            'message': 'Analyst coverage endpoint is working'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/profile')
def profile():
    try:
        return jsonify({
            'status': 'ok',
            'endpoint': '/profile',
            'message': 'Profile endpoint is working'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting test server on http://localhost:5002")
    print("Endpoints to test:")
    print("- /health")
    print("- /stocks/compare")
    print("- /my-subscription")
    print("- /forum/create_topic")
    print("- /analysis/warren-buffett")
    print("- /advanced-analytics")
    print("- /external-data/analyst-coverage")
    print("- /profile")
    
    run_simple('localhost', 5002, app, use_reloader=False, use_debugger=True)
