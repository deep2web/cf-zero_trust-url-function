FROM python:3.11-slim

# Verhindert, dass Python Outputs buffert
ENV PYTHONUNBUFFERED=1 

# 1. Setze das Arbeitsverzeichnis
WORKDIR /usr/src/app

# 2. Kopiere requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Kopiere den Rest des Codes
COPY . .

# 4. User anlegen und Rechte vergeben
RUN useradd -m appuser && chown -R appuser .

# 5. Zum User wechseln
USER appuser

CMD ["python", "handler.py"]
