#!/bin/bash

# Script to set production Stripe environment variables on Railway
# Replace the dummy values with your actual Stripe production keys and price IDs

echo "Setting production Stripe environment variables on Railway..."

# IMPORTANT: Replace these with your actual Stripe production values
# You can find these in your Stripe Dashboard at https://dashboard.stripe.com/

# Stripe API Keys (Production)
STRIPE_SECRET_KEY="sk_live_your_production_secret_key_here"
STRIPE_PUBLIC_KEY="pk_live_your_production_public_key_here"

# Stripe Price IDs for your subscription products
# Create these in Stripe Dashboard > Products
STRIPE_MONTHLY_PRICE_ID="price_your_monthly_subscription_price_id"
STRIPE_YEARLY_PRICE_ID="price_your_yearly_subscription_price_id"

# Webhook secret (if using webhooks)
STRIPE_WEBHOOK_SECRET="whsec_your_webhook_secret_here"

echo "🔧 To set these environment variables on Railway, run the following commands:"
echo ""
echo "railway variables set STRIPE_SECRET_KEY=\"$STRIPE_SECRET_KEY\""
echo "railway variables set STRIPE_PUBLIC_KEY=\"$STRIPE_PUBLIC_KEY\""
echo "railway variables set STRIPE_MONTHLY_PRICE_ID=\"$STRIPE_MONTHLY_PRICE_ID\""
echo "railway variables set STRIPE_YEARLY_PRICE_ID=\"$STRIPE_YEARLY_PRICE_ID\""
echo "railway variables set STRIPE_WEBHOOK_SECRET=\"$STRIPE_WEBHOOK_SECRET\""
echo ""
echo "📝 Or set them in Railway Dashboard > Your Project > Variables tab"
echo ""
echo "🚨 SECURITY NOTE: Replace the dummy values above with your actual Stripe keys"
echo "   Never commit real Stripe keys to version control!"
echo ""
echo "📚 To get your Stripe keys:"
echo "   1. Go to https://dashboard.stripe.com/"
echo "   2. Navigate to Developers > API keys"
echo "   3. Copy your Publishable key and Secret key"
echo "   4. Create products and prices in Products section"
echo "   5. Copy the price IDs for monthly and yearly subscriptions"
