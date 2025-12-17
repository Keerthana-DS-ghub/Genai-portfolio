# diag_infer1.py  
from dotenv import load_dotenv
import os
import requests
import json
import sys

load_dotenv()

API_KEY = os.getenv("IBM_APIKEY")
ML_URL = os.getenv("IBM_ML_URL", "https://us-south.ml.cloud.ibm.com").rstrip('/')
DEPLOYMENT_ID = os.getenv("WATSONX_DEPLOYMENT_ID")
VERSION = "2021-05-01"   # use the version shown in the deployment UI

if not (API_KEY and ML_URL and DEPLOYMENT_ID):
    print("ERROR: Missing IBM_APIKEY, IBM_ML_URL or WATSONX_DEPLOYMENT_ID in .env")
    sys.exit(1)

def get_token():
    """Exchange API key for IAM access token"""
    url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url, data=data, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def extract_text(obj):
    """Find a readable assistant message inside various possible JSON shapes."""
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj
    if isinstance(obj, list):
        for item in obj:
            t = extract_text(item)
            if t:
                return t
        return None
    if isinstance(obj, dict):
        # common keys where text can live
        for k in ("choices", "message", "messages", "content", "text", "output", "generated_text", "response"):
            if k in obj:
                t = extract_text(obj[k])
                if t:
                    return t
        # search all values
        for v in obj.values():
            t = extract_text(v)
            if t:
                return t
    return None

def infer_chat(prompt: str, timeout: int = 60):
    """
    Call the watsonx chat endpoint and return a structured dict:
    - {"ok": True, "json": response_json}
    - {"ok": False, "status": int, "text": "..."}  (for non-2xx)
    """
    token = get_token()
    endpoint = f"{ML_URL}/ml/v1/deployments/{DEPLOYMENT_ID}/text/chat?version={VERSION}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"messages": [{"role": "user", "content": prompt}]}

    r = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
    if not r.ok:
        return {"ok": False, "status": r.status_code, "text": r.text}
    try:
        j = r.json()
    except Exception:
        return {"ok": False, "status": r.status_code, "text": r.text}
    return {"ok": True, "json": j}

# Quick local test when run directly
if __name__ == "__main__":
    res = infer_chat("Hello Watsonx! Please reply briefly.")
    if not res.get("ok"):
        print(f"Runtime error: {res.get('status')} — {res.get('text')}")
    else:
        print("STATUS: 200 (OK)")
        # pretty print whole json (trimmed)
        print(json.dumps(res["json"], indent=2)[:4000])
        # extract assistant text and show it
        reply = extract_text(res["json"])
        print("\n=== Assistant reply (extracted) ===")
        print(reply or "(no text found)")
