import re

with open('app/__init__.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'✅', 'OK', content)
content = re.sub(r'🚨', 'CRITICAL', content)
content = re.sub(r'🔍', 'DEBUG', content)  
content = re.sub(r'🎯', 'SUCCESS', content)
content = re.sub(r'❌', 'ERROR', content)

with open('app/__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Emojis replaced')
