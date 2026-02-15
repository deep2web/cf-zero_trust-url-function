# Nutzen eines leichten Python-Images
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code kopieren
COPY . .

# User anlegen (Best Practice: Nicht als Root laufen)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Standard-Kommando (Kann von Scaleway überschrieben werden)
CMD ["python", "handler.py"]
