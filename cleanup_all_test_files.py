#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import time

def cleanup_test_files():
    """Sletter alle testfiler i workspace"""
    
    print("🗑️ SLETTER ALLE TESTFILER I APPEN")
    print("=" * 50)
    
    # Finn alle filer som begynner med "test"
    test_patterns = [
        "test*",
        "test_*",
        "*test.py",
        "*test.html", 
        "*test.txt",
        "*test.json",
        "*test.log",
        "*test.md",
        "*test.bat",
        "*test.sh"
    ]
    
    deleted_count = 0
    errors = []
    
    try:
        # Søk etter testfiler i current directory
        for pattern in test_patterns:
            files = glob.glob(pattern)
            for file_path in files:
                if os.path.isfile(file_path):
                    try:
                        print(f"📄 Sletter: {file_path}")
                        os.remove(file_path)
                        deleted_count += 1
                        time.sleep(0.1)  # Kort pause
                    except Exception as e:
                        error_msg = f"❌ Kunne ikke slette {file_path}: {e}"
                        print(error_msg)
                        errors.append(error_msg)
                        
        # Søk i undermapper
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.startswith("test") and not file.endswith("cleanup_all_test_files.py"):
                    file_path = os.path.join(root, file)
                    try:
                        print(f"📄 Sletter: {file_path}")
                        os.remove(file_path)
                        deleted_count += 1
                        time.sleep(0.1)
                    except Exception as e:
                        error_msg = f"❌ Kunne ikke slette {file_path}: {e}"
                        print(error_msg)
                        errors.append(error_msg)
                        
    except Exception as e:
        print(f"❌ Generell feil: {e}")
    
    print("\n" + "=" * 50)
    print(f"✅ Slettet {deleted_count} testfiler!")
    
    if errors:
        print(f"⚠️ {len(errors)} filer kunne ikke slettes:")
        for error in errors[:10]:  # Vis max 10 feil
            print(f"   {error}")
            
    print("🎉 Workspace opprydding ferdig!")
    return deleted_count, errors

if __name__ == "__main__":
    cleanup_test_files()
