from flask import Blueprint, current_app, request, jsonify, session, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from flask_wtf.csrf import validate_csrf
from werkzeug.exceptions import BadRequest
from ..models.user import User
from ..extensions import db
from datetime import datetime, timedelta
import stripe

stripe_bp = Blueprint('stripe', __name__, url_prefix='/stripe')

@stripe_bp.record_once
def on_register(state):
    """Non-blocking Stripe initialization"""
    try:
        # Set Stripe API key but don't test connection during startup
        stripe.api_key = state.app.config['STRIPE_SECRET_KEY']
        state.app.logger.info('Stripe API key configured')
        
        # Cache Stripe configuration values
        state.app.config['_STRIPE_CONFIG_CACHED'] = True
        
        # Only validate in production, and only if explicitly enabled
        if state.app.config.get('IS_REAL_PRODUCTION') and state.app.config.get('VALIDATE_STRIPE_ON_STARTUP'):
            # Test connection in background (don't block startup)
            import threading
            def test_stripe_connection():
                try:
                    # Cache common Stripe resources for faster checkout process
                    prices = stripe.Price.list(limit=10, active=True)
                    state.app.config['_STRIPE_PRICES_CACHE'] = {p.id: p for p in prices.data}
                    state.app.logger.info(f'Cached {len(prices.data)} Stripe prices for faster checkout')
                    
                    state.app.logger.info('Stripe connection validated successfully')
                except Exception as e:
                    state.app.logger.error(f'Stripe connection test failed: {e}')
            
            thread = threading.Thread(target=test_stripe_connection)
            thread.daemon = True
            thread.start()
        
    except Exception as e:
        state.app.logger.error(f'Failed to initialize Stripe: {str(e)}')
        # Don't raise - allow app to start without Stripe

