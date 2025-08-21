#!/usr/bin/env python3
"""
Test script to verify that the BuildError for analysis.analysis has been fixed

This script tests:
1. analysis.index route works properly  
2. analysis.analysis route no longer exists
3. Templates render without BuildError 
4. Navigation links work correctly
"""

import sys
import os
import logging

# Add the app directory to sys.path
app_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, app_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_app_creation():
    """Test that the Flask app can be created without errors"""
    logger.info("Testing app creation...")
    
    try:
        # Import create_app
        from app import create_app
        
        # Create app instance  
        app = create_app('development')
        
        logger.info("✅ App created successfully")
        return app
        
    except Exception as e:
        logger.error(f"❌ Error creating app: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        return None

def test_url_generation(app):
    """Test URL generation for analysis routes"""
    logger.info("Testing URL generation...")
    
    if not app:
        logger.error("❌ No app available for testing")
        return False
        
    with app.app_context():
        from flask import url_for
        
        # Test analysis.index (should work)
        try:
            url = url_for('analysis.index')
            logger.info(f"✅ analysis.index URL built successfully: {url}")
        except Exception as e:
            logger.error(f"❌ Failed to build analysis.index URL: {e}")
            return False
            
        # Test analysis.currency_overview (should work)
        try:
            url = url_for('analysis.currency_overview')
            logger.info(f"✅ analysis.currency_overview URL built successfully: {url}")
        except Exception as e:
            logger.error(f"❌ Failed to build analysis.currency_overview URL: {e}")
            return False
            
        # Test the old analysis.analysis route (should fail)
        try:
            url = url_for('analysis.analysis')
            logger.error(f"❌ ERROR: analysis.analysis should not exist but got: {url}")
            return False
        except Exception as e:
            logger.info(f"✅ analysis.analysis correctly fails as expected: {type(e).__name__}")
            
    return True

def test_template_rendering(app):
    """Test that templates render without BuildError"""
    logger.info("Testing template rendering...")
    
    if not app:
        logger.error("❌ No app available for testing")
        return False
        
    try:
        from flask import render_template
        
        # Test with app context and request context (needed for url_for)
        with app.test_request_context():
            # This will fail if there are any BuildErrors in base.html or navigation
            rendered = render_template('analysis/index.html')
            logger.info("✅ Template rendering successful - no BuildError in navigation")
            
            # Check if the rendered content contains the correct navigation
            if 'analysis/index' in rendered or '/analysis/' in rendered:
                logger.info("✅ Navigation contains correct analysis route")
            else:
                logger.warning("⚠️ Could not verify correct navigation route in rendered content")
                
    except Exception as e:
        logger.error(f"❌ Template rendering failed: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        return False
        
    return True

def check_base_template():
    """Check base.html template for correct URL references"""
    logger.info("Checking base.html template...")
    
    template_path = 'app/templates/base.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check that analysis.index is used (correct)
        if 'analysis.index' in content:
            logger.info("✅ base.html correctly uses 'analysis.index'")
        else:
            logger.error("❌ base.html does not contain 'analysis.index'")
            return False
            
        # Check that analysis.analysis is NOT used (incorrect)
        if 'analysis.analysis' in content:
            logger.error("❌ base.html still contains 'analysis.analysis' - fix not applied!")
            return False
        else:
            logger.info("✅ base.html correctly does NOT contain 'analysis.analysis'")
            
    except Exception as e:
        logger.error(f"❌ Error reading {template_path}: {e}")
        return False
        
    return True

def main():
    """Run all tests"""
    logger.info("🔍 Starting BuildError fix verification tests...")
    logger.info("=" * 50)
    
    # Test 1: Check base template
    if not check_base_template():
        logger.error("❌ Base template check failed!")
        sys.exit(1)
        
    # Test 2: Create app
    app = test_app_creation()
    if not app:
        logger.error("❌ App creation failed!")
        sys.exit(1)
        
    # Test 3: URL generation
    if not test_url_generation(app):
        logger.error("❌ URL generation tests failed!")
        sys.exit(1)
        
    # Test 4: Template rendering
    if not test_template_rendering(app):
        logger.error("❌ Template rendering tests failed!")
        sys.exit(1)
        
    logger.info("=" * 50)
    logger.info("🎉 ALL TESTS PASSED!")
    logger.info("✅ BuildError has been successfully fixed!")
    logger.info("✅ Navigation now correctly uses 'analysis.index' instead of 'analysis.analysis'")
    logger.info("✅ Website should now work without navigation errors")

if __name__ == '__main__':
    main()
                logger.info("✅ Template syntax check passed")
                return True
                
            except Exception as e:
                logger.error(f"❌ Template rendering error: {e}")
                return False
                
    except ImportError as e:
        logger.error(f"❌ Flask import error: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting BuildError fix verification...")
    
    tests = [
        ("Route Definition", test_route_exists),
        ("Template Syntax", test_template_syntax),
        ("No BuildErrors", test_no_more_builderrors)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running {test_name} test...")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                logger.info(f"✅ {test_name} test PASSED")
            else:
                logger.error(f"❌ {test_name} test FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} test CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 BuildError fix verification SUCCESSFUL!")
        logger.info("\n" + "="*60)
        logger.info("ISSUE RESOLUTION SUMMARY")
        logger.info("="*60)
        logger.info("✅ Fixed template references to non-existent route")
        logger.info("✅ Simplified crypto_dashboard function to avoid import errors")
        logger.info("✅ All url_for() calls now reference working endpoints")
        logger.info("✅ BuildError should no longer occur on user login")
        logger.info("="*60)
        return True
    else:
        logger.error(f"💥 {total - passed} tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
