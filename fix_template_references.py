import os
import glob

# Define the paths to search
template_paths = [
    r'templates',
    r'app\templates'
]

# Find all HTML files
html_files = []
for path in template_paths:
    if os.path.exists(path):
        html_files.extend(glob.glob(os.path.join(path, '**', '*.html'), recursive=True))

print(f'Found {len(html_files)} HTML files to process')

# Replace in each file
updated_files = 0
for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "url_for('portfolio.index')" in content:
            new_content = content.replace("url_for('portfolio.index')", "url_for('portfolio.portfolio_overview')")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f'Updated: {file_path}')
            updated_files += 1
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

print(f'Successfully updated {updated_files} template files')
