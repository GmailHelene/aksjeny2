#!/usr/bin/env python3
"""
Comprehensive Sentiment Analysis Route Test
"""

import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def comprehensive_sentiment_test():
    """Comprehensive test of sentiment analysis functionality"""
    base_url = "http://localhost:5002"
    
    tests = [
        {
            'name': 'Base Sentiment Page',
            'url': f'{base_url}/analysis/sentiment',
            'method': 'GET'
        },
        {
            'name': 'Sentiment View Page',
            'url': f'{base_url}/analysis/sentiment-view',
            'method': 'GET'
        },
        {
            'name': 'Oslo Stock Sentiment (EQNR.OL)',
            'url': f'{base_url}/analysis/sentiment?symbol=EQNR.OL',
            'method': 'GET'
        },
        {
            'name': 'US Stock Sentiment (AAPL)',
            'url': f'{base_url}/analysis/sentiment?symbol=AAPL',
            'method': 'GET'
        },
        {
            'name': 'Norwegian Stock (DNB.OL)',
            'url': f'{base_url}/analysis/sentiment?symbol=DNB.OL',
            'method': 'GET'
        },
        {
            'name': 'Invalid Symbol Test',
            'url': f'{base_url}/analysis/sentiment?symbol=INVALID123!!!',
            'method': 'GET'
        },
        {
            'name': 'Empty Symbol Test',
            'url': f'{base_url}/analysis/sentiment?symbol=',
            'method': 'GET'
        }
    ]
    
    results = {'passed': 0, 'failed': 0, 'total': len(tests)}
    
    for test in tests:
        logger.info(f"🧪 Running: {test['name']}")
        
        try:
            response = requests.get(test['url'])
            
            # Check response
            if response.status_code == 200:
                logger.info(f"✅ {test['name']}: SUCCESS")
                
                # Verify content
                content = response.text.lower()
                checks = [
                    'sentiment' in content,
                    'analyse' in content or 'analysis' in content,
                ]
                
                if all(checks):
                    logger.info("   ✅ Content verification passed")
                    results['passed'] += 1
                else:
                    logger.warning("   ⚠️ Content verification failed")
                    results['failed'] += 1
                    
            elif response.status_code == 302:
                # Redirect is acceptable for invalid symbols
                logger.info(f"✅ {test['name']}: REDIRECT (acceptable for invalid input)")
                results['passed'] += 1
                
            else:
                logger.error(f"❌ {test['name']}: HTTP {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            logger.error(f"❌ {test['name']}: ERROR - {e}")
            results['failed'] += 1
        
        time.sleep(0.5)  # Brief pause between tests
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("🏁 SENTIMENT ANALYSIS TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"Total Tests: {results['total']}")
    logger.info(f"✅ Passed: {results['passed']}")
    logger.info(f"❌ Failed: {results['failed']}")
    logger.info(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['failed'] == 0:
        logger.info("🎉 ALL TESTS PASSED! Sentiment analysis is working correctly!")
        return True
    else:
        logger.warning(f"⚠️ {results['failed']} tests failed.")
        return False

if __name__ == "__main__":
    success = comprehensive_sentiment_test()
    exit(0 if success else 1)
