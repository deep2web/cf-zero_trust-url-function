# Cloudflare Zero Trust Cron Trigger (Scaleway) 🚀

![Docker](https://img.shields.io/badge/Docker-Container-blue?style=flat-square&logo=docker)
![Python](https://img.shields.io/badge/Python-3.11-yellow?style=flat-square&logo=python)
![Scaleway](https://img.shields.io/badge/Scaleway-Serverless-purple?style=flat-square&logo=scaleway)

Ein Docker-basierter **Scaleway Serverless Cron-Job**, um authentifizierte HTTP-Requests an Endpunkte zu senden, die durch **Cloudflare Zero Trust (Access)** geschützt sind.

Der Container wird automatisch via GitHub Actions gebaut und in die Scaleway Container Registry gepusht.

## ✨ Features

- **Zero Trust Authentication:** Nutzt Cloudflare Service Tokens (`CF-Access-Client-Id` & `Secret`).
- **Secure Configuration:** Credentials werden sicher als JSON-Objekt im Scaleway Secret Manager verwaltet.
- **Dockerized:** Sauberer Build-Prozess mit `python:3.11-slim`.
- **CI/CD:** Automatischer Push in die Scaleway Registry bei jedem Commit auf `main`.

## 📂 Projektstruktur

```text
/
├── .github/workflows/   # CI/CD Pipeline
├── app/                 # Quellcode
│   ├── Dockerfile       # Container Definition
│   ├── handler.py       # Python Logik
│   └── requirements.txt # Abhängigkeiten
└── README.md
```

## 🛠 Konfiguration (Scaleway)

Der Container benötigt zwei Arten von Umgebungsvariablen in der Scaleway Serverless Container Konfiguration:

### 1. Environment Variables (Klartext)

Hier wird das Ziel definiert.

| Key | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `TARGET_URL` | Die URL, die aufgerufen werden soll. | `https://internal.example.com/api/sync` |

### 2. Secrets (Verschlüsselt)

Erstelle im Scaleway Secret Manager **ein** Secret, das die Zugangsdaten als JSON enthält.

**Secret Name (Empfehlung):** `cloudflare-auth-json`

**Inhalt (JSON):**

```json
{
  "CF-Access-Client-Id": "deine-client-id",
  "CF-Access-Client-Secret": "dein-client-secret"
}
```

Binde dieses Secret dann im Container als **Environment Variable** ein:

| Environment Key | Secret Reference |
| :--- | :--- |
| `CLOUDFLARE_AUTH` | Verweist auf dein Secret `cloudflare-auth-json` (Version `latest`) |

## 🚀 Deployment (CI/CD)

Der Workflow `.github/workflows/push-to-scaleway.yml` baut das Image und lädt es hoch.

### Voraussetzungen im GitHub Repository:

Unter `Settings` -> `Secrets and variables` -> `Actions`:

**Repository Secrets:**
- `SCW_SECRET_KEY`: Dein Scaleway API Secret Key.

**Repository Variables:**
- `SCW_REGISTRY_IMAGE`: Die volle URL zu deinem Image in der Scaleway Registry.
  - *Beispiel:* `rg.nl-ams.scw.cloud/somsos-public/cf-zerotrust-url-function`

## 📦 Local Development

Um den Container lokal zu testen:

```bash
# Image bauen
docker build -t cron-bot ./app

# Container starten (mit Dummy-Werten)
docker run --rm \
  -e TARGET_URL="https://example.com" \
  -e CLOUDFLARE_AUTH='{"CF-Access-Client-Id":"123", "CF-Access-Client-Secret":"abc"}' \
  cron-bot
```

## 📄 License

MIT License - Copyright (c) 2026 SOMSOS Limited


_Teile des Codes wurden mittels des LLM Gemini 3 Pro erstellt_
