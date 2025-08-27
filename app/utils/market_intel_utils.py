def get_sector_data():
    from flask_login import current_user
    # If user is authenticated, fetch real sector data
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # TODO: Replace with real sector data fetching logic from DB or API
        # Example: fetch from external API or database
        # This is a placeholder for real implementation
        return [
            {'name': 'Technology', 'performance': 5.2},
            {'name': 'Healthcare', 'performance': 3.8},
            {'name': 'Finance', 'performance': 2.1}
        ]
    else:
        # Non-authenticated users get demo data
        return generate_demo_sectors()

def generate_demo_sectors():
    # Dummy implementation: Replace with real demo sector data logic
    return [
        {'name': 'Demo Sector', 'performance': 0.0}
    ]
