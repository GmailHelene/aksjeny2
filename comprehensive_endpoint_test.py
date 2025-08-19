#!/usr/bin/env python3
"""
Comprehensive endpoint testing for Aksjeradar
Tests all routes for errors, missing data, and content issues
"""
import requests
import json
import time
import sys
from urllib.parse import urljoin
import threading
from datetime import datetime

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class EndpointTester:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {
            'passed': [],
            'failed': [],
            'errors': [],
            'warnings': []
        }
        
        # Login first to access protected routes
        self.authenticated = False
        self.setup_session()

    def setup_session(self):
        """Setup session with authentication if possible"""
        try:
            # Try to get demo access first
            response = self.session.get(f"{self.base_url}/demo")
            if response.status_code == 200:
                self.authenticated = True
                print(f"{Color.GREEN}✅ Demo access established{Color.END}")
        except:
            print(f"{Color.YELLOW}⚠️  Demo access not available, testing public routes only{Color.END}")
    
    def test_endpoint(self, path, expected_status=200, method='GET', data=None, description=None):
        """Test a single endpoint"""
        url = urljoin(self.base_url, path)
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, data=data, timeout=10)
            else:
                return self.record_error(path, f"Unsupported method: {method}")
            
            # Check status code
            if response.status_code == expected_status:
                self.record_pass(path, response, description)
            elif response.status_code == 302:
                # Check if redirect is to login (unauthorized)
                if 'login' in response.headers.get('Location', ''):
                    self.record_warning(path, f"Redirects to login (unauthorized access)")
                else:
                    self.record_pass(path, response, f"Redirects to: {response.headers.get('Location', 'unknown')}")
            elif response.status_code == 404:
                self.record_error(path, "404 Not Found")
            elif response.status_code == 500:
                self.record_error(path, f"500 Internal Server Error: {response.text[:200]}")
            else:
                self.record_warning(path, f"Unexpected status: {response.status_code}")
            
            return response
            
        except requests.exceptions.ConnectionError:
            self.record_error(path, "Connection refused - server not running?")
        except requests.exceptions.Timeout:
            self.record_error(path, "Request timeout")
        except Exception as e:
            self.record_error(path, f"Exception: {str(e)}")
    
    def record_pass(self, path, response, description=None):
        content_length = len(response.content)
        desc = description or f"Status {response.status_code}"
        self.results['passed'].append({
            'path': path,
            'status': response.status_code,
            'content_length': content_length,
            'description': desc
        })
        print(f"{Color.GREEN}✅ {path:50} - {desc} ({content_length:,} bytes){Color.END}")
    
    def record_warning(self, path, message):
        self.results['warnings'].append({'path': path, 'message': message})
        print(f"{Color.YELLOW}⚠️  {path:50} - {message}{Color.END}")
    
    def record_error(self, path, message):
        self.results['errors'].append({'path': path, 'message': message})
        print(f"{Color.RED}❌ {path:50} - {message}{Color.END}")
    
    def check_content_quality(self, path, response):
        """Check for content quality issues"""
        content = response.text.lower()
        issues = []
        
        # Check for common error indicators
        if 'error' in content and 'traceback' in content:
            issues.append("Contains error traceback")
        if 'n/a' in content and content.count('n/a') > 10:
            issues.append(f"Too many N/A values ({content.count('n/a')})")
        if len(response.text) < 500:
            issues.append("Very short content (< 500 chars)")
        if 'lorem ipsum' in content:
            issues.append("Contains placeholder text")
        if response.text.count('undefined') > 0:
            issues.append("Contains 'undefined' values")
        
        return issues
    
    def test_all_routes(self):
        """Test all known routes"""
        print(f"\n{Color.BOLD}🧪 COMPREHENSIVE ENDPOINT TESTING{Color.END}")
        print("=" * 80)
        
        # Core routes
        core_routes = [
            '/',
            '/demo',
            '/index',
            '/health',
            '/health/ready',
            '/health/detailed',
        ]
        
        # Main functionality routes
        main_routes = [
            '/login',
            '/register',
            '/logout',
            '/profile',
            '/settings',
            '/search',
            '/pricing',
            '/pricing/pricing',
            '/pricing/subscription',
        ]
        
        # Stock routes
        stock_routes = [
            '/stocks',
            '/stocks/list',
            '/stocks/list/oslo',
            '/stocks/list/global',
            '/stocks/list/crypto',
            '/stocks/list/currency',
            '/stocks/compare',
            '/stocks/details/AAPL',
            '/stocks/details/DNB.OL',
        ]
        
        # Analysis routes
        analysis_routes = [
            '/analysis',
            '/analysis/technical',
            '/analysis/fundamental',
            '/analysis/ai',
            '/analysis/screener',
            '/analysis/screener-view',
            '/analysis/recommendation',
            '/analysis/prediction',
            '/analysis/market-overview',
            '/analysis/currency-overview',
            '/analysis/oslo-overview',
            '/analysis/global-overview',
        ]
        
        # Portfolio routes
        portfolio_routes = [
            '/portfolio',
            '/portfolio/watchlist',
            '/portfolio/tips',
            '/portfolio/create',
            '/portfolio/transactions',
            '/portfolio/advanced',
            '/portfolio-analytics',
        ]
        
        # News routes
        news_routes = [
            '/news',
            '/news/latest',
            '/news/company/AAPL',
        ]
        
        # Features routes
        features_routes = [
            '/features/ai-predictions',
            '/features/social-sentiment',
            '/features/analyst-recommendations',
        ]
        
        # API routes
        api_routes = [
            '/api/health',
            '/api/stocks/quick-prices?tickers=AAPL,GOOGL',
            '/api/homepage/market-data',
            '/api/realtime/market-summary',
        ]
        
        # Investment guides
        investment_routes = [
            '/investment-guides',
            '/investment-guides/index',
        ]
        
        # Notifications
        notification_routes = [
            '/notifications',
            '/notifications/settings',
        ]
        
        # Advanced features
        advanced_routes = [
            '/advanced-analytics',
            '/financial-dashboard',
            '/mobile-trading',
        ]
        
        # Combine all routes
        all_routes = (core_routes + main_routes + stock_routes + 
                     analysis_routes + portfolio_routes + news_routes + 
                     features_routes + api_routes + investment_routes + 
                     notification_routes + advanced_routes)
        
        print(f"\n{Color.BLUE}Testing {len(all_routes)} endpoints...{Color.END}\n")
        
        # Test each route
        for route in all_routes:
            self.test_endpoint(route)
            time.sleep(0.1)  # Small delay to avoid overwhelming server
    
    def print_summary(self):
        """Print test summary"""
        total = len(self.results['passed']) + len(self.results['warnings']) + len(self.results['errors'])
        
        print(f"\n{Color.BOLD}📊 TEST SUMMARY{Color.END}")
        print("=" * 80)
        print(f"{Color.GREEN}✅ Passed: {len(self.results['passed'])}{Color.END}")
        print(f"{Color.YELLOW}⚠️  Warnings: {len(self.results['warnings'])}{Color.END}")
        print(f"{Color.RED}❌ Errors: {len(self.results['errors'])}{Color.END}")
        print(f"📈 Success Rate: {(len(self.results['passed'])/total*100):.1f}%")
        
        if self.results['errors']:
            print(f"\n{Color.RED}{Color.BOLD}🚨 CRITICAL ERRORS:{Color.END}")
            for error in self.results['errors']:
                print(f"   {error['path']}: {error['message']}")
        
        if self.results['warnings']:
            print(f"\n{Color.YELLOW}{Color.BOLD}⚠️  WARNINGS:{Color.END}")
            for warning in self.results['warnings']:
                print(f"   {warning['path']}: {warning['message']}")
        
        # Save detailed results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'endpoint_test_results_{timestamp}.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n📁 Detailed results saved to: endpoint_test_results_{timestamp}.json")

def main():
    """Main testing function"""
    print(f"{Color.BOLD}🎯 AKSJERADAR ENDPOINT TESTING{Color.END}")
    print("Testing all endpoints for errors, missing data, and content issues\n")
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        print(f"{Color.GREEN}✅ Server is running (Status: {response.status_code}){Color.END}")
    except:
        print(f"{Color.RED}❌ Server is not running on localhost:5001{Color.END}")
        print("Please start the server with: python3 main.py")
        return
    
    # Run tests
    tester = EndpointTester()
    tester.test_all_routes()
    tester.print_summary()

if __name__ == "__main__":
    main()
