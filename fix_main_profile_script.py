import re

def fix_main_py():
    """Fix the profile function in main.py to remove indentation issues"""
    file_path = "app/routes/main.py"
    
    try:
        # Read the entire file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Define pattern to match the problematic function
        pattern = r'@main\.route\(\s*[\'"]\/profile[\'"]\s*\)[^@]*?def\s+profile\s*\(\s*\):\s*"""[^"]*""".*?(?=@main\.route|$)'
        
        # Replace with our fixed version
        replacement = '''@main.route('/profile')
@login_required
def profile():
    """Redirect to the new profile page under /user"""
    return redirect(url_for('profile.profile_page'))
'''
        
        # Use re.DOTALL to match across newlines
        fixed_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(fixed_content)
        
        print("Successfully fixed profile function in main.py")
        return True
    except Exception as e:
        print(f"Error fixing main.py: {e}")
        return False

if __name__ == "__main__":
    fix_main_py()
