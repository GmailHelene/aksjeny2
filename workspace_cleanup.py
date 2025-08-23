#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

def cleanup_workspace_test_files():
    """Sletter alle testfiler i workspace systematisk"""
    
    print("🗑️ WORKSPACE TESTFIL CLEANUP STARTER")
    print("=" * 50)
    
    deleted_count = 0
    errors = []
    
    # Spesifikke testfiler som skal slettes
    test_files_to_delete = [
        # Python testfiler
        "test_*.py",
        "*test.py", 
        "*_test.py",
        
        # JSON testfiler
        "test_*.json",
        "*test.json",
        "*_test.json",
        "endpoint_test_results*.json",
        "production_test_results*.json",
        "navigation_test_results*.json",
        
        # HTML testfiler
        "test_*.html",
        "*test.html",
        "navigation-test.html",
        "style_test.html",
        "styling_test.html",
        
        # TXT og LOG testfiler
        "test_*.txt",
        "*test.txt", 
        "test_*.log",
        "*test.log",
        "endpoint_test_*.txt",
        
        # BAT og SH testfiler
        "test_*.bat",
        "*test.bat",
        "test_*.sh", 
        "*test.sh",
        "start_local_test.*",
        
        # Andre testfiler
        "test_user.json",
        "test_user_instance.json",
        "subscription_test.log",
        "auth_test.log"
    ]
    
    # Først slett direkte filer i root
    print("📁 Sletter testfiler i root directory...")
    for filename in os.listdir("."):
        if os.path.isfile(filename):
            should_delete = False
            
            # Sjekk om filen begynner med test
            if filename.startswith("test_") or filename.startswith("Test"):
                should_delete = True
            
            # Sjekk om filen slutter med test
            if filename.endswith("_test.py") or filename.endswith("test.py"):
                should_delete = True
                
            # Sjekk spesifikke testfiler
            if "test" in filename.lower() and (
                filename.endswith(".py") or 
                filename.endswith(".json") or 
                filename.endswith(".html") or 
                filename.endswith(".txt") or 
                filename.endswith(".log") or
                filename.endswith(".bat") or
                filename.endswith(".sh")
            ):
                should_delete = True
                
            if should_delete and filename != "cleanup_all_test_files.py":
                try:
                    print(f"  📄 Sletter: {filename}")
                    os.remove(filename)
                    deleted_count += 1
                except Exception as e:
                    error_msg = f"❌ Feil ved sletting av {filename}: {e}"
                    print(error_msg)
                    errors.append(error_msg)
    
    # Så slett testfiler i app/ directory
    if os.path.exists("app"):
        print("📁 Sletter testfiler i app/ directory...")
        for root, dirs, files in os.walk("app"):
            for filename in files:
                should_delete = False
                file_path = os.path.join(root, filename)
                
                # Samme logikk som over
                if filename.startswith("test_") or filename.startswith("Test"):
                    should_delete = True
                
                if filename.endswith("_test.py") or filename.endswith("test.py"):
                    should_delete = True
                    
                if "test" in filename.lower() and (
                    filename.endswith(".py") or 
                    filename.endswith(".json") or 
                    filename.endswith(".html") or 
                    filename.endswith(".txt") or 
                    filename.endswith(".log") or
                    filename.endswith(".bat") or
                    filename.endswith(".sh")
                ):
                    should_delete = True
                    
                if should_delete:
                    try:
                        print(f"  📄 Sletter: {file_path}")
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        error_msg = f"❌ Feil ved sletting av {file_path}: {e}"
                        print(error_msg)
                        errors.append(error_msg)
        
        # Slett tomme test directories
        if os.path.exists("app/tests") and not os.listdir("app/tests"):
            try:
                print("  📁 Sletter tom app/tests/ directory")
                os.rmdir("app/tests")
            except Exception as e:
                print(f"❌ Kunne ikke slette app/tests/: {e}")
    
    # Slett testfiler i static/ hvis de finnes
    if os.path.exists("static"):
        print("📁 Sletter testfiler i static/ directory...")
        for root, dirs, files in os.walk("static"):
            for filename in files:
                if "test" in filename.lower():
                    file_path = os.path.join(root, filename)
                    try:
                        print(f"  📄 Sletter: {file_path}")
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        error_msg = f"❌ Feil ved sletting av {file_path}: {e}"
                        print(error_msg)
                        errors.append(error_msg)
    
    print("\n" + "=" * 50)
    print(f"✅ WORKSPACE CLEANUP FERDIG!")
    print(f"📊 Slettet {deleted_count} testfiler totalt")
    
    if errors:
        print(f"⚠️ {len(errors)} filer kunne ikke slettes:")
        for error in errors[:5]:  # Vis max 5 feil
            print(f"   {error}")
            
    print("🎉 Workspace er nå ryddig og klar til bruk!")
    return deleted_count, errors

if __name__ == "__main__":
    cleanup_workspace_test_files()
