#!/usr/bin/env python3
"""
KOMPLETT LOKAL TESTING SUITE
Tester all hovedfunksjonalitet lokalt uten å vente på deployment
"""

import sys
import os
import subprocess
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class LocalTester:
    def __init__(self):
        self.base_url = "http://localhost:5555"
        self.server_process = None
        
    def start_local_server(self):
        """Start the local test server"""
        print("🚀 Starter lokal test server...")
        try:
            # Start server in background
            self.server_process = subprocess.Popen([
                sys.executable, 'local_test_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(3)
            
            # Test if server is running
            try:
                response = requests.get(f"{self.base_url}/", timeout=5)
                if response.status_code == 200:
                    print("✅ Server startet successfully!")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            print("❌ Server failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Feil ved start av server: {e}")
            return False
    
    def stop_local_server(self):
        """Stop the local test server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("🛑 Server stoppet")
    
    def test_stocks_search(self):
        """Test stocks search functionality"""
        print("\n🔍 TESTER AKSJESØK...")
        print("-" * 30)
        
        test_cases = [
            {"query": "tesla", "expected": "TSLA"},
            {"query": "apple", "expected": "AAPL"},
            {"query": "microsoft", "expected": "MSFT"},
            {"query": "", "expected": "no_results"}
        ]
        
        results = []
        
        for test in test_cases:
            try:
                if test["query"]:
                    url = f"{self.base_url}/stocks/search?q={test['query']}"
                else:
                    url = f"{self.base_url}/stocks/search"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    if test["expected"] == "no_results":
                        if "ingen resultater" in content or "no results" in content or not test["query"]:
                            result = "✅ PASS"
                        else:
                            result = "❌ FAIL"
                    else:
                        if test["expected"].lower() in content:
                            result = "✅ PASS"
                        else:
                            result = "❌ FAIL"
                else:
                    result = f"❌ HTTP {response.status_code}"
                
                print(f"  Query: '{test['query']}' -> {result}")
                results.append({
                    'test': f"search_{test['query'] or 'empty'}",
                    'passed': result.startswith('✅'),
                    'query': test['query'],
                    'expected': test['expected']
                })
                
            except Exception as e:
                print(f"  Query: '{test['query']}' -> ❌ ERROR: {e}")
                results.append({
                    'test': f"search_{test['query'] or 'empty'}",
                    'passed': False,
                    'error': str(e)
                })
        
        return results
    
    def test_stocks_compare(self):
        """Test stocks compare functionality"""
        print("\n📊 TESTER AKSJESAMMENLIGNING...")
        print("-" * 30)
        
        test_cases = [
            {"symbols": "", "expected": "default_compare"},
            {"symbols": "TSLA,AAPL", "expected": ["tsla", "aapl"]},
            {"symbols": "EQNR.OL,DNB.OL", "expected": ["eqnr", "dnb"]}
        ]
        
        results = []
        
        for test in test_cases:
            try:
                if test["symbols"]:
                    url = f"{self.base_url}/stocks/compare?symbols={test['symbols']}"
                else:
                    url = f"{self.base_url}/stocks/compare"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    if test["expected"] == "default_compare":
                        if "sammenligning" in content or "compare" in content:
                            result = "✅ PASS"
                        else:
                            result = "❌ FAIL"
                    else:
                        # Check if expected symbols are in content
                        found_symbols = all(symbol in content for symbol in test["expected"])
                        if found_symbols:
                            result = "✅ PASS"
                        else:
                            result = "❌ FAIL"
                else:
                    result = f"❌ HTTP {response.status_code}"
                
                symbols_str = test["symbols"] or "default"
                print(f"  Symbols: '{symbols_str}' -> {result}")
                results.append({
                    'test': f"compare_{symbols_str}",
                    'passed': result.startswith('✅'),
                    'symbols': test['symbols'],
                    'expected': test['expected']
                })
                
            except Exception as e:
                symbols_str = test["symbols"] or "default"
                print(f"  Symbols: '{symbols_str}' -> ❌ ERROR: {e}")
                results.append({
                    'test': f"compare_{symbols_str}",
                    'passed': False,
                    'error': str(e)
                })
        
        return results
    
    def test_main_issues(self):
        """Test the main issues you mentioned"""
        print("\n🎯 TESTER HOVEDPROBLEMER...")
        print("-" * 30)
        
        # Test 1: Tesla search should work
        print("  Test 1: Tesla søk skal fungere...")
        try:
            response = requests.get(f"{self.base_url}/stocks/search?q=tesla", timeout=10)
            if response.status_code == 200 and "tesla" in response.text.lower():
                print("    ✅ Tesla søk fungerer!")
                tesla_result = True
            else:
                print("    ❌ Tesla søk fungerer ikke")
                tesla_result = False
        except Exception as e:
            print(f"    ❌ Tesla søk feil: {e}")
            tesla_result = False
        
        # Test 2: Compare page should show actual interface
        print("  Test 2: Sammenligning skal vise riktig grensesnitt...")
        try:
            response = requests.get(f"{self.base_url}/stocks/compare", timeout=10)
            if response.status_code == 200 and "sammenligning" in response.text.lower():
                print("    ✅ Sammenligning fungerer!")
                compare_result = True
            else:
                print("    ❌ Sammenligning fungerer ikke")
                compare_result = False
        except Exception as e:
            print(f"    ❌ Sammenligning feil: {e}")
            compare_result = False
        
        # Test 3: No demo content should be shown
        print("  Test 3: Ingen demo-innhold skal vises...")
        try:
            response = requests.get(f"{self.base_url}/stocks/search?q=tesla", timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                has_demo = "demo-modus aktivert" in content or "prøv alle aksjeradar funksjoner" in content
                if not has_demo:
                    print("    ✅ Ingen demo-innhold!")
                    demo_result = True
                else:
                    print("    ❌ Demo-innhold vises fortsatt")
                    demo_result = False
            else:
                demo_result = False
        except Exception as e:
            print(f"    ❌ Demo test feil: {e}")
            demo_result = False
        
        return {
            'tesla_search': tesla_result,
            'compare_page': compare_result,
            'no_demo_content': demo_result
        }
    
    def generate_test_report(self, search_results, compare_results, main_issues):
        """Generate comprehensive test report"""
        print("\n📊 TESTRAPPORT")
        print("=" * 50)
        
        # Count passed tests
        search_passed = sum(1 for r in search_results if r.get('passed', False))
        compare_passed = sum(1 for r in compare_results if r.get('passed', False))
        main_passed = sum(1 for v in main_issues.values() if v)
        
        total_tests = len(search_results) + len(compare_results) + len(main_issues)
        total_passed = search_passed + compare_passed + main_passed
        
        print(f"📈 SAMMENDRAG:")
        print(f"  Søk tester: {search_passed}/{len(search_results)} bestått")
        print(f"  Sammenligning tester: {compare_passed}/{len(compare_results)} bestått") 
        print(f"  Hovedproblemer: {main_passed}/{len(main_issues)} løst")
        print(f"  TOTALT: {total_passed}/{total_tests} tester bestått")
        
        if total_passed == total_tests:
            print(f"\n🎉 ALLE TESTER BESTÅTT! ({total_passed}/{total_tests})")
            print("✅ Alle endringer fungerer lokalt!")
        elif total_passed > total_tests * 0.8:
            print(f"\n😊 MEST BESTÅTT! ({total_passed}/{total_tests})")
            print("⚠️ Noen mindre problemer gjenstår")
        else:
            print(f"\n😞 NOE FUNGERER IKKE ({total_passed}/{total_tests})")
            print("❌ Flere problemer må fikses")
        
        # Save detailed report
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total_tests,
                'total_passed': total_passed,
                'success_rate': (total_passed / total_tests) * 100
            },
            'search_tests': search_results,
            'compare_tests': compare_results,
            'main_issues': main_issues
        }
        
        with open('local_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Detaljert rapport lagret i: local_test_report.json")
        
        return report
    
    def run_full_test_suite(self):
        """Run the complete test suite"""
        print("🧪 KJØRER KOMPLETT TESTING SUITE")
        print("=" * 60)
        
        # Start server
        if not self.start_local_server():
            print("❌ Kunne ikke starte server. Avslutter.")
            return
        
        try:
            # Run all tests
            search_results = self.test_stocks_search()
            compare_results = self.test_stocks_compare() 
            main_issues = self.test_main_issues()
            
            # Generate report
            report = self.generate_test_report(search_results, compare_results, main_issues)
            
            # Show next steps
            print(f"\n🎯 NESTE STEG:")
            print(f"1. Åpne http://localhost:5555 i nettleseren")
            print(f"2. Test funksjonaliteten manuelt")
            print(f"3. Gjør endringer i koden")
            print(f"4. Restart serveren for å se endringer")
            print(f"5. Kjør denne testen på nytt: python local_testing_suite.py")
            
            return report
            
        finally:
            # Always stop server
            self.stop_local_server()

def main():
    """Main function"""
    print("🏠 LOKAL TESTING SUITE FOR AKSJERADAR")
    print("Tester alle endringer lokalt uten å vente på deployment!")
    print("=" * 60)
    
    tester = LocalTester()
    
    try:
        report = tester.run_full_test_suite()
        return report
    except KeyboardInterrupt:
        print("\n👋 Testing avbrutt av bruker")
        tester.stop_local_server()
    except Exception as e:
        print(f"\n❌ Uventet feil: {e}")
        tester.stop_local_server()

if __name__ == '__main__':
    main()
