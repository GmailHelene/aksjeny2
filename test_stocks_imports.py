import sys
sys.path.insert(0, '.')

print("Starting import tests...")

# Test 1: Basic imports
try:
    import math
    import pandas as pd
    import random
    import time
    import traceback
    print("✅ Basic imports successful")
except Exception as e:
    print(f"❌ Basic imports failed: {e}")

# Test 2: Flask imports
try:
    from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
    from flask_login import current_user, login_required
    from datetime import datetime, timedelta
    print("✅ Flask imports successful")
except Exception as e:
    print(f"❌ Flask imports failed: {e}")

# Test 3: App specific imports one by one
try:
    from app.services.data_service import DataService
    print("✅ DataService imported")
except Exception as e:
    print(f"❌ DataService import failed: {e}")

try:
    from app.services.analysis_service import AnalysisService
    print("✅ AnalysisService imported")
except Exception as e:
    print(f"❌ AnalysisService import failed: {e}")

try:
    from app.utils.access_control import access_required
    print("✅ access_control imported")
except Exception as e:
    print(f"❌ access_control import failed: {e}")

print("Import tests complete")
