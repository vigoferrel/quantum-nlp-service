# ==============================================================================
# || QBTC UNIFIED SYSTEM - DOCKERFILE: LLM API Service                        ||
# ==============================================================================
#
# Dockerfile para construir la imagen del servicio de API de LLM.
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
# Exponer el puerto 8000, que es el que usará Uvicorn por defecto.
EXPOSE 8000

# Comando para ejecutar la aplicación usando Uvicorn.
# --host 0.0.0.0 es crucial para que la aplicación sea accesible desde fuera del contenedor.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
