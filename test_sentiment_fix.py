#!/usr/bin/env python3
"""
Test script to verify sentiment analysis route works correctly
"""

import os
import sys
import requests
from app import create_app
from flask import Flask, request

def test_sentiment_direct():
    """Test sentiment function directly"""
    try:
        app = create_app('development')
        
        with app.test_client() as client:
            # Test without login first to see what happens
            response = client.get('/analysis/sentiment?symbol=AFG.OL')
            print(f"✅ Status Code: {response.status_code}")
            print(f"✅ Response type: {type(response.data)}")
            print(f"✅ Response length: {len(response.data)} bytes")
            
            # Check if response contains error message
            response_text = response.data.decode('utf-8')
            if 'teknisk feil under analyse' in response_text.lower():
                print("❌ Found 'teknisk feil under analyse' in response")
                return False
            elif 'sentiment' in response_text.lower():
                print("✅ Response contains sentiment content")
                return True
            else:
                print(f"⚠️  Unexpected response content (first 200 chars): {response_text[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing sentiment route: {e}")
        return False

def test_sentiment_with_login():
    """Test sentiment function with proper login"""
    try:
        app = create_app('development')
        
        with app.test_client() as client:
            # Create test session 
            with client.session_transaction() as session:
                session['user_id'] = 1
                session['logged_in'] = True
                
            response = client.get('/analysis/sentiment?symbol=AFG.OL')
            print(f"\n🔐 With Login - Status Code: {response.status_code}")
            
            response_text = response.data.decode('utf-8')
            if 'teknisk feil under analyse' in response_text.lower():
                print("❌ Still getting 'teknisk feil under analyse' with login")
                return False
            elif 'sentiment' in response_text.lower():
                print("✅ Response contains sentiment content with login")
                return True
            else:
                print(f"⚠️  Unexpected response with login (first 200 chars): {response_text[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing sentiment route with login: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Testing sentiment analysis route...")
    
    success1 = test_sentiment_direct()
    success2 = test_sentiment_with_login()
    
    if success1 or success2:
        print("\n✅ Sentiment route appears to be working!")
    else:
        print("\n❌ Sentiment route has issues that need fixing")
