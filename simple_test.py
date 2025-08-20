import requests
import sys

print("Testing Flask app...")

try:
    response = requests.get("http://localhost:5000/", timeout=10)
    print(f"Homepage status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.text
        if 'ROI Kalkulator' not in content:
            print("✅ ROI Calculator removed from navigation")
        else:
            print("❌ ROI Calculator still in navigation")
            
        if 'Beregn ROI' in content:
            print("✅ ROI Calculator promotion found")
        else:
            print("❌ ROI Calculator promotion missing")
    
except Exception as e:
    print(f"Error: {e}")

print("Test complete!")
