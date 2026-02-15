# Datei: /app/Dockerfile
FROM python:3.11-slim

WORKDIR /usr/src/app  # Standard Linux Pfad

# Kopiere requirements aus dem aktuellen Context (also /app Ordner)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest (handler.py etc.)
COPY . .

# User security
RUN useradd -m appuser && chown -R appuser /usr/src/app
USER appuser

CMD ["python", "handler.py"]
