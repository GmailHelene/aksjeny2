def test_economic_indicators_timeframe_buttons(auth_client):
    client, user = auth_client
    resp = client.get('/market-intel/economic-indicators')
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    # Check for new timeframe buttons with data-timeframe attributes
    for tf in ['live','daily','weekly']:
        assert f'data-timeframe="{tf}"' in html, f"Timeframe button {tf} missing"
    # Ensure ARIA pressed attribute present for at least the active one
    assert 'aria-pressed="true"' in html
