#!/usr/bin/env python3
"""
Manually run the init_database function to debug issues
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

print("🚀 MANUALLY RUNNING INIT_DATABASE...")

try:
    from app import init_database, DEMO_PRODUCTS

    print(f"📊 DEMO_PRODUCTS contains {len(DEMO_PRODUCTS)} products")

    # Run init_database manually
    print("🔧 Calling init_database()...")
    init_database()
    print("✅ init_database() call completed")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
