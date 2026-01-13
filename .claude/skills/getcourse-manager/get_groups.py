#!/usr/bin/env python3
"""
Get list of groups from GetCourse
"""
import os
import requests
import json
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load .env from workspace root (search upward)
def find_env_file():
    current = Path(__file__).resolve().parent
    while current != current.parent:
        env_file = current / '.env'
        if env_file.exists():
            return env_file
        current = current.parent
    return Path('/opt/ai-workspace/.env')  # fallback

load_dotenv(find_env_file())

# Get credentials from environment
ACCOUNT_NAME = os.getenv('GETCOURSE_ACCOUNT_NAME')
API_KEY = os.getenv('GETCOURSE_API_KEY')

if not ACCOUNT_NAME or not API_KEY:
    print(json.dumps({
        "success": False,
        "error": "Missing GETCOURSE_ACCOUNT_NAME or GETCOURSE_API_KEY in environment"
    }))
    exit(1)

# API endpoint
url = f"https://{ACCOUNT_NAME}.getcourse.ru/pl/api/account/groups"

# Empty params (just need to get all groups)
params_dict = {}
params_json = json.dumps(params_dict)
params_base64 = base64.b64encode(params_json.encode()).decode()

# Request data
data = {
    'action': 'get',
    'key': API_KEY,
    'params': params_base64
}

try:
    response = requests.post(url, data=data, timeout=30)
    response.raise_for_status()
    result = response.json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(json.dumps({
        "success": False,
        "error": str(e)
    }))
    exit(1)
