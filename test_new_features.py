import re
from datetime import datetime

def test_economic_indicators_api(client):
    resp = client.get('/market-intel/api/economic-indicators?timeframe=live')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['timeframe'] == 'live'
    for key in ['inflation_rate','interest_rate','unemployment_rate','oil_price','crypto_fear_greed','data_source']:
        assert key in data

    # Test unsupported timeframe fallback
    resp2 = client.get('/market-intel/api/economic-indicators?timeframe=weekly')
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    # weekly allowed; ensure timeframe echoes
    assert data2['timeframe'] == 'weekly'


def test_technical_cache_flag(client):
    # First call (expect cache_hit false)
    r1 = client.get('/stocks/details/AAPL')
    assert r1.status_code == 200
    assert b'data-tech-cache-hit="false"' in r1.data
    # Second call (within TTL) should be cache hit
    r2 = client.get('/stocks/details/AAPL')
    assert r2.status_code == 200
    assert b'data-tech-cache-hit="true"' in r2.data


def test_insider_trading_search_filters(client):
    # Use a plausible symbol; route redirects if missing
    r = client.get('/insider-trading/search?symbol=EQNR&period=30&transaction_type=buy&sort=value_desc')
    # Could redirect if no data; accept 200 or redirect as non-failure but prefer 200
    assert r.status_code in (200,302,301)
    if r.status_code == 200:
        # Look for selected symbol badge or summary block
        assert b'EQNR' in r.data


def test_daily_view_analysis_valid_and_invalid_date(client):
    today_iso = datetime.utcnow().strftime('%Y-%m-%d')
    r_valid = client.get(f'/daily-view/analysis/{today_iso}')
    assert r_valid.status_code == 200
    assert today_iso.encode() in r_valid.data

    r_invalid = client.get('/daily-view/analysis/2025-99-99')
    # Should not 500
    assert r_invalid.status_code == 200
    # Falls back to today => ensure not literal invalid string present (best effort)
    assert b'2025-99-99' not in r_invalid.data
