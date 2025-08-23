#!/usr/bin/env python3
"""
ULTIMATE TESTFIL CLEANUP - Sletter ALLE testfiler fra workspace
"""
import os
import shutil

def main():
    print("🗑️ ULTIMATE TESTFIL CLEANUP STARTER")
    print("=" * 60)
    
    deleted_count = 0
    
    # Slett alle filer i root som begynner med test_
    print("🔍 Søker etter testfiler i root directory...")
    
    try:
        all_files = os.listdir(".")
        test_files = [f for f in all_files if f.startswith("test_") or f.startswith("Test")]
        
        for filename in test_files:
            if os.path.isfile(filename):
                try:
                    os.remove(filename)
                    print(f"  ✅ Slettet: {filename}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ Feil: {filename} - {e}")
                    
        # Slett andre test-relaterte filer
        other_test_files = [
            "auth_test.log",
            "subscription_test.log", 
            "test_user.json",
            "test_user_instance.json",
            "contrast_test.html",
            "style_test.html",
            "styling_test.html",
            "navigation-test.html",
            "endpoint_test_output.txt",
            "endpoint_test_report.json",
            "endpoint_test_results.json"
        ]
        
        for filename in other_test_files:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    print(f"  ✅ Slettet: {filename}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ Feil: {filename} - {e}")
        
        # Slett JSON testfiler med timestamp
        json_files = [f for f in all_files if "test_results" in f and f.endswith(".json")]
        for filename in json_files:
            try:
                os.remove(filename)
                print(f"  ✅ Slettet: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"  ❌ Feil: {filename} - {e}")
                
    except Exception as e:
        print(f"❌ Feil ved listing av root directory: {e}")
    
    print(f"\n🎯 FERDIG! Slettet {deleted_count} testfiler fra workspace!")
    print("🎉 Workspace er nå ryddig!")
    
    return deleted_count

if __name__ == "__main__":
    main()
