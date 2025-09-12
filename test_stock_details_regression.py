import re

from flask import url_for

# Use authenticated client to avoid login redirect (route requires auth context for full rendering)
def test_stock_details_full_template(auth_client):
    client, user = auth_client
    symbol = 'EQNR.OL'
    response = client.get(f'/stocks/details/{symbol}', follow_redirects=False)
    # If we unexpectedly get a redirect, capture for debugging
    assert response.status_code == 200, f'Expected 200 from stock details route, got {response.status_code} (Location={response.headers.get("Location")})'

    html = response.get_data(as_text=True)

    # Should not be just the bare fallback
    assert html.strip() != f'Stock {symbol}', 'Placeholder plain text still returned instead of full template'

    # Look for at least one of known container classes/ids from the real template
    markers = [
        'stock-details-container',
        'data-tradingview-widget',
        'class="stock-overview-tabs"',
        'id="tradingview_widget"'
    ]
    assert any(m in html for m in markers), 'Expected structural markers from full stock details template not found'

    # Ensure basic HTML structure present
    assert '<html' in html.lower() and '</body>' in html.lower(), 'Response does not look like full HTML document'
