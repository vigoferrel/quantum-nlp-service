# Dockerfile para VIGOLEONROCKS - Quantum NLP Service
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorio para datos persistentes
RUN mkdir -p /app/data /app/logs /app/cache

# Variables de entorno
ENV PYTHONPATH=/app
ENV FLASK_APP=vigoleonrocks_server.py
ENV FLASK_ENV=production

# Puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Comando para ejecutar
CMD ["python", "vigoleonrocks_server.py"]