@main.route('/profile')
@login_required
def profile():
    """Redirect to the new profile page under /user"""
    return redirect(url_for('profile.profile_page'))
