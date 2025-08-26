#!/usr/bin/env python3
"""Simple template syntax checker"""

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
import os

def check_template_syntax():
    """Check if the sector analysis template has correct syntax"""
    try:
        # Create a simple Jinja2 environment
        env = Environment()
        
        # Read the template file content
        template_path = "app/templates/market_intel/sector_analysis.html"
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Try to parse the template
        template = env.from_string(template_content)
        print("✅ Template syntax is correct!")
        
        # Count blocks
        block_starts = template_content.count('{% block')
        endblock_count = template_content.count('{% endblock')
        
        print(f"📊 Block analysis:")
        print(f"   - Block starts: {block_starts}")
        print(f"   - Endblocks: {endblock_count}")
        
        if block_starts == endblock_count:
            print("✅ All blocks are properly closed!")
        else:
            print("❌ Block count mismatch!")
            
        return True
        
    except TemplateSyntaxError as e:
        print(f"❌ Template syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking template: {e}")
        return False

if __name__ == "__main__":
    check_template_syntax()
