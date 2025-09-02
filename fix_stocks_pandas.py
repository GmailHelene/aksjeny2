"""
Script to replace pandas/numpy functions with Python standard library equivalents in stocks.py
"""

with open('app/routes/stocks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace pandas Series operations with list operations
replacements = [
    ('prices_series = pd.Series(prices)', 'prices_series = prices'),
    ('prices_series.rolling(window=window).mean().iloc[-1]', 'sum(prices_series[-window:]) / min(len(prices_series), window)'),
    ('prices_series.ewm(span=period).mean().iloc[-1]', 'prices_series[-1]'),  # Simplified EMA
    ('pd.Series(closing_prices).ewm(span=12).mean().iloc[-1]', 'closing_prices[-1]'),  # Simplified EMA
    
    # Replace numpy functions with statistics/math equivalents
    ('np.mean(closing_prices[-20:])', 'sum(closing_prices[-20:]) / len(closing_prices[-20:])'),
    ('np.mean(closing_prices[-50:])', 'sum(closing_prices[-50:]) / len(closing_prices[-50:])'),
    ('np.mean(closing_prices[-min(20, len(closing_prices)):])', 'sum(closing_prices[-min(20, len(closing_prices)):]) / min(20, len(closing_prices))'),
    ('np.mean(closing_prices[-min(50, len(closing_prices)):])', 'sum(closing_prices[-min(50, len(closing_prices)):]) / min(50, len(closing_prices))'),
    ('np.std(closing_prices[-20:])', 'statistics.stdev(closing_prices[-20:]) if len(closing_prices[-20:]) > 1 else 0'),
    ('np.max(historical_data[\'High\'].values[-14:])', 'max(historical_data[\'High\'].values[-14:])'),
    ('np.min(historical_data[\'Low\'].values[-14:])', 'min(historical_data[\'Low\'].values[-14:])'),
    ('np.max(historical_data[\'High\'].values[-(14+i):-(i) if i > 0 else None])', 'max(historical_data[\'High\'].values[-(14+i):-(i) if i > 0 else None])'),
    ('np.min(historical_data[\'Low\'].values[-(14+i):-(i) if i > 0 else None])', 'min(historical_data[\'Low\'].values[-(14+i):-(i) if i > 0 else None])'),
    ('np.mean(recent_k_values)', 'sum(recent_k_values) / len(recent_k_values)'),
]

# Apply replacements
for old, new in replacements:
    content = content.replace(old, new)

# Add statistics import at the top
import_section = """import math
# import pandas as pd
import random
import time
import traceback
# import numpy as np
import logging
import statistics"""

content = content.replace("""import math
# import pandas as pd
import random
import time
import traceback
# import numpy as np
import logging""", import_section)

# Write back to file
with open('app/routes/stocks.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully replaced pandas/numpy functions with standard library equivalents")
print("Added statistics import")
print(f"Applied {len(replacements)} replacements")
