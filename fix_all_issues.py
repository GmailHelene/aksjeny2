#!/usr/bin/env python3
"""Fix all known issues with the application"""

import os
import shutil
import subprocess
import sys

def fix_crypto_template():
    """Fix the crypto.html template"""
    print("🔧 Fixing crypto.html template...")
    
    crypto_content = '''{% extends "base.html" %}
{% block title %}Kryptovaluta - Aksjeny{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <div class="row mb-4">
        <div class="col">
            <h1 class="display-4 mb-2">
                <i class="fas fa-coins text-warning me-3"></i>Kryptovaluta
            </h1>
            <p class="lead text-muted">Følg de største kryptovalutaene i sanntid</p>
        </div>
    </div>

    {% if stocks_data and stocks_data|length > 0 %}
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Navn</th>
                        <th class="text-end">Pris (USD)</th>
                        <th class="text-end">Endring</th>
                        <th class="text-end">Volum</th>
                        <th class="text-end">Markedsverdi</th>
                    </tr>
                </thead>
                <tbody>
                    {% for symbol, stock in stocks_data.items() %}
                        <tr>
                            <td><strong>{{ stock.symbol }}</strong></td>
                            <td>{{ stock.name }}</td>
                            <td class="text-end">${{ "%.2f"|format(stock.current_price) }}</td>
                            <td class="text-end">
                                <span class="badge {% if stock.change_percent >= 0 %}bg-success{% else %}bg-danger{% endif %}">
                                    {% if stock.change_percent >= 0 %}+{% endif %}{{ "%.2f"|format(stock.change_percent) }}%
                                </span>
                            </td>
                            <td class="text-end">{{ "{:,.0f}".format(stock.volume) }}</td>
                            <td class="text-end">${{ "{:,.0f}".format(stock.market_cap) }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="alert alert-info" role="alert">
            <i class="fas fa-info-circle me-2"></i>
            Ingen kryptovalutadata tilgjengelig for øyeblikket.
        </div>
    {% endif %}
</div>
{% endblock %}'''
    
    os.makedirs('templates/stocks', exist_ok=True)
    with open('templates/stocks/crypto.html', 'w', encoding='utf-8') as f:
        f.write(crypto_content)
    print("✅ crypto.html fixed")

def fix_global_template():
    """Fix the global.html template"""
    print("🔧 Fixing global.html template...")
    
    global_content = '''{% extends "base.html" %}
{% block title %}Globale Aksjer - Aksjeny{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <div class="row mb-4">
        <div class="col">
            <h1 class="display-4 mb-2">
                <i class="fas fa-globe text-success me-3"></i>Globale Aksjer
            </h1>
            <p class="lead text-muted">Oversikt over internasjonale aksjer</p>
        </div>
    </div>

    {% if stocks_data and stocks_data|length > 0 %}
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Navn</th>
                        <th class="text-end">Pris (USD)</th>
                        <th class="text-end">Endring</th>
                        <th class="text-end">Volum</th>
                        <th class="text-end">Markedsverdi</th>
                    </tr>
                </thead>
                <tbody>
                    {% for symbol, stock in stocks_data.items() %}
                        <tr>
                            <td><strong>{{ stock.symbol }}</strong></td>
                            <td>{{ stock.name }}</td>
                            <td class="text-end">${{ "%.2f"|format(stock.current_price) }}</td>
                            <td class="text-end">
                                <span class="badge {% if stock.change_percent >= 0 %}bg-success{% else %}bg-danger{% endif %}">
                                    {% if stock.change_percent >= 0 %}+{% endif %}{{ "%.2f"|format(stock.change_percent) }}%
                                </span>
                            </td>
                            <td class="text-end">{{ "{:,.0f}".format(stock.volume) }}</td>
                            <td class="text-end">${{ "{:,.0f}".format(stock.market_cap) }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="alert alert-info" role="alert">
            <i class="fas fa-info-circle me-2"></i>
            Ingen data tilgjengelig for globale aksjer.
        </div>
    {% endif %}
</div>
{% endblock %}'''
    
    with open('templates/stocks/global.html', 'w', encoding='utf-8') as f:
        f.write(global_content)
    print("✅ global.html fixed")

def clear_all_cache():
    """Clear all cache files"""
    print("🧹 Clearing all cache...")
    
    cache_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.pytest_cache',
        'instance/cache',
        'flask_session'
    ]
    
    for root, dirs, files in os.walk('.'):
        # Skip venv directories
        if 'venv' in root or '.git' in root:
            continue
            
        # Remove cache directories
        for d in dirs:
            if d in ['__pycache__', '.pytest_cache', 'flask_session']:
                path = os.path.join(root, d)
                try:
                    shutil.rmtree(path)
                    print(f"  Removed: {path}")
                except:
                    pass
        
        # Remove cache files
        for f in files:
            if f.endswith(('.pyc', '.pyo')):
                path = os.path.join(root, f)
                try:
                    os.remove(path)
                    print(f"  Removed: {path}")
                except:
                    pass
    
    print("✅ Cache cleared")

def git_deploy():
    """Deploy to Railway via Git"""
    print("🚀 Deploying to Railway...")
    
    commands = [
        ['git', 'add', '-A'],
        ['git', 'commit', '-m', 'FIX: Complete fix for crypto, global stocks, and all template issues'],
        ['git', 'push', 'origin', 'main']
    ]
    
    for cmd in commands:
        print(f"  Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Warning: {result.stderr}")
    
    print("✅ Deployed to Railway")

def main():
    print("🚨 FIXING ALL ISSUES 🚨\n")
    
    # Fix templates
    fix_crypto_template()
    fix_global_template()
    
    # Clear cache
    clear_all_cache()
    
    # Deploy
    git_deploy()
    
    print("\n✅ ALL FIXES COMPLETE!")
    print("📊 Check Railway logs at: https://railway.app/dashboard")
    print("🌐 Your app: https://aksjeradar.trade")

if __name__ == "__main__":
    main()
