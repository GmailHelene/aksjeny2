#!/usr/bin/env python3
"""
Mock Data Detection Script - Find potential mock/demo data for paying users
Searches the entire codebase for demo/mock data patterns
"""

import os
import re
import json
from datetime import datetime

def search_for_mock_data():
    """Search for potential mock data across the entire codebase"""
    
    print("🔍 MOCK DATA DETECTION REPORT")
    print("=" * 60)
    print(f"Scan started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Patterns to search for that might indicate mock/demo data
    mock_patterns = [
        (r'mock|fake|dummy|sample|test[_\s]data', 'Mock/Demo Data References'),
        (r'demo[_\s]?(user|account|data|mode)', 'Demo User/Account References'),
        (r'placeholder|lorem|ipsum', 'Placeholder Content'),
        (r'999999|9999999|123456|test@|example\.com', 'Test/Example Values'),
        (r'current_user\.is_demo', 'Demo User Checks'),
        (r'is_demo_user|demo_only', 'Demo User Functions'),
        (r'subscription.*demo|demo.*subscription', 'Demo Subscription Logic'),
        (r'free[_\s]?tier|trial[_\s]?mode', 'Free/Trial Mode References')
    ]
    
    # File extensions to search
    file_extensions = ['.py', '.html', '.js', '.css', '.json', '.md']
    
    # Directories to exclude
    exclude_dirs = {'__pycache__', '.git', 'node_modules', 'venv', '.pytest_cache'}
    
    results = {}
    total_files_scanned = 0
    total_matches = 0
    
    # Walk through all files
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                total_files_scanned += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    file_matches = []
                    
                    # Search for each pattern
                    for pattern, description in mock_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                        
                        for match in matches:
                            # Get line number
                            line_num = content[:match.start()].count('\\n') + 1
                            
                            # Get context (surrounding lines)
                            lines = content.split('\\n')
                            context_start = max(0, line_num - 2)
                            context_end = min(len(lines), line_num + 2)
                            context = lines[context_start:context_end]
                            
                            file_matches.append({
                                'pattern': description,
                                'match': match.group(),
                                'line': line_num,
                                'context': context
                            })
                            total_matches += 1
                    
                    if file_matches:
                        results[file_path] = file_matches
                        
                except Exception as e:
                    print(f"⚠️  Error reading {file_path}: {e}")
    
    # Report results
    print(f"📊 SCAN SUMMARY")
    print(f"Files scanned: {total_files_scanned}")
    print(f"Total potential issues found: {total_matches}")
    print(f"Files with issues: {len(results)}")
    print()
    
    if results:
        print("🚨 POTENTIAL MOCK DATA ISSUES")
        print("-" * 40)
        
        # Group by pattern type
        pattern_counts = {}
        for file_path, matches in results.items():
            for match in matches:
                pattern = match['pattern']
                if pattern not in pattern_counts:
                    pattern_counts[pattern] = 0
                pattern_counts[pattern] += 1
        
        print("Issues by category:")
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {pattern}: {count} occurrences")
        print()
        
        # Detailed findings
        critical_files = []
        for file_path, matches in results.items():
            print(f"📁 {file_path}")
            
            # Check if this is a critical file (routes, models, core logic)
            is_critical = any(keyword in file_path.lower() for keyword in ['route', 'model', 'view', 'controller', 'auth'])
            
            if is_critical:
                critical_files.append(file_path)
                print("   🔥 CRITICAL FILE")
            
            for match in matches:
                print(f"   • Line {match['line']}: {match['pattern']}")
                print(f"     Match: '{match['match']}'")
                
                # Show context if it's a critical match
                if is_critical or 'demo' in match['match'].lower():
                    print(f"     Context:")
                    for i, line in enumerate(match['context']):
                        line_num = match['line'] - len(match['context'])//2 + i
                        marker = ">>>" if line_num == match['line'] else "   "
                        print(f"     {marker} {line_num:3d}: {line[:80]}")
                print()
            print()
        
        # Critical recommendations
        if critical_files:
            print("🎯 CRITICAL RECOMMENDATIONS")
            print("-" * 30)
            print("The following files contain potential mock data and need review:")
            for file_path in critical_files:
                print(f"   • {file_path}")
            print()
            print("For paying users, ensure these files use real data only!")
        
    else:
        print("✅ No obvious mock data patterns detected!")
        print("   This is good - the codebase appears clean of demo data.")
    
    print()
    
    # Save detailed results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f'mock_data_scan_{timestamp}.json'
    
    scan_summary = {
        "timestamp": datetime.now().isoformat(),
        "files_scanned": total_files_scanned,
        "total_matches": total_matches,
        "files_with_issues": len(results),
        "pattern_counts": pattern_counts if results else {},
        "detailed_results": results
    }
    
    with open(results_file, 'w') as f:
        json.dump(scan_summary, f, indent=2)
    
    print(f"📁 Detailed scan results saved to: {results_file}")
    
    return {
        "clean": len(results) == 0,
        "critical_files": len([f for f in results.keys() if any(k in f.lower() for k in ['route', 'model', 'view'])]),
        "total_issues": total_matches
    }

if __name__ == "__main__":
    results = search_for_mock_data()
    
    if results["clean"]:
        print("\\n🎉 Codebase is clean of obvious mock data!")
        exit(0)
    elif results["critical_files"] > 0:
        print(f"\\n❌ Found {results['critical_files']} critical files with potential mock data!")
        exit(1)
    else:
        print(f"\\n⚠️  Found {results['total_issues']} non-critical mock data references")
        exit(2)
