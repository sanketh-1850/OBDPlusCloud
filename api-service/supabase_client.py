import os
import requests

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]

HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Accept": "application/json"
}

def get_dtc_info(code: str):
    url = f"{SUPABASE_URL}/rest/v1/obd_codes"

    params = {
        "select": "code,tcode,sections",
        "code": f"eq.{code}",
        "limit": 1
    }

    res = requests.get(url, headers=HEADERS, params=params, timeout=10)

    if res.status_code != 200:
        print("[Supabase REST ERROR]", res.status_code, res.text)
        return None

    data = res.json()

    if not data:
        return None

    return data[0]
