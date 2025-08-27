def get_sector_data():
    try:
        from flask_login import current_user
        import requests
        # If user is authenticated, fetch real sector data from API
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            try:
                from app.services.external_data import external_data_service
                overview = external_data_service.get_market_overview()
                if 'sector_performance' in overview:
                    sectors = []
                    for sector, data in overview['sector_performance'].items():
                        sectors.append({
                            'name': sector.title(),
                            'performance': data['performance'],
                            'trend': data['trend']
                        })
                    return sectors
            except Exception as api_error:
                pass  # Faller tilbake til demo-data
        # Non-authenticated users eller feil gir demo-data
        return generate_demo_sectors()
    except Exception as e:
        # If any error, return demo data
        return generate_demo_sectors()

def generate_demo_sectors():
    # Dummy implementation: Replace with real demo sector data logic
    return [
        {'name': 'Demo Sector', 'performance': 0.0}
    ]

def get_market_intelligence_data(real=False):
    if real:
        try:
            from flask_login import current_user
            from app.services.external_data import external_data_service
            if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
                overview = external_data_service.get_market_overview()
                # Format for template: convert dict to list of sections
                result = []
                if 'osebx_index' in overview:
                    result.append({'title': 'OSEBX Index', 'summary': f"Value: {overview['osebx_index']['value']}, Change: {overview['osebx_index']['change']} ({overview['osebx_index']['change_percent']}%), Trend: {overview['osebx_index']['trend']}"})
                if 'top_insider_activity' in overview:
                    summary = ', '.join([f"{a['symbol']}: {a['net_activity']} (Confidence: {a['confidence']})" for a in overview['top_insider_activity']])
                    result.append({'title': 'Top Insider Activity', 'summary': summary})
                if 'analyst_upgrades' in overview:
                    summary = ', '.join([f"{a['symbol']}: {a['from']}→{a['to']} ({a['firm']})" for a in overview['analyst_upgrades']])
                    result.append({'title': 'Analyst Upgrades', 'summary': summary})
                if 'sector_performance' in overview:
                    summary = ', '.join([f"{sector}: {data['performance']}% ({data['trend']})" for sector, data in overview['sector_performance'].items()])
                    result.append({'title': 'Sector Performance', 'summary': summary})
                if 'market_sentiment' in overview:
                    sentiment = overview['market_sentiment']
                    summary = f"Overall: {sentiment['overall']}, Fear/Greed: {sentiment['fear_greed_index']}, Volatility: {sentiment['volatility_index']}"
                    result.append({'title': 'Market Sentiment', 'summary': summary})
                return result
        except Exception as e:
            pass  # Fallback to demo data
        # If error, fallback to demo
        return [
            {'title': 'Demo Market Intelligence', 'summary': 'Demo summary.'}
        ]
    else:
        # Demo data for non-authenticated users
        return [
            {'title': 'Demo Market Intelligence', 'summary': 'Demo summary.'}
        ]

def get_analyst_coverage_data(real=False):
    if real:
        try:
            from flask_login import current_user
            from app.services.external_data import external_data_service
            if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
                top_stocks = ['EQNR', 'DNB', 'TEL', 'AKER', 'MOWI']
                analyst_coverage = {}
                for symbol in top_stocks:
                    try:
                        analyst_data = external_data_service.get_norwegian_analyst_data(symbol)
                        analyst_coverage[symbol] = {
                            'consensus': analyst_data.get('consensus', {}),
                            'recommendations': analyst_data.get('recommendations', [])
                        }
                    except Exception as e:
                        analyst_coverage[symbol] = {
                            'consensus': {'rating': 'HOLD', 'avg_target_price': 0, 'num_analysts': 0},
                            'recommendations': []
                        }
                return analyst_coverage
        except Exception as e:
            pass  # Fallback to demo data
        # If error, fallback to demo
        return {
            'EQNR': {'consensus': {'rating': 'Demo', 'avg_target_price': 0, 'num_analysts': 0}, 'recommendations': []}
        }
    else:
        # Demo data for non-authenticated users
        return [
            {'analyst': 'Demo Analyst', 'rating': 'Demo', 'target_price': 0}
        ]
