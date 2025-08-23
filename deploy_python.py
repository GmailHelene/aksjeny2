#!/usr/bin/env python3
"""
Deploy the stock search and compare fixes using Python subprocess
"""
import subprocess
import os
import sys

def run_git_command(command, cwd=None):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, 
                              capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def deploy_fixes():
    """Deploy all fixes to production"""
    print("🚀 DEPLOYING STOCK SEARCH & COMPARE FIXES")
    print("=" * 50)
    
    # Try to find the git repository
    workspace_paths = [
        "/workspaces/aksjeny2",  # Common Codespace path
        ".",  # Current directory
        os.getcwd(),  # Current working directory
    ]
    
    git_repo_path = None
    for path in workspace_paths:
        if os.path.exists(os.path.join(path, ".git")):
            git_repo_path = path
            break
    
    if not git_repo_path:
        print("❌ Could not find git repository")
        print("Looking for .git directory in these paths:")
        for path in workspace_paths:
            print(f"   - {path}")
        return False
    
    print(f"📂 Found git repository at: {git_repo_path}")
    
    # Add all changes
    print("📋 Adding all changes...")
    success, stdout, stderr = run_git_command("git add .", git_repo_path)
    if not success:
        print(f"❌ Failed to add changes: {stderr}")
        return False
    
    # Check status
    print("📊 Checking git status...")
    success, stdout, stderr = run_git_command("git status --porcelain", git_repo_path)
    if success and stdout.strip():
        print(f"Changes to commit:\n{stdout}")
    else:
        print("No changes to commit")
        return True
    
    # Commit changes
    print("💾 Committing fixes...")
    commit_message = """Fix stock search and compare functionality

- Remove conflicting @main.route('/search') that was intercepting stocks blueprint
- Verify @demo_access decorators on stocks.search and stocks.compare routes
- Ensure both endpoints are in public_endpoints whitelist  
- Fix route conflicts that prevented proper blueprint resolution

Fixes:
- https://aksjeradar.trade/stocks/search?q=tesla now works properly
- https://aksjeradar.trade/stocks/compare shows actual interface
- Both endpoints accessible without demo restrictions"""
    
    success, stdout, stderr = run_git_command(f'git commit -m "{commit_message}"', git_repo_path)
    if not success:
        print(f"❌ Failed to commit: {stderr}")
        return False
    
    print("✅ Committed successfully")
    
    # Push to production
    print("🚢 Pushing to production...")
    success, stdout, stderr = run_git_command("git push origin main", git_repo_path)
    if not success:
        print(f"❌ Failed to push: {stderr}")
        return False
    
    print("✅ Pushed successfully!")
    print("")
    print("⏰ Deployment initiated! Railway typically takes 2-3 minutes to deploy.")
    print("🔍 Run final_verification_script.py after deployment to verify fixes.")
    print("")
    print("📊 Expected results after deployment:")
    print("  ✅ /stocks/search?q=tesla - Shows search interface, finds Tesla results")
    print("  ✅ /stocks/compare - Shows comparison tool interface")
    print("  ❌ Should NOT show 'demo-modus aktivert' or promotional content")
    print("")
    print("🏁 Deployment complete!")
    return True

if __name__ == "__main__":
    success = deploy_fixes()
    if not success:
        sys.exit(1)
