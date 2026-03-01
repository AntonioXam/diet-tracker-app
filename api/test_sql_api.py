#!/usr/bin/env python3
"""Test Supabase SQL API."""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
if SUPABASE_URL:
    PROJECT_REF = SUPABASE_URL.split('//')[1].split('.')[0]
else:
    PROJECT_REF = "lwbhdgpvigivgpyjqbeo"

ACCESS_TOKEN = os.getenv("SUPABASE_ACCESS_TOKEN") or "sbp_1ec3b72a123fc51889736833ba04e4138adb3afa"
API_URL = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Simple SELECT 1
sql = "SELECT 1 as test"

try:
    print(f"Testing SQL API at {API_URL}")
    print(f"Using token: {ACCESS_TOKEN[:10]}...")
    response = requests.post(API_URL, headers=headers, json={"query": sql}, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()