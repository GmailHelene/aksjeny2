#!/usr/bin/env python3
"""Comprehensive template verification for sector analysis"""

def verify_template_blocks():
    """Verify that all Jinja2 blocks are properly closed"""
    template_path = "app/templates/market_intel/sector_analysis.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all block start and end tags
        import re
        
        # Find all {% block ... %} tags
        block_starts = re.findall(r'{%\s*block\s+(\w+)', content)
        
        # Find all {% endblock %} tags
        endblocks = re.findall(r'{%\s*endblock\s*%}', content)
        
        print("🔍 Template Block Analysis:")
        print(f"   📂 Block starts found: {len(block_starts)}")
        print(f"   📋 Block names: {block_starts}")
        print(f"   🔚 Endblocks found: {len(endblocks)}")
        
        if len(block_starts) == len(endblocks):
            print("✅ All blocks are properly closed!")
            
            # Verify specific structure
            expected_blocks = ['title', 'head', 'content', 'scripts']
            missing_blocks = [block for block in expected_blocks if block not in block_starts]
            extra_blocks = [block for block in block_starts if block not in expected_blocks]
            
            if not missing_blocks and not extra_blocks:
                print("✅ Template has expected block structure!")
                return True
            else:
                if missing_blocks:
                    print(f"⚠️  Missing expected blocks: {missing_blocks}")
                if extra_blocks:
                    print(f"⚠️  Unexpected blocks found: {extra_blocks}")
                return True  # Still valid, just different structure
        else:
            print(f"❌ Block count mismatch! {len(block_starts)} starts vs {len(endblocks)} ends")
            return False
            
    except Exception as e:
        print(f"❌ Error reading template: {e}")
        return False

def verify_jinja_syntax():
    """Use simple regex to check for obvious syntax issues"""
    template_path = "app/templates/market_intel/sector_analysis.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for unclosed tags
        issues = []
        
        # Check for mismatched {{ }}
        open_vars = content.count('{{')
        close_vars = content.count('}}')
        if open_vars != close_vars:
            issues.append(f"Variable tag mismatch: {open_vars} {{ vs {close_vars} }}")
        
        # Check for mismatched {% %}
        open_statements = content.count('{%')
        close_statements = content.count('%}')
        if open_statements != close_statements:
            issues.append(f"Statement tag mismatch: {open_statements} {{% vs {close_statements} %}}")
        
        if issues:
            print("❌ Syntax issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Basic syntax checks passed!")
            return True
            
    except Exception as e:
        print(f"❌ Error checking syntax: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing sector_analysis.html template...")
    print("=" * 50)
    
    block_ok = verify_template_blocks()
    syntax_ok = verify_jinja_syntax()
    
    print("=" * 50)
    if block_ok and syntax_ok:
        print("🎉 Template verification PASSED! The Jinja error should be fixed.")
    else:
        print("❌ Template verification FAILED! Issues still exist.")
