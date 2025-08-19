#!/usr/bin/env python3
"""
Comprehensive Warren Buffett Analysis Route Test
"""

import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def comprehensive_warren_buffett_test():
    """Comprehensive test of Warren Buffett analysis functionality"""
    base_url = "http://localhost:5002"
    
    tests = [
        {
            'name': 'Base Page Load',
            'url': f'{base_url}/analysis/warren-buffett',
            'method': 'GET'
        },
        {
            'name': 'Oslo Stock Analysis (EQNR.OL)',
            'url': f'{base_url}/analysis/warren-buffett?ticker=EQNR.OL',
            'method': 'GET'
        },
        {
            'name': 'US Stock Analysis (AAPL)',
            'url': f'{base_url}/analysis/warren-buffett?ticker=AAPL',
            'method': 'GET'
        },
        {
            'name': 'POST Form Submission',
            'url': f'{base_url}/analysis/warren-buffett',
            'method': 'POST',
            'data': {'ticker': 'MSFT'}
        },
        {
            'name': 'Invalid Ticker Test',
            'url': f'{base_url}/analysis/warren-buffett',
            'method': 'POST',
            'data': {'ticker': 'INVALID123'}
        },
        {
            'name': 'Empty Ticker Test',
            'url': f'{base_url}/analysis/warren-buffett',
            'method': 'POST',
            'data': {'ticker': ''}
        }
    ]
    
    results = {'passed': 0, 'failed': 0, 'total': len(tests)}
    
    for test in tests:
        logger.info(f"🧪 Running: {test['name']}")
        
        try:
            if test['method'] == 'GET':
                response = requests.get(test['url'])
            else:
                response = requests.post(test['url'], data=test.get('data', {}))
            
            # Check response
            if response.status_code == 200:
                logger.info(f"✅ {test['name']}: SUCCESS")
                
                # Verify content
                content = response.text.lower()
                checks = [
                    'warren buffett' in content,
                    'analyse' in content or 'analysis' in content,
                    'buffett' in content
                ]
                
                if all(checks):
                    logger.info("   ✅ Content verification passed")
                    results['passed'] += 1
                else:
                    logger.warning("   ⚠️ Content verification failed")
                    results['failed'] += 1
                    
            else:
                logger.error(f"❌ {test['name']}: HTTP {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            logger.error(f"❌ {test['name']}: ERROR - {e}")
            results['failed'] += 1
        
        time.sleep(0.5)  # Brief pause between tests
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("🏁 WARREN BUFFETT ANALYSIS TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"Total Tests: {results['total']}")
    logger.info(f"✅ Passed: {results['passed']}")
    logger.info(f"❌ Failed: {results['failed']}")
    logger.info(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['failed'] == 0:
        logger.info("🎉 ALL TESTS PASSED! Warren Buffett analysis is working correctly!")
        return True
    else:
        logger.warning(f"⚠️ {results['failed']} tests failed.")
        return False

if __name__ == "__main__":
    success = comprehensive_warren_buffett_test()
    exit(0 if success else 1)