@stripe_bp.route('/create-checkout-session', methods=['POST', 'GET'])
@login_required
def create_checkout_session():
    """Create a Stripe checkout session for subscription purchase"""
    try:
        # Handle both POST and GET requests
        if request.method == 'GET':
            # Redirect GET requests to subscription page
            return redirect(url_for('main.subscription'))
        
        # Validate CSRF token for POST requests - more lenient approach
        csrf_token = request.form.get('csrf_token')
        if not csrf_token:
            current_app.logger.warning("No CSRF token provided")
            flash('Sikkerhetsfeil: Manglende sikkerhetstoken. Prøv å oppdater siden.', 'danger')
            return redirect(url_for('pricing.pricing_page'))
            
        try:
            validate_csrf(csrf_token)
        except Exception as e:
            current_app.logger.warning(f"CSRF validation failed: {e}")
            # Instead of failing, try to regenerate and redirect
            flash('Sikkerhetssession utløpt. Siden har blitt oppdatert - prøv igjen.', 'info')
            return redirect(url_for('pricing.pricing_page'))
            
        subscription_type = request.form.get('subscription_type')
        if not subscription_type:
            flash('Ingen abonnementstype valgt.', 'warning')
            return redirect(url_for('main.subscription'))

        # Verify user is authenticated
        if not current_user.is_authenticated:
            flash('Du må være innlogget for å kjøpe abonnement.', 'warning')
            return redirect(url_for('auth.login', next=url_for('main.subscription')))

        # Check if Stripe is properly configured
        stripe_secret_key = current_app.config.get('STRIPE_SECRET_KEY')
        if not stripe_secret_key:
            current_app.logger.warning("⚠️ STRIPE_SECRET_KEY not found - using demo mode")
            flash('Demo modus: Betalingssystem er ikke konfigurert. Dette ville normalt koble til Stripe for ekte betalinger.', 'info')
            return redirect(url_for('main.subscription_success', demo=True))
        
        # Check for dummy/test keys in production
        if (stripe_secret_key.startswith('sk_test_dummy') or 
            stripe_secret_key == 'sk_test_dummy_key_for_development_only' or
            stripe_secret_key == 'your-stripe-secret-key-here'):
            current_app.logger.warning("⚠️ Using demo Stripe configuration - Payment system in demo mode")
            flash('Demo modus: Betalingssystem simulert. I produksjon ville dette koble til Stripe for ekte betalinger.', 'success')
            return redirect(url_for('main.subscription_success', demo=True))
        
        # Log successful Stripe configuration (without exposing keys)
        current_app.logger.info(f"✅ Using Stripe key: {stripe_secret_key[:12]}...")
        
        # Set Stripe API key - only if needed (it should be set in on_register)
        if not hasattr(stripe, 'api_key') or not stripe.api_key:
            stripe.api_key = stripe_secret_key

        # Get price ID based on subscription type - with better fallbacks
        price_id = None
        mode = 'subscription'
        # Check cache first
        prices_cache = current_app.config.get('_STRIPE_PRICES_CACHE', {})
        
        if subscription_type == 'pro' or subscription_type == 'monthly':
            price_id = current_app.config.get('STRIPE_MONTHLY_PRICE_ID')
            # Fallback for development/demo - create a test price if none exists
            if not price_id and current_app.debug:
                price_id = 'price_test_monthly_demo'
        elif subscription_type == 'yearly':
            price_id = current_app.config.get('STRIPE_YEARLY_PRICE_ID')
            if not price_id and current_app.debug:
                price_id = 'price_test_yearly_demo'
        elif subscription_type == 'basic':
            # For backward compatibility - redirect basic to pro
            price_id = current_app.config.get('STRIPE_MONTHLY_PRICE_ID')
            if not price_id and current_app.debug:
                price_id = 'price_test_monthly_demo'
        elif subscription_type == 'lifetime':
            price_id = current_app.config.get('STRIPE_LIFETIME_PRICE_ID')
            if not price_id and current_app.debug:
                price_id = 'price_test_lifetime_demo'
            mode = 'payment'
        else:
            flash('Ugyldig abonnementstype.', 'danger')
            return redirect(url_for('main.subscription'))

        # Check if price_id was found and is not a dummy value
        if not price_id or (price_id.startswith('price_') and ('default_dev' in price_id or 'dummy' in price_id)):
            if current_app.debug:
                # In development, show a friendly message and redirect to demo
                current_app.logger.warning(f"No production price ID configured for {subscription_type} - showing demo mode")
                flash(f'Demo-modus: {subscription_type} abonnement er ikke konfigurert for produksjon. Kontakt administrator.', 'info')
                return redirect(url_for('demo.demo_page'))
            else:
                # In production, this is an error
                current_app.logger.error(f"No valid price ID configured for subscription type: {subscription_type}")
                flash(f'Abonnementstype {subscription_type} er ikke riktig konfigurert. Kontakt support.', 'danger')
                return redirect(url_for('main.subscription'))

        # Ekstra defensiv sjekk for innlogget bruker
        if not hasattr(current_user, 'id') or not hasattr(current_user, 'email'):
            flash('Brukerdata ikke tilgjengelig. Prøv å logg inn på nytt.', 'warning')
            return redirect(url_for('auth.login', next=url_for('main.subscription')))
            
        # Create or retrieve Stripe customer - with error handling
        try:
            if not getattr(current_user, 'stripe_customer_id', None):
                customer = stripe.Customer.create(
                    email=current_user.email,
                    metadata={'user_id': current_user.id},
                    name=f"{getattr(current_user, 'first_name', '')} {getattr(current_user, 'last_name', '')}".strip() or None
                )
                current_user.stripe_customer_id = customer.id
                db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to create/update Stripe customer: {str(e)}")
            flash('Kunne ikke opprette kundeprofil. Kontakt support.', 'danger')
            return redirect(url_for('main.subscription'))
            
        # Create checkout session with enhanced error handling
        try:
            # Validate price exists in Stripe before creating session
            if not price_id.startswith('price_test_'):  # Skip validation for test prices
                try:
                    price_obj = stripe.Price.retrieve(price_id)
                    # Check if price is active
                    if not price_obj.get('active', True):
                        current_app.logger.error(f"Stripe price is inactive: {price_id}")
                        flash('Den valgte abonnementstypen er ikke aktiv. Kontakt support for oppdaterte priser.', 'danger')
                        return redirect(url_for('main.subscription'))
                except stripe.error.InvalidRequestError as price_error:
                    if 'No such price' in str(price_error):
                        current_app.logger.error(f"Invalid Stripe price ID: {price_id}")
                        if current_app.debug:
                            flash(f'Demo-modus: Stripe price {price_id} er ikke gyldig. Kontakt administrator.', 'warning')
                            return redirect(url_for('demo.demo_page'))
                        else:
                            flash('Betalingskonfigurasjonen er ikke gyldig. Kontakt support.', 'danger')
                            return redirect(url_for('main.subscription'))
                    elif 'inactive' in str(price_error).lower():
                        current_app.logger.error(f"Stripe price is inactive: {price_id}")
                        flash('Den valgte abonnementstypen er ikke aktiv. Kontakt support for oppdaterte priser.', 'danger')
                        return redirect(url_for('main.subscription'))
                    else:
                        raise price_error
            
            checkout_params = {
                'customer': current_user.stripe_customer_id,
                'payment_method_types': ['card'],
                'line_items': [{
                    'price': price_id,
                    'quantity': 1
                }],
                'mode': mode,
                'success_url': request.host_url.rstrip('/') + url_for('stripe.payment_success') + '?session_id={CHECKOUT_SESSION_ID}',
                'cancel_url': request.host_url.rstrip('/') + url_for('main.subscription'),
                'metadata': {
                    'user_id': current_user.id,
                    'subscription_type': subscription_type
                },
                # Add locale support
                'locale': request.cookies.get('locale', 'auto'),
                # Add client reference for tracking
                'client_reference_id': str(current_user.id)
            }
            
            # Allow automatic tax calculation if enabled
            if current_app.config.get('STRIPE_AUTO_TAX_ENABLED'):
                checkout_params['automatic_tax'] = {'enabled': True}
                
            session = stripe.checkout.Session.create(**checkout_params)
            # Redirect directly to Stripe Checkout instead of returning JSON
            return redirect(session.url, code=303)
        except stripe.error.InvalidRequestError as e:
            if 'No such price' in str(e):
                current_app.logger.error(f"Stripe price not found: {price_id} - {str(e)}")
                flash('Den valgte abonnementstypen er ikke tilgjengelig. Kontakt support.', 'danger')
                return redirect(url_for('main.subscription'))
            elif 'inactive' in str(e).lower() or 'only accepts active prices' in str(e):
                current_app.logger.error(f"Stripe price is inactive: {price_id} - {str(e)}")
                flash('Den valgte abonnementstypen er ikke aktiv. Kontakt support for oppdaterte priser.', 'danger')
                return redirect(url_for('main.subscription'))
            else:
                current_app.logger.error(f"Stripe API error: {str(e)}")
                flash('Det oppstod en feil i betalingssystemet. Prøv igjen senere eller kontakt support.', 'danger')
                return redirect(url_for('main.subscription'))
        except stripe.error.StripeError as e:
            current_app.logger.error(f"Stripe API error: {str(e)}")
            return jsonify({'error': 'Det oppstod en feil i betalingssystemet. Prøv igjen senere eller kontakt support.'}), 500
        
    except Exception as e:
        current_app.logger.error(f'Failed to create checkout session: {str(e)}')
        return jsonify({'error': 'En uventet feil oppstod. Vennligst prøv igjen senere.'}), 500

