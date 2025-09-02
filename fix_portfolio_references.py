with open('app/routes/portfolio.py', 'r', encoding='utf-8') as f:
    content = f.read()

original_count = content.count('portfolio.index')
new_content = content.replace("url_for('portfolio.index')", "url_for('portfolio.portfolio_overview')")
final_count = new_content.count('portfolio.index')

with open('app/routes/portfolio.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Replaced {original_count - final_count} portfolio.index references')
print(f'Remaining portfolio.index references: {final_count}')
