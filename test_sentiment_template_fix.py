#!/usr/bin/env python3
"""
Test to verify sentiment analysis template fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import Flask

def test_sentiment_template_fix():
    """Test that sentiment template now works without errors"""
    try:
        app = create_app('development')
        
        with app.test_client() as client:
            # Test with login simulation
            with client.session_transaction() as session:
                session['user_id'] = 1
                session['logged_in'] = True
                
            # Test the sentiment endpoint
            response = client.get('/analysis/sentiment?symbol=AFG.OL')
            print(f"✅ Status Code: {response.status_code}")
            
            response_text = response.data.decode('utf-8')
            
            # Check for error patterns
            if 'teknisk feil under analyse' in response_text.lower():
                print("❌ Still getting 'teknisk feil under analyse'")
                print(f"Response excerpt: {response_text[:500]}")
                return False
            elif 'error' in response_text.lower() and '500' in response_text:
                print("❌ Getting 500 error")
                print(f"Response excerpt: {response_text[:500]}")
                return False
            elif 'sentiment' in response_text.lower() and 'analyser sentiment' in response_text.lower():
                print("✅ Sentiment page loaded successfully!")
                print("✅ Template fix appears to work")
                return True
            else:
                print("⚠️  Unexpected response")
                print(f"Response excerpt: {response_text[:500]}")
                return False
                
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🧪 Testing sentiment template fix...")
    success = test_sentiment_template_fix()
    if success:
        print("\n✅ Sentiment analysis fix successful!")
        print("✅ Item 19 in critical error list should now be resolved!")
    else:
        print("\n❌ Sentiment analysis still has issues")
