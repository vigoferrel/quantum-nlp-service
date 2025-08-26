# Dockerfile para el servicio Learning Updater

FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY updater.py .

# Ejecutar el updater
CMD ["python", "updater.py"]
