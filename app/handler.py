import os
import json
import requests

def handle(event, context):
    # 1. Konfiguration laden (URL ist öffentlich)
    target_url = os.environ.get('TARGET_URL')
    
    # 2. Den JSON-String aus der EINEN geheimen Variable laden
    # Ich nenne die Variable hier CLOUDFLARE_AUTH (muss in Scaleway so heißen)
    secret_json_str = os.environ.get('CLOUDFLARE_AUTH')
    
    # Sicherheits-Check: Fehlen Variablen?
    if not target_url:
        return {"statusCode": 500, "body": "Error: TARGET_URL variable missing"}
    
    if not secret_json_str:
        return {"statusCode": 500, "body": "Error: CLOUDFLARE_AUTH secret missing"}

    # 3. JSON parsen um an die inneren Werte zu kommen
    try:
        creds = json.loads(secret_json_str)
        
        # Die Keys müssen exakt so heißen wie in deinem Screenshot (Step 2)
        cf_id = creds.get('CF-Access-Client-Id')
        cf_secret = creds.get('CF-Access-Client-Secret')
        
        if not cf_id or not cf_secret:
             return {"statusCode": 500, "body": "Error: JSON does not contain correct keys"}
             
    except json.JSONDecodeError:
        return {"statusCode": 500, "body": "Error: Secret is not valid JSON"}

    # 4. Headers vorbereiten
    headers = {
        "CF-Access-Client-Id": cf_id,
        "CF-Access-Client-Secret": cf_secret
    }

    try:
        # Request senden
        print(f"Pinging {target_url}...")
        response = requests.post(target_url, headers=headers, timeout=10)
        
        return {
            "body": f"Success: {response.status_code}",
            "statusCode": 200
        }
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}




if __name__ == "__main__":
    print("Starting manual execution...", flush=True)
    
    # Dummy-Event/Context (werden im Container-Modus eh nicht genutzt)
    result = handle({}, {})
    
    print("Execution finished:", flush=True)
    print(result, flush=True)
