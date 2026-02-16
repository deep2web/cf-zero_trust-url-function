import os
import json
import requests
import sys

# Output unbuffered für Docker Logs
sys.stdout.reconfigure(line_buffering=True)

def handle(event, context):
    target_url = os.environ.get('TARGET_URL')
    secret_json_str = os.environ.get('CLOUDFLARE_AUTH')
    
    # 1. Validierung
    if not target_url:
        print("Error: TARGET_URL variable missing", file=sys.stderr)
        return {"statusCode": 500, "body": "Error: TARGET_URL missing"}
    
    if not secret_json_str:
        print("Error: CLOUDFLARE_AUTH secret missing", file=sys.stderr)
        return {"statusCode": 500, "body": "Error: CLOUDFLARE_AUTH missing"}

    # 2. JSON Parsen
    try:
        creds = json.loads(secret_json_str)
        cf_id = creds.get('CF-Access-Client-Id')
        cf_secret = creds.get('CF-Access-Client-Secret')
        
        # Fallback für Leute, die aus Versehen Unterstriche nutzen
        if not cf_id: cf_id = creds.get('CF_Access_Client_Id')
        if not cf_secret: cf_secret = creds.get('CF_Access_Client_Secret')

        if not cf_id or not cf_secret:
             print(f"Error: JSON missing keys. Found: {list(creds.keys())}", file=sys.stderr)
             return {"statusCode": 500, "body": "Error: JSON keys missing"}
             
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return {"statusCode": 500, "body": "Error: Invalid JSON"}

    # 3. Request Session aufbauen
    session = requests.Session()
    
    # Header setzen (Exakt laut Cloudflare Doku)
    # Doku: "add the following to the headers of any HTTP request"
    session.headers.update({
        "CF-Access-Client-Id": cf_id,
        "CF-Access-Client-Secret": cf_secret,
        "User-Agent": "SOMSOS-CronBot/1.0",
        "Accept": "*/*" # Manchmal wichtig für APIs
    })

    try:
        print(f"Pinging {target_url}...", flush=True)
        
        # WICHTIG: allow_redirects=True ist Standard, aber wir loggen es explizit
        # Wir nutzen POST (wie von dir gewünscht), aber GET wäre für simple Pings üblicher.
        # Falls deine API Daten erwartet, füge json={} hinzu.
        response = session.post(target_url, timeout=30)
        
        # Cloudflare Redirect Handling Logik
        # Wenn wir einen 302 bekommen, heißt das oft: Auth hat geklappt, aber wir werden zur App geleitet
        if response.history:
            print(f"Notice: Request was redirected {len(response.history)} times.", flush=True)
            for resp in response.history:
                print(f" -> Redirect from {resp.url} ({resp.status_code})", flush=True)
        
        print(f"Final Status Code: {response.status_code}", flush=True)
        
        # Erweiterte Fehler-Ausgabe für Cloudflare Access Denied (403)
        if response.status_code == 403:
            print("Error: 403 Forbidden. This usually means Cloudflare Access rejected the token.", file=sys.stderr)
            print("Check: 1. Is the Service Token valid? 2. Is it added to the Access Policy?", file=sys.stderr)
            # Cloudflare gibt oft HTML zurück, wir geben nur die ersten 500 Zeichen aus
            print(f"Response Body (Start): {response.text[:500]}", file=sys.stderr)

        if not response.ok:
             print(f"Error Response: {response.text[:200]}", file=sys.stderr)

        return {
            "body": f"Success: {response.status_code}",
            "statusCode": 200 if response.ok else response.status_code
        }

    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}", file=sys.stderr)
        return {"statusCode": 500, "body": "SSL Error"}
    except Exception as e:
        print(f"Exception: {str(e)}", file=sys.stderr)
        return {"statusCode": 500, "body": str(e)}

if __name__ == "__main__":
    print("Starting manual execution...", flush=True)
    result = handle({}, {})
    print("Execution finished:", flush=True)
    print(result, flush=True)
    if result.get("statusCode", 200) >= 400:
        sys.exit(1)

