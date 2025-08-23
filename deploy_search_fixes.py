#!/usr/bin/env python3
"""
Deployment script for stock search and compare fixes
Commits and pushes changes to trigger Railway deployment
"""
import subprocess
import os
import time

def run_command(command, description):
    """Run a command and return success status"""
    try:
        print(f"🔄 {description}...")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def deploy_fixes():
    """Deploy the stock search and compare fixes"""
    print("🚀 DEPLOYING STOCK SEARCH AND COMPARE FIXES")
    print("=" * 60)
    
    commands = [
        ("git status", "Checking git status"),
        ("git add .", "Adding all changes"),
        ("git commit -m \"🔍 FIX: Stock search and compare access control issues\n\n- Fixed stocks/search access control (changed @access_required to @demo_access)\n- Fixed stocks/compare access control (removed from PREMIUM_ENDPOINTS, added to public_endpoints)\n- Removed conflicting route in main.py\n- Both pages now accessible without premium subscription\n- Tesla and other stock search data verified in fallback data\n\nResolves: Search functionality returning 'Ingen resultater funnet'\nResolves: Compare page redirecting to demo content\"", "Committing changes"),
        ("git push origin master", "Pushing to master branch for deployment")
    ]
    
    all_success = True
    
    for command, description in commands:
        success = run_command(command, description)
        if not success:
            all_success = False
            # Continue with remaining commands even if one fails
            
        time.sleep(1)  # Brief pause between commands
    
    if all_success:
        print("\n✅ DEPLOYMENT COMPLETE!")
        print("🔄 Railway should automatically deploy changes from master branch")
        print("⏱️  Deployment typically takes 2-3 minutes")
        print("🌐 Test live site after deployment completes")
    else:
        print("\n⚠️  DEPLOYMENT HAD ISSUES")
        print("📝 Check output above for specific errors")
        print("🔧 Manual intervention may be required")
    
    print("\n📋 POST-DEPLOYMENT CHECKLIST:")
    print("1. Wait 2-3 minutes for Railway deployment")
    print("2. Test https://aksjeradar.trade/stocks/search?q=tesla")
    print("3. Test https://aksjeradar.trade/stocks/compare")
    print("4. Verify pages show actual content (not demo promotional content)")
    print("5. Test search functionality with various queries")

if __name__ == "__main__":
    deploy_fixes()
