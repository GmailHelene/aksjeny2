def get_sector_data():
    try:
        from flask_login import current_user
        import requests
        # If user is authenticated, fetch real sector data from API
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            try:
                # Hent sektordata fra API
                response = requests.get('http://localhost:5000/market/sectors', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and 'sectors' in data:
                        return data['sectors']
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
        # TODO: Replace with real market intelligence data fetching logic
        return [
            {'title': 'Global Market Trends', 'summary': 'Markets are up 2% this week.'},
            {'title': 'Sector Rotation', 'summary': 'Investors moving from tech to healthcare.'}
        ]
    else:
        # Demo data for non-authenticated users
        return [
            {'title': 'Demo Market Intelligence', 'summary': 'Demo summary.'}
        ]

def get_analyst_coverage_data(real=False):
    if real:
        # TODO: Replace with real analyst coverage data fetching logic
        return [
            {'analyst': 'John Doe', 'rating': 'Buy', 'target_price': 150},
            {'analyst': 'Jane Smith', 'rating': 'Hold', 'target_price': 120}
        ]
    else:
        # Demo data for non-authenticated users
        return [
            {'analyst': 'Demo Analyst', 'rating': 'Demo', 'target_price': 0}
        ]
