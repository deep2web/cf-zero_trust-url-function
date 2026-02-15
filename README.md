# Scaleway Cloudflare Cron Trigger 🚀

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Scaleway](https://img.shields.io/badge/Scaleway-Serverless-purple?style=flat-square&logo=scaleway)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Zero%20Trust-orange?style=flat-square&logo=cloudflare)

Eine leichtgewichtige **Scaleway Serverless Function**, um zeitgesteuerte HTTP-Requests (Cron Jobs) an Endpunkte zu senden, die durch **Cloudflare Zero Trust (Access)** geschützt sind.

Entwickelt für interne Automatisierung bei **SOMSOS Limited**.

## sparkles: Features

- **Zero Trust Kompatibel:** Authentifiziert sich automatisch gegenüber Cloudflare Access mittels Service Tokens.
- **Konfigurierbar:** Ziel-URL kann über Umgebungsvariablen geändert werden, ohne den Code neu zu deployen.
- **Sicher:** Sensible Credentials (Client Secret) werden sicher als Scaleway Secrets verwaltet.
- **Kosteneffizient:** Läuft im Scaleway Free Tier (Serverless Functions).

## 🛠 Konfiguration

Die Funktion benötigt folgende Umgebungsvariablen und Secrets in der Scaleway Konsole:

### Environment Variables (Klartext)
Diese Variablen steuern das Ziel und können jederzeit geändert werden.

| Key | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `TARGET_URL` | Die volle URL, die aufgerufen werden soll. | `https://internal.somsos.net/api/sync` |

### Secrets (Verschlüsselt)
Diese Werte müssen im Bereich "Secrets" der Function hinterlegt werden. Sie werden für den `CF-Access-Client-Id` und `CF-Access-Client-Secret` Header genutzt.

| Key | Beschreibung | Woher? |
| :--- | :--- | :--- |
| `CF_CLIENT_ID` | Die ID des Cloudflare Service Tokens. | Cloudflare Zero Trust Dashboard |
| `CF_CLIENT_SECRET` | Das Secret des Service Tokens. | Cloudflare Zero Trust Dashboard |

## 🚀 Deployment (Manuell)

1. **Scaleway Function erstellen:**
   - Runtime: `Python 3.x`
   - Privacy: `Public` (Schutz erfolgt durch Nicht-Veröffentlichung der Trigger-URL oder interne Logik)

2. **Code einfügen:**
   Kopiere den Inhalt von `handler.py` in den Editor.

3. **Dependencies:**
   Füge `requests` zur `requirements.txt` hinzu.

4. **Variablen setzen:**
   Konfiguriere die oben genannten Env Vars und Secrets.

5. **Cron Trigger:**
   Füge in den Funktionseinstellungen einen Cron-Schedule hinzu (z.B. `0 3 * * *` für tägliche Ausführung um 3 Uhr nachts).

## 📦 Local Development

Um das Skript lokal zu testen, exportiere die Variablen in deiner Shell:

```bash
export TARGET_URL="https://example.com"
export CF_CLIENT_ID="deine-id"
export CF_CLIENT_SECRET="dein-secret"

python3 local_test.py
