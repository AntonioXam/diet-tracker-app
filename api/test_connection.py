#!/usr/bin/env python3
"""Test connection to Supabase."""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env")
    exit(1)

print(f"URL: {SUPABASE_URL}")
print(f"KEY: {SUPABASE_KEY[:10]}...")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    # Try to fetch one row from users table
    response = supabase.table('users').select('count', count='exact').limit(1).execute()
    print(f"✅ Connection successful. Count: {response.count}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()