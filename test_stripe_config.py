#!/usr/bin/env python3
"""
Test script to verify Stripe production configuration
Run this to test Stripe integration without starting the full Flask app
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_stripe_config():
    """Test Stripe configuration"""
    print("🧪 Testing Stripe Production Configuration...")
    print()
    
    # Import configuration
    try:
        from config import Config
        config = Config()
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    # Check Stripe keys
    stripe_keys = {
        'STRIPE_PUBLISHABLE_KEY': config.STRIPE_PUBLISHABLE_KEY,
        'STRIPE_SECRET_KEY': config.STRIPE_SECRET_KEY,
        'STRIPE_WEBHOOK_SECRET': config.STRIPE_WEBHOOK_SECRET,
        'STRIPE_MONTHLY_PRICE_ID': config.STRIPE_MONTHLY_PRICE_ID,
        'STRIPE_YEARLY_PRICE_ID': config.STRIPE_YEARLY_PRICE_ID,
        'STRIPE_LIFETIME_PRICE_ID': config.STRIPE_LIFETIME_PRICE_ID,
    }
    
    print("📋 Stripe Configuration:")
    all_configured = True
    
    for key, value in stripe_keys.items():
        if value:
            # Show only first 12 characters for security
            display_value = f"{value[:12]}..." if len(value) > 12 else value
            print(f"✅ {key}: {display_value}")
        else:
            print(f"❌ {key}: NOT SET")
            all_configured = False
    
    print()
    
    if all_configured:
        print("✅ All Stripe configuration keys are set!")
    else:
        print("⚠️  Some Stripe keys are missing")
        return False
    
    # Test Stripe import and basic functionality
    try:
        import stripe
        stripe.api_key = config.STRIPE_SECRET_KEY
        print("✅ Stripe module imported successfully")
        
        # Test basic API call (don't create anything, just test connection)
        try:
            # Just verify the key format - don't make actual API calls in test
            if stripe.api_key.startswith('sk_live_'):
                print("✅ Using live Stripe key (production mode)")
            elif stripe.api_key.startswith('sk_test_'):
                print("⚠️  Using test Stripe key (test mode)")
            else:
                print("❌ Invalid Stripe key format")
                return False
                
        except Exception as e:
            print(f"⚠️  Stripe API test skipped: {e}")
            
    except ImportError:
        print("❌ Stripe module not available")
        return False
    except Exception as e:
        print(f"❌ Stripe setup failed: {e}")
        return False
    
    print()
    print("🎉 Stripe configuration test completed successfully!")
    print("� Remember to set these environment variables on Railway:")
    print("   - Use the Railway dashboard or CLI to set production variables")
    print("   - Redeploy after setting variables")
    
    return True

if __name__ == '__main__':
    success = test_stripe_config()
    sys.exit(0 if success else 1)
