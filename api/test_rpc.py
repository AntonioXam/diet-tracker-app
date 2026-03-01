#!/usr/bin/env python3
"""Test RPC exec_sql."""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing env vars")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Try to create a simple index (IF NOT EXISTS)
sql = "CREATE INDEX IF NOT EXISTS idx_test ON users(name);"

try:
    print("Calling exec_sql...")
    result = supabase.rpc('exec_sql', {'sql': sql}).execute()
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()