from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_required, current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@login_required
def my_subscription():
    """Dedicated user subscription management page"""
    try:
        user_subscription = current_user.subscription_status if current_user.is_authenticated else 'free'
        is_premium = user_subscription == 'active'

        if is_premium:
            subscription_info = {
                'status': 'active',
                'plan_name': 'Premium',
                'plan_description': 'Full tilgang til alle analyser og funksjoner',
                'start_date': current_user.created_at if hasattr(current_user, 'created_at') else None,
                'end_date': None,
                'next_billing': None,
                'price': 399,
                'currency': 'NOK',
                'features': [
                    'Ubegrenset tilgang til alle aksjer',
                    'Avanserte analyser (Warren Buffett, Benjamin Graham)',
                    'AI-drevne anbefalinger',
                    'Innsidehandel-overvåkning',
                    'Sanntids prisdata',
                    'Porteføljeoptimalisering',
                    'Backtesting av strategier'
                ],
                'upgrade_options': []
            }
        else:
            subscription_info = {
                'status': 'free',
                'plan_name': 'Gratis',
                'plan_description': 'Grunnleggende tilgang til aksjedata og analyser',
                'start_date': None,
                'end_date': None,
                'next_billing': None,
                'price': 0,
                'currency': 'NOK',
                'features': [
                    'Begrenset tilgang til aksjedata',
                    'Grunnleggende teknisk analyse',
                    'Daglig markedsoversikt'
                ],
                'upgrade_options': [
                    {
                        'name': 'Premium',
                        'price': 399,
                        'billing': 'monthly',
                        'features': [
                            'Ubegrenset tilgang til alle aksjer',
                            'Avanserte analyser (Warren Buffett, Benjamin Graham)',
                            'AI-drevne anbefalinger',
                            'Innsidehandel-overvåkning',
                            'Sanntids prisdata',
                            'Porteføljeoptimalisering og backtesting'
                        ]
                    },
                    {
                        'name': 'Premium',
                        'price': 2499,
                        'billing': 'yearly',
                        'features': [
                            'Alt i månedspakken',
                            'Årlig rabatt (spare 1789 kr)',
                            'Prioritert kundestøtte',
                            'Tidlig tilgang til nye funksjoner',
                            'API-tilgang',
                            'Avanserte screener-filter'
                        ]
                    }
                ]
            }

        is_exempt_user = current_user.email in {
            'helene@luxushair.com', 
            'helene721@gmail.com', 
            'eiriktollan.berntsen@gmail.com',
            'tonjekit91@gmail.com'
        }

        if is_exempt_user:
            subscription_info.update({
                'status': 'active',
                'plan_name': 'Premium',
                'plan_description': 'Full tilgang til alle funksjoner som premium bruker',
                'start_date': datetime.now().date(),
                'end_date': None,
                'next_billing': None,
                'price': 0,
                'currency': 'NOK',
                'features': [
                    'Ubegrenset tilgang til alle aksjer og analyser',
                    'Avanserte analyser (Warren Buffett, Benjamin Graham)',
                    'AI-drevne anbefalinger og porteføljeoptimalisering',
                    'Innsidehandel-overvåkning og sanntids data',
                    'Backtesting og screener-funksjoner',
                    'API-tilgang og prioritert support',
                    'Premium bruker (livstid tilgang)'
                ],
                'is_exempt': True
            })
        elif hasattr(current_user, 'subscription') and current_user.subscription:
            subscription = current_user.subscription
            if hasattr(subscription, 'status') and subscription.status == 'active':
                subscription_info.update({
                    'status': 'active',
                    'plan_name': getattr(subscription, 'plan_name', 'Pro'),
                    'start_date': getattr(subscription, 'start_date', None),
                    'end_date': getattr(subscription, 'end_date', None),
                    'next_billing': getattr(subscription, 'next_billing_date', None),
                    'price': getattr(subscription, 'price', 299),
                    'features': [
                        'Ubegrenset tilgang til alle aksjer',
                        'Avanserte analyser',
                        'AI-drevne anbefalinger',
                        'Sanntids prisdata'
                    ]
                })

        return render_template('subscription_management.html',
                              subscription=subscription_info,
                              user=current_user)
    except Exception as e:
        logger.error(f"Error in subscription page for user {getattr(current_user, 'id', 'unknown')}: {e}")
        flash('Kunne ikke laste abonnementssiden. Prøv igjen senere.', 'error')
        return redirect(url_for('main.profile'))