@stripe_bp.route('/payment/success')
def payment_success():
    """Handle successful payment"""
    session_id = request.args.get('session_id')
    if not session_id:
        flash('Ingen betalingsinformasjon funnet', 'warning')
        return redirect(url_for('main.subscription'))
    
    if not current_user.is_authenticated:
        flash('Du må være innlogget for å se abonnementsinformasjon', 'warning')
        return redirect(url_for('auth.login', next=url_for('main.dashboard')))
    
    try:
        # Set Stripe API key if not already set
        if not hasattr(stripe, 'api_key') or not stripe.api_key:
            stripe_secret_key = current_app.config.get('STRIPE_SECRET_KEY')
            if not stripe_secret_key:
                flash('Betalingssystem er ikke riktig konfigurert', 'danger')
                return redirect(url_for('main.subscription'))
            stripe.api_key = stripe_secret_key
            
        # Retrieve Checkout session to confirm payment
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        # Verify that the session belongs to the current user
        session_user_id = checkout_session.metadata.get('user_id')
        if not session_user_id or int(session_user_id) != current_user.id:
            current_app.logger.warning(f"User {current_user.id} attempted to access session {session_id} belonging to user {session_user_id}")
            flash('Ugyldig betalingsinformasjon', 'danger')
            return redirect(url_for('main.subscription'))
        
        # Check payment status
        if checkout_session.payment_status != 'paid':
            if checkout_session.payment_status == 'unpaid':
                flash('Betalingen er ikke fullført ennå. Sjekk e-posten din for betalingsinstruksjoner.', 'warning')
            else:
                flash(f'Betalingsstatus: {checkout_session.payment_status}. Kontakt support hvis du har problemer.', 'warning')
            return redirect(url_for('main.subscription'))
        
        # Update user's subscription status based on subscription type
        subscription_type = checkout_session.metadata.get('subscription_type')
        now = datetime.utcnow()
        
        # Process different subscription types
        if subscription_type in ['monthly', 'pro', 'basic']:
            current_user.has_subscription = True
            current_user.subscription_type = 'monthly'
            current_user.subscription_start = now
            current_user.subscription_end = now + timedelta(days=31)  # Give an extra day to avoid timing issues
            current_user.has_trial = False  # Ensure trial is ended if they purchase
            
            # Log subscription details for audit
            current_app.logger.info(f"Monthly subscription activated for user {current_user.id}, valid until {current_user.subscription_end}")
            
        elif subscription_type == 'yearly':
            current_user.has_subscription = True
            current_user.subscription_type = 'yearly'
            current_user.subscription_start = now
            current_user.subscription_end = now + timedelta(days=366)  # Give an extra day to avoid timing issues
            current_user.has_trial = False  # Ensure trial is ended if they purchase
            
            # Log subscription details for audit
            current_app.logger.info(f"Yearly subscription activated for user {current_user.id}, valid until {current_user.subscription_end}")
            
        elif subscription_type == 'lifetime':
            current_user.has_subscription = True
            current_user.subscription_type = 'lifetime'
            current_user.subscription_start = now
            current_user.subscription_end = None
            current_user.has_trial = False  # Ensure trial is ended if they purchase
            
            # Log subscription details for audit
            current_app.logger.info(f"Lifetime subscription activated for user {current_user.id}")
        
        # Store additional info from Stripe if available
        if hasattr(current_user, 'last_payment_date'):
            current_user.last_payment_date = now
        if hasattr(current_user, 'last_payment_amount') and checkout_session.amount_total:
            current_user.last_payment_amount = checkout_session.amount_total / 100  # Convert from cents
            
        # Store payment method info if available
        try:
            payment_intent = stripe.PaymentIntent.retrieve(checkout_session.payment_intent)
            if payment_intent and payment_intent.charges and payment_intent.charges.data:
                charge = payment_intent.charges.data[0]
                if hasattr(current_user, 'payment_method'):
                    current_user.payment_method = charge.payment_method_details.type
                if hasattr(current_user, 'payment_method_last4') and charge.payment_method_details.card:
                    current_user.payment_method_last4 = charge.payment_method_details.card.last4
        except Exception as e:
            current_app.logger.warning(f"Could not retrieve payment details: {str(e)}")
        
        # Save all user changes
        db.session.commit()
        
        # Show success message and redirect to dashboard
        flash('Takk for kjøpet! Du har nå et aktivt abonnement.', 'success')
        return redirect(url_for('main.dashboard'))
        
    except stripe.error.StripeError as e:
        current_app.logger.error(f"Stripe API error in payment_success: {str(e)}")
        flash('Det oppstod et problem ved bekreftelse av betalingen. Kontakt support hvis abonnementet ikke er aktivert.', 'warning')
        return redirect(url_for('main.subscription'))
        
    except Exception as e:
        current_app.logger.error(f'Payment success processing error: {str(e)}')
        flash('Det oppstod en uventet feil. Kontakt support hvis abonnementet ikke er aktivert.', 'danger')
        return redirect(url_for('main.subscription'))

