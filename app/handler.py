import os
import json
import requests
import sys

# Erzwingt unbuffered Output für Docker Logs (wichtig!)
sys.stdout.reconfigure(line_buffering=True)

def handle(event, context):
    # 1. Konfiguration laden
    target_url = os.environ.get('TARGET_URL')
    
    # 2. Secret laden
    secret_json_str = os.environ.get('CLOUDFLARE_AUTH')
    print(f"DEBUG: RAW SECRET STRING: '{secret_json_str}'", flush=True)

    
    # Sicherheits-Check
    if not target_url:
        print("Error: TARGET_URL variable missing", file=sys.stderr)
        return {"statusCode": 500, "body": "Error: TARGET_URL variable missing"}
    
    if not secret_json_str:
        print("Error: CLOUDFLARE_AUTH secret missing", file=sys.stderr)
        # Debugging-Hilfe (zeigt verfügbare Variablen, aber keine Werte)
        print(f"DEBUG: Available Env Vars: {list(os.environ.keys())}", file=sys.stderr)
        return {"statusCode": 500, "body": "Error: CLOUDFLARE_AUTH secret missing"}

    # 3. JSON parsen
    try:
        creds = json.loads(secret_json_str)
        
        # Keys müssen exakt stimmen!
        cf_id = creds.get('CF-Access-Client-Id')
        cf_secret = creds.get('CF-Access-Client-Secret')
        
        if not cf_id or not cf_secret:
             print("Error: JSON does not contain correct keys", file=sys.stderr)
             print(f"DEBUG: Found keys: {list(creds.keys())}", file=sys.stderr)
             return {"statusCode": 500, "body": "Error: JSON does not contain correct keys"}
             
    except json.JSONDecodeError as e:
        print(f"Error: Secret is not valid JSON: {str(e)}", file=sys.stderr)
        return {"statusCode": 500, "body": "Error: Secret is not valid JSON"}

    # 4. Request senden
    headers = {
        "CF-Access-Client-Id": cf_id,
        "CF-Access-Client-Secret": cf_secret,
        "User-Agent": "SOMSOS-CronBot/1.0" # Gut für Logs
    }

    try:
        print(f"Pinging {target_url}...", flush=True)
        # WICHTIG: requests.post statt .get (wie von dir gewünscht)
        response = requests.post(target_url, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}", flush=True)
        
        if response.status_code >= 400:
             print(f"Error Response: {response.text[:200]}", file=sys.stderr)

        return {
            "body": f"Success: {response.status_code}",
            "statusCode": 200 if response.ok else response.status_code
        }
    except Exception as e:
        print(f"Exception: {str(e)}", file=sys.stderr)
        return {"statusCode": 500, "body": str(e)}

if __name__ == "__main__":
    print("Starting manual execution...", flush=True)
    
    # Ausführen
    result = handle({}, {})
    
    print("Execution finished:", flush=True)
    print(result, flush=True)

    # Exit mit Fehlercode, falls der Job fehlgeschlagen ist
    if result.get("statusCode", 200) >= 400:
        sys.exit(1)

