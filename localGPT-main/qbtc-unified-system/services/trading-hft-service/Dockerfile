# ==============================================================================
# || QBTC UNIFIED SYSTEM - DOCKERFILE: Trading HFT Service                    ||
# ==============================================================================
#
# Dockerfile para construir la imagen del servicio de High-Frequency Trading.
#

# --- Fase 1: Build -----------------------------------------------------------
# Usar una imagen base de Python más moderna y segura.
FROM python:3.11-slim-bookworm

# Establecer variables de entorno usando el formato clave=valor
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# --- Fase 2: Run -------------------------------------------------------------
# Exponer un puerto es opcional, ya que se comunica internamente vía RabbitMQ.

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
