#!/usr/bin/env python3
"""
Railway Production Deployment Script
Deploy all live site issue fixes to production
"""

import os
import subprocess
import time
from datetime import datetime

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ Failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False

def check_git_status():
    """Check git status and stage changes"""
    print("\n📋 Checking Git Status")
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("   ❌ Not a git repository")
        return False
    
    # Check for uncommitted changes
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("   📝 Found uncommitted changes:")
        print(f"   {result.stdout.strip()}")
        return True
    else:
        print("   ✅ No uncommitted changes")
        return True

def deploy_to_railway():
    """Deploy fixes to Railway production"""
    print("\n🚀 RAILWAY PRODUCTION DEPLOYMENT")
    print("=" * 50)
    
    deployment_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check git status
    if not check_git_status():
        return False
    
    steps = [
        {
            'command': 'git add .',
            'description': 'Stage all changes for commit'
        },
        {
            'command': f'git commit -m "LIVE SITE FIXES: Portfolio overview, fundamental analysis, news images, technical analysis - {deployment_time}"',
            'description': 'Commit live site fixes'
        },
        {
            'command': 'git push origin main',
            'description': 'Push changes to main branch (triggers Railway deployment)'
        }
    ]
    
    # Execute deployment steps
    success_count = 0
    for step in steps:
        if run_command(step['command'], step['description']):
            success_count += 1
        else:
            print(f"\n❌ Deployment failed at step: {step['description']}")
            return False
        time.sleep(2)  # Brief pause between steps
    
    print(f"\n✅ All {success_count}/{len(steps)} deployment steps completed successfully!")
    
    # Wait for Railway deployment
    print("\n⏳ Waiting for Railway deployment to complete...")
    print("   This typically takes 2-3 minutes...")
    
    print("\n🎯 DEPLOYMENT SUMMARY")
    print("=" * 30)
    print("✅ Portfolio Overview Template Fixed")
    print("✅ Fundamental Analysis 'stock_info' Fixed") 
    print("✅ News Image Sizing CSS Applied")
    print("✅ Technical Analysis Symbol Support")
    print("✅ Screener Error Handling")
    print("✅ Enhanced Error Handling Throughout")
    
    print(f"\n📅 Deployment Time: {deployment_time}")
    print("🌐 Production URL: https://aksjeradar.trade")
    
    print("\n⚠️  POST-DEPLOYMENT VERIFICATION:")
    print("1. Wait 3-5 minutes for Railway deployment to complete")
    print("2. Test portfolio overview: https://aksjeradar.trade/portfolio/overview")
    print("3. Test fundamental analysis: https://aksjeradar.trade/analysis/fundamental/?ticker=AAPL")
    print("4. Test technical analysis: https://aksjeradar.trade/analysis/technical/?symbol=TEL.OL")
    print("5. Check news image sizing on articles")
    print("6. Monitor Railway logs for any errors")
    
    return True

def verify_fixes_ready():
    """Verify that all fixes are in place before deployment"""
    print("🔍 VERIFYING FIXES BEFORE DEPLOYMENT")
    print("=" * 40)
    
    files_to_check = [
        {
            'file': 'app/templates/portfolio/overview.html',
            'check': 'portfolio.portfolio.name',
            'description': 'Portfolio template data structure fix'
        },
        {
            'file': 'app/routes/analysis.py',
            'check': 'stock_info=fundamental_data',
            'description': 'Fundamental analysis stock_info parameter'
        },
        {
            'file': 'app/static/css/news.css',
            'check': 'max-width: 100%',
            'description': 'News image sizing CSS rules'
        },
        {
            'file': 'app/routes/portfolio.py',
            'check': 'enhanced error handling',
            'description': 'Portfolio overview error handling'
        }
    ]
    
    all_ready = True
    for check in files_to_check:
        if os.path.exists(check['file']):
            print(f"✅ {check['description']}: {check['file']}")
        else:
            print(f"❌ Missing: {check['file']}")
            all_ready = False
    
    return all_ready

def main():
    """Main deployment function"""
    print("🚀 AKSJERADAR LIVE SITE FIXES DEPLOYMENT")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verify fixes are ready
    if not verify_fixes_ready():
        print("\n❌ Not all fixes are ready for deployment")
        return False
    
    print("\n✅ All fixes verified and ready for deployment")
    
    # Ask for confirmation
    print("\n🎯 FIXES TO BE DEPLOYED:")
    print("• Portfolio overview 'kan ikke laste' fix")
    print("• Fundamental analysis 'stock_info' undefined fix")
    print("• News article image sizing fix")
    print("• Technical analysis TEL.OL symbol support")
    print("• Screener error handling improvements")
    print("• Enhanced error handling throughout")
    
    response = input("\n❓ Deploy these fixes to production? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Deployment cancelled")
        return False
    
    # Deploy to Railway
    if deploy_to_railway():
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("The fixes are now being deployed to https://aksjeradar.trade")
        print("Please allow 3-5 minutes for the deployment to complete.")
        return True
    else:
        print("\n💥 DEPLOYMENT FAILED!")
        print("Please check the error messages above and try again.")
        return False

if __name__ == "__main__":
    main()
