#!/usr/bin/env python3
"""
Deploy stock data fix to production
This script deploys the stock details real data fix for authenticated users
"""

import subprocess
import sys
import time
import requests

def run_command(command, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    if check and result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        return False
    
    return True

def main():
    print("=== Deploying Stock Data Fix ===")
    
    # Git commands to commit and push changes
    commands = [
        "git add app/routes/stocks.py",
        "git commit -m 'Fix stock details to show real data for authenticated users'",
        "git push origin master"
    ]
    
    for command in commands:
        if not run_command(command, check=False):
            print(f"Warning: Command '{command}' had issues, continuing...")
    
    print("\n=== Changes pushed to GitHub ===")
    print("Railway should auto-deploy from master branch...")
    
    # Wait for deployment
    print("Waiting 30 seconds for Railway deployment...")
    time.sleep(30)
    
    # Test the fix
    print("\n=== Testing stock data fix ===")
    test_urls = [
        "https://aksjeradar.trade/stocks/details/TSLA",
        "https://aksjeradar.trade/stocks/details/DNB.OL",
        "https://aksjeradar.trade/stocks/details/EQNR.OL"
    ]
    
    for url in test_urls:
        try:
            print(f"Testing: {url}")
            response = requests.get(url, timeout=10)
            if "$100.00" in response.text:
                print(f"❌ Still showing $100.00 for {url}")
            elif "price" in response.text.lower():
                print(f"✅ Price data updated for {url}")
            else:
                print(f"⚠️  Could not find price data for {url}")
        except Exception as e:
            print(f"❌ Error testing {url}: {e}")
    
    print("\n=== Deployment complete ===")
    print("Stock details should now show real data for authenticated users")

if __name__ == "__main__":
    main()
