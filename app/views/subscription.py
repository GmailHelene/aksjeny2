from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import app, db
from datetime import datetime, timedelta

@app.route('/my-subscription')
@login_required
def my_subscription():
    """Display user's subscription details"""
    try:
        # Calculate renewal date if premium
        renewal_date = None
        if current_user.is_premium and hasattr(current_user, 'subscription_end'):
            renewal_date = current_user.subscription_end
        elif current_user.is_premium:
            # Default to 30 days from now if no end date set
            renewal_date = datetime.utcnow() + timedelta(days=30)
        
        return render_template('subscription/my-subscription.html',
                             renewal_date=renewal_date)
    except Exception as e:
        app.logger.error(f"Subscription page error: {str(e)}")
        flash('Kunne ikke laste abonnementsinformasjon', 'error')
        return redirect(url_for('index'))

@app.route('/subscription/upgrade')
@login_required
def subscription_upgrade():
    """Redirect to upgrade page"""
    return render_template('subscription/upgrade.html')

@app.route('/subscription/checkout/<plan>')
@login_required
def subscription_checkout(plan):
    """Handle subscription checkout"""
    plans = {
        'monthly': {'name': 'Månedlig', 'price': 299},
        'yearly': {'name': 'Årlig', 'price': 2499},
        'lifetime': {'name': 'Livstid', 'price': 9999}
    }
    
    if plan not in plans:
        flash('Ugyldig abonnementsplan', 'error')
        return redirect(url_for('my_subscription'))
    
    return render_template('subscription/checkout.html',
                         plan=plan,
                         plan_details=plans[plan])
