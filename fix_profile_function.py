"""
This script will fix the profile function in main.py by:
1. Reading the file
2. Finding the profile function
3. Removing all indented code after the return statement
4. Writing the fixed content back to the file
"""

def fix_main_py():
    try:
        # Read the main.py file
        with open('app/routes/main.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find the profile function
        profile_start = -1
        for i, line in enumerate(lines):
            if '@main.route(\'/profile\')' in line:
                profile_start = i
                break
        
        if profile_start == -1:
            print("Couldn't find profile function")
            return False
        
        # Find where the function definition starts
        func_def_line = profile_start + 1
        while func_def_line < len(lines) and 'def profile()' not in lines[func_def_line]:
            func_def_line += 1
        
        # Find the return statement
        return_line = func_def_line + 1
        while return_line < len(lines) and 'return redirect' not in lines[return_line]:
            return_line += 1
        
        # Find the next function or route (which should be after all the indented code)
        next_func_line = return_line + 1
        while next_func_line < len(lines):
            if (next_func_line < len(lines) and 
                ('@main.route' in lines[next_func_line] or 
                 'def ' in lines[next_func_line] and not lines[next_func_line].startswith(' '))):
                break
            next_func_line += 1
        
        # Create the fixed content
        fixed_lines = lines[:return_line + 1]
        if next_func_line < len(lines):
            fixed_lines.append('\n')  # Add an empty line after the return
            fixed_lines.extend(lines[next_func_line:])
        
        # Write the fixed content back
        with open('app/routes/main.py', 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("Successfully fixed profile function in main.py")
        return True
    except Exception as e:
        print(f"Error fixing main.py: {e}")
        return False

if __name__ == '__main__':
    fix_main_py()
