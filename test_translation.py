#!/usr/bin/env python3
"""
Test script to verify translation system functionality
"""

def test_translation_functions():
    """Test the translation functions we added"""
    try:
        # Import the translation functions
        from app.utils.translation import get_free_translation_js, get_language_toggle_html
        
        print("Testing translation system...")
        
        # Test JavaScript generation
        js_code = get_free_translation_js()
        print(f"JavaScript code generated: {len(js_code)} characters")
        assert 'function translatePage' in js_code
        assert 'TRANSLATION_DICTIONARY' in js_code
        print("✓ JavaScript translation code generated successfully")
        
        # Test HTML toggle generation
        html_code = get_language_toggle_html()
        print(f"HTML code generated: {len(html_code)} characters")
        assert 'language-toggle' in html_code
        assert 'btn btn-outline-light' in html_code
        print("✓ Language toggle HTML generated successfully")
        
        print("\n✅ All translation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_includes():
    """Test that analysis menu includes work"""
    try:
        # Check if the menu template file exists
        import os
        menu_path = 'app/templates/analysis/_menu.html'
        
        if os.path.exists(menu_path):
            print("✓ Analysis menu template found")
            with open(menu_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'btn-primary' in content
                assert 'btn-outline-primary' in content
                print("✓ Analysis menu contains expected Bootstrap classes")
        else:
            print("❌ Analysis menu template not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Translation System Test ===\n")
    
    translation_ok = test_translation_functions()
    template_ok = test_template_includes()
    
    if translation_ok and template_ok:
        print("\n🎉 All tests passed! Translation system is ready.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
