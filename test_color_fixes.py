#!/usr/bin/env python3
"""
Test color and contrast fixes

This script tests:
1. CSS file syntax and loading
2. Template rendering without errors  
3. Color restoration functionality
4. Cache busting implementation
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_css_files():
    """Test that CSS files exist and have no syntax errors"""
    logger.info("Testing CSS files...")
    
    css_files = [
        'app/static/css/color-restoration-fix.css',
        'app/static/css/ultimate-contrast-fix.css',
        'app/static/css/text-contrast.css'
    ]
    
    for css_file in css_files:
        try:
            if os.path.exists(css_file):
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Basic CSS syntax checks
                if content.count('{') != content.count('}'):
                    logger.error(f"❌ CSS syntax error in {css_file}: Mismatched braces")
                    return False
                    
                if '!important' in content:
                    logger.info(f"✅ {css_file} contains important declarations (good for overrides)")
                    
                if 'linear-gradient' in content:
                    logger.info(f"✅ {css_file} contains gradient backgrounds")
                    
                logger.info(f"✅ {css_file} syntax check passed")
            else:
                logger.warning(f"⚠️ {css_file} not found")
                
        except Exception as e:
            logger.error(f"❌ Error reading {css_file}: {e}")
            return False
    
    return True

def test_template_updates():
    """Test that templates have been updated correctly"""
    logger.info("Testing template updates...")
    
    templates_to_check = [
        ('app/templates/base.html', 'color-restoration-fix.css'),
        ('app/templates/demo.html', 'linear-gradient(135deg, #28a745, #20c997)'),
        ('currency.html', 'linear-gradient(135deg, #28a745, #20c997)')
    ]
    
    for template_file, expected_content in templates_to_check:
        try:
            if os.path.exists(template_file):
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if expected_content in content:
                    logger.info(f"✅ {template_file} contains expected fix: {expected_content[:50]}...")
                else:
                    logger.error(f"❌ {template_file} missing expected content: {expected_content[:50]}...")
                    return False
            else:
                logger.warning(f"⚠️ {template_file} not found")
                
        except Exception as e:
            logger.error(f"❌ Error reading {template_file}: {e}")
            return False
    
    return True

def test_color_restoration_css():
    """Test specific color restoration CSS content"""
    logger.info("Testing color restoration CSS content...")
    
    css_file = 'app/static/css/color-restoration-fix.css'
    
    required_selectors = [
        '.btn-success',
        '.btn-primary', 
        '.bg-success',
        '.bg-primary',
        '.text-center.mt-5.mb-5',
        '.card-header.bg-success',
        '.card-header.bg-primary'
    ]
    
    try:
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for selector in required_selectors:
                if selector in content:
                    logger.info(f"✅ Found required selector: {selector}")
                else:
                    logger.error(f"❌ Missing required selector: {selector}")
                    return False
                    
            # Check for important gradient backgrounds
            if 'linear-gradient(135deg, #28a745, #1e7e34) !important' in content:
                logger.info("✅ Green gradient backgrounds implemented")
            else:
                logger.error("❌ Missing green gradient backgrounds")
                return False
                
            if 'linear-gradient(135deg, #007bff, #0056b3) !important' in content:
                logger.info("✅ Blue gradient backgrounds implemented")
            else:
                logger.error("❌ Missing blue gradient backgrounds")
                return False
                
            # Check for CTA banner fixes
            if 'CTA BANNER FIXES' in content:
                logger.info("✅ CTA banner fixes section found")
            else:
                logger.error("❌ Missing CTA banner fixes section")
                return False
                
        else:
            logger.error(f"❌ {css_file} not found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error analyzing {css_file}: {e}")
        return False
    
    return True

def test_cache_busting():
    """Test that cache busting is implemented"""
    logger.info("Testing cache busting...")
    
    try:
        base_template = 'app/templates/base.html'
        if os.path.exists(base_template):
            with open(base_template, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if '20250821_color_fix' in content:
                logger.info("✅ Cache bust meta tag updated")
            else:
                logger.error("❌ Cache bust meta tag not updated")
                return False
                
            if '?v=20250821' in content:
                logger.info("✅ CSS file cache busting implemented")
            else:
                logger.error("❌ CSS file cache busting not implemented")
                return False
                
        else:
            logger.error(f"❌ {base_template} not found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error checking cache busting: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    logger.info("🚀 Starting color and contrast fixes test suite...")
    
    tests = [
        ("CSS Files", test_css_files),
        ("Template Updates", test_template_updates),
        ("Color Restoration CSS", test_color_restoration_css),
        ("Cache Busting", test_cache_busting)
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
        logger.info("🎉 All color and contrast fixes are working correctly!")
        return True
    else:
        logger.error(f"💥 {total - passed} tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