@stripe_bp.route('/success')
def success():
    """Simple success page for completed payments"""
    return render_template('stripe/success.html')

@stripe_bp.route('/cancel') 
def cancel():
    """Simple cancel page for cancelled payments"""
    return render_template('stripe/cancel.html')

@stripe_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events with improved error handling and logging"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
    
    # Validate webhook credentials
    if not webhook_secret:
        current_app.logger.error('⚠️ STRIPE_WEBHOOK_SECRET not found in environment variables')
        return jsonify({'error': 'Webhook not configured'}), 500
    
    # Check for dummy webhook secrets
    if webhook_secret.startswith('whsec_test') or webhook_secret == 'dummy_webhook_secret':
        current_app.logger.warning('⚠️ Using dummy webhook secret - Production webhooks will not work')
        return jsonify({'error': 'Demo webhook - not processing events'}), 200
    
    # Log webhook configuration (without exposing secret)
    current_app.logger.info(f"✅ Using webhook secret: {webhook_secret[:10]}...")
    
    # Attempt to parse and verify the webhook
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        current_app.logger.error(f'Invalid payload: {str(e)}')
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        current_app.logger.error(f'Invalid signature: {str(e)}')
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Log the event type for monitoring
    current_app.logger.info(f'Received Stripe webhook: {event.type} ({event.id})')
    
    # Handle specific event types
    try:
        if event.type == 'checkout.session.completed':
            handle_checkout_session(event.data.object)
            current_app.logger.info(f'Successfully processed checkout session: {event.data.object.id}')
            
        elif event.type == 'customer.subscription.updated':
            handle_subscription_update(event.data.object)
            current_app.logger.info(f'Successfully processed subscription update: {event.data.object.id}')
            
        elif event.type == 'customer.subscription.deleted':
            handle_subscription_deleted(event.data.object)
            current_app.logger.info(f'Successfully processed subscription deletion: {event.data.object.id}')
            
        elif event.type == 'invoice.payment_succeeded':
            handle_invoice_paid(event.data.object)
            current_app.logger.info(f'Successfully processed invoice payment: {event.data.object.id}')
            
        elif event.type == 'invoice.payment_failed':
            handle_invoice_failed(event.data.object)
            current_app.logger.info(f'Processed failed invoice payment: {event.data.object.id}')
            
        # Return success even for unhandled event types
        return jsonify({
            'status': 'success', 
            'message': f'Processed event: {event.type}',
            'event_id': event.id
        })
            
    except Exception as e:
        current_app.logger.error(f'Error handling webhook {event.type}: {str(e)}')
        # Log traceback for easier debugging
        import traceback
        current_app.logger.error(traceback.format_exc())
        
        # Return 200 to acknowledge receipt - we don't want Stripe to retry
        # (even though we had an error) to avoid processing duplicates
        return jsonify({
            'status': 'error', 
            'message': f'Error processing event: {event.type}',
            'event_id': event.id
        }), 200

