from app import create_app, db
from app.models.user import User

app = create_app()

results = {}
with app.app_context():
    client = app.test_client()
    # Anonymous request
    anon_resp = client.get('/portfolio/', follow_redirects=True)
    anon_text = anon_resp.data.decode('utf-8', errors='ignore')
    results['anonymous_status'] = anon_resp.status_code
    # Norwegian phrases (partial to avoid brittle diacritic issues)
    results['anonymous_contains_create_btn'] = ('Opprett din første portef' in anon_text) or ('Opprett ny portef' in anon_text)

    # Logged-in request (pick first user)
    user = User.query.first()
    if user:
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True
        auth_resp = client.get('/portfolio/', follow_redirects=True)
        auth_text = auth_resp.data.decode('utf-8', errors='ignore')
        results['auth_status'] = auth_resp.status_code
        # Look for table header or action buttons
        results['auth_has_table'] = ('Ticker' in auth_text) or ('Ingen portef' in auth_text)
    else:
        results['auth_status'] = 'NO_USER'

print(results)
