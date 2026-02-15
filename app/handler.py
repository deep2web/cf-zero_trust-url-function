import os
import requests

def handle(event, context):
    # 1. Konfiguration laden (URL ist öffentlich sichtbar in Settings)
    target_url = os.environ.get('TARGET_URL')
    
    # 2. Secrets laden (Cloudflare Auth)
    cf_id = os.environ.get('CF-Access-Client-Id')
    cf_secret = os.environ.get('CF-Access-Client-SecretT')

    # Sicherheits-Check: Fehlt was?
    if not target_url:
        return {"statusCode": 500, "body": "Error: TARGET_URL variable missing"}
    
    # Headers vorbereiten (nur wenn Secrets da sind, sonst ohne Auth probieren)
    headers = {}
    if cf_id and cf_secret:
        headers["CF-Access-Client-Id"] = cf_id
        headers["CF-Access-Client-Secret"] = cf_secret

    try:
        # Request senden
        print(f"Pinging {target_url}...") # Taucht in den Scaleway Logs auf
        response = requests.get(target_url, headers=headers, timeout=10)
        
        return {
            "body": f"Success: {response.status_code}",
            "statusCode": 200
        }
    except requests.exceptions.Timeout:
        return {"statusCode": 504, "body": "Timeout: Target took too long"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
