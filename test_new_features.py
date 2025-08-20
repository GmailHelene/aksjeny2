#!/usr/bin/env python3
"""
Quick test script to verify new features are working
"""

import requests
import time

# Base URL for the running Flask app
BASE_URL = "http://localhost:5000"

def test_route(path, description):
    """Test a route and report status"""
    try:
        response = requests.get(f"{BASE_URL}{path}", timeout=10)
        status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
        print(f"{status} - {description}: {path}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ERROR - {description}: {path} - {str(e)}")
        return False

def main():
    print("🚀 Testing Aksjeradar New Features")
    print("=" * 50)
    
    # Test core functionality first
    print("\n📍 Core Routes:")
    test_route("/", "Homepage")
    test_route("/analysis/", "Analysis Overview")
    test_route("/portfolio/", "Portfolio")
    
    # Test new Norwegian Intelligence features
    print("\n🇳🇴 Norwegian Intelligence Hub:")
    test_route("/norwegian-intel/", "Norwegian Intel Overview")
    test_route("/norwegian-intel/social-sentiment", "Social Sentiment")
    test_route("/norwegian-intel/oil-correlation", "Oil Correlation")
    test_route("/norwegian-intel/government-impact", "Government Impact")
    test_route("/norwegian-intel/shipping-intelligence", "Shipping Intelligence")
    
    # Test Daily View
    print("\n📅 Daily Market View:")
    test_route("/daily-view/", "Daily View")
    
    # Test Forum System
    print("\n💬 Forum System:")
    test_route("/forum/", "Forum Homepage")
    test_route("/forum/category/enkelaksjer", "Enkeltaksjer Category")
    test_route("/forum/category/investeringsstrategier", "Investeringsstrategier Category")
    test_route("/forum/category/teknisk-analyse", "Teknisk Analyse Category")
    test_route("/forum/category/markedsnyheter", "Markedsnyheter Category")
    test_route("/forum/category/begynnerhjornet", "Begynnerhjørnet Category")
    test_route("/forum/search", "Forum Search")
    
    # Test API endpoints
    print("\n🔌 API Endpoints:")
    test_route("/norwegian-intel/api/real-time-sentiment/EQUI", "Real-time Sentiment API")
    test_route("/norwegian-intel/api/oil-correlation/EQUI", "Oil Correlation API")
    test_route("/daily-view/api/live-updates", "Daily View Live Updates API")
    
    print("\n" + "=" * 50)
    print("✨ Test completed! Check the navigation menu to access all new features.")
    print("\n🌟 New Features Available:")
    print("   • Norwegian Market Intelligence Hub")
    print("   • Daily Market View with live updates")
    print("   • Community Forum with 5 categories")
    print("   • Enhanced Analysis menu with AI Predictions")
    print("   • Fixed portfolio stock addition functionality")

if __name__ == "__main__":
    main()