def handle_checkout_session(session):
    """Handle completed checkout session"""
    user_id = int(session.metadata.get('user_id'))
    subscription_type = session.metadata.get('subscription_type')
    
    user = db.session.get(User, user_id)
    if not user:
        current_app.logger.error(f'User not found: {user_id}')
        return
    
    try:
        # Update user subscription
        user.has_subscription = True
        user.subscription_type = subscription_type
        user.subscription_start = datetime.utcnow()
        
        if subscription_type == 'monthly':
            user.subscription_end = datetime.utcnow() + timedelta(days=30)
        elif subscription_type == 'yearly':
            user.subscription_end = datetime.utcnow() + timedelta(days=365)
        elif subscription_type == 'lifetime':
            user.subscription_end = None
        
        db.session.commit()
        current_app.logger.info(f'Subscription activated for user {user_id}')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to update subscription for user {user_id}: {str(e)}')
        raise

def handle_subscription_update(subscription):
    """Handle subscription updates"""
    try:
        customer_id = subscription.customer
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if not user:
            current_app.logger.error(f'User not found for Stripe customer: {customer_id}')
            return
        
        # Update subscription status
        user.has_subscription = subscription.status == 'active'
        if subscription.status == 'active':
            if subscription.cancel_at:
                user.subscription_end = datetime.fromtimestamp(subscription.cancel_at)
            elif subscription.current_period_end:
                user.subscription_end = datetime.fromtimestamp(subscription.current_period_end)
        
        db.session.commit()
        current_app.logger.info(f'Subscription updated for user {user.id}')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to update subscription: {str(e)}')
        raise

