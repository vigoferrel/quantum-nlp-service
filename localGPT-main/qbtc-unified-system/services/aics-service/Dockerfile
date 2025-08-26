# Dockerfile para el servicio AICS

FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
# Nota: el validation.json se montará como un volumen
COPY main.py .

# Exponer el puerto y ejecutar la aplicación
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
