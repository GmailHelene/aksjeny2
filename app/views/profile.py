from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import app
from ..models import Portfolio

@app.route('/profile')
@login_required
def profile():
    try:
        user = current_user
        portfolios = Portfolio.query.filter_by(user_id=user.id).all()
        return render_template('profile/profile.html', 
                             user=user, 
                             portfolios=portfolios)
    except Exception as e:
        app.logger.error(f"Profile error: {str(e)}")
        flash('Kunne ikke laste profilen. Prøv igjen senere.', 'error')
        return redirect(url_for('index'))