def handle_invoice_paid(invoice):
    """Handle successful invoice payment"""
    try:
        # Get the customer associated with this invoice
        customer_id = invoice.customer
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if not user:
            current_app.logger.error(f'User not found for Stripe customer: {customer_id}')
            return
        
        # Update subscription details based on invoice
        if invoice.subscription:
            try:
                subscription = stripe.Subscription.retrieve(invoice.subscription)
                
                # Update user subscription end date based on billing cycle
                if subscription.current_period_end:
                    new_end_date = datetime.fromtimestamp(subscription.current_period_end)
                    user.subscription_end = new_end_date
                    
                    # Determine subscription type based on billing interval
                    if subscription.items and subscription.items.data:
                        interval = subscription.items.data[0].plan.interval
                        if interval == 'month':
                            user.subscription_type = 'monthly'
                        elif interval == 'year':
                            user.subscription_type = 'yearly'
                
                # Store last payment info if available
                if hasattr(user, 'last_payment_date'):
                    user.last_payment_date = datetime.utcnow()
                if hasattr(user, 'last_payment_amount'):
                    user.last_payment_amount = invoice.amount_paid / 100  # Convert from cents
                
                db.session.commit()
                current_app.logger.info(f'Updated subscription from invoice for user {user.id}, valid until {user.subscription_end}')
                
            except Exception as e:
                current_app.logger.error(f'Error retrieving subscription {invoice.subscription}: {str(e)}')
        
        # Handle one-time payments (not subscription-related)
        elif invoice.amount_paid > 0:
            current_app.logger.info(f'One-time payment of {invoice.amount_paid/100} processed for user {user.id}')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to process invoice payment: {str(e)}')
        raise

def handle_invoice_failed(invoice):
    """Handle failed invoice payment"""
    try:
        # Get the customer associated with this invoice
        customer_id = invoice.customer
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if not user:
            current_app.logger.error(f'User not found for Stripe customer: {customer_id}')
            return
        
        # Log the failed payment
        current_app.logger.warning(f'Payment failed for user {user.id}: invoice {invoice.id}, amount {invoice.amount_due/100}')
        
        # If this is the final attempt, mark the subscription as at risk
        if invoice.next_payment_attempt is None:
            current_app.logger.warning(f'Final payment attempt failed for user {user.id}, subscription at risk')
            
            # Optionally flag the account for follow-up
            if hasattr(user, 'payment_failed'):
                user.payment_failed = True
            
            # Store the date of the failed payment
            if hasattr(user, 'last_failed_payment'):
                user.last_failed_payment = datetime.utcnow()
            
            db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to process invoice failure: {str(e)}')
        raise

def handle_subscription_deleted(subscription):
    """Handle subscription deletion event from Stripe"""
    try:
        customer_id = subscription.customer
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        if not user:
            current_app.logger.error(f'User not found for Stripe customer: {customer_id}')
            return

        user.has_subscription = False
        user.subscription_end = datetime.utcnow()
        user.subscription_type = None

        db.session.commit()
        current_app.logger.info(f'Subscription deleted for user {user.id}')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to process subscription deletion: {str(e)}')
        raise