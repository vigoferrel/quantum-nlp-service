# VIGOLEONROCKS - Quantum NLP Service
# Production-Ready Deployment Dockerfile
# Updated: September 2025
# Version: 2.1.0-supreme

FROM python:3.11-slim

# Metadata
LABEL maintainer="vigoferrel <vigoferrel@gmail.com>"
LABEL description="VIGOLEONROCKS: Quantum-Inspired Natural Language Processing Research Project"
LABEL version="2.1.0-supreme"
LABEL org.opencontainers.image.title="VIGOLEONROCKS"
LABEL org.opencontainers.image.description="Experimental quantum-inspired AI system for NLP research"
LABEL org.opencontainers.image.version="2.1.0-supreme"
LABEL org.opencontainers.image.created="2025-09-05"
LABEL org.opencontainers.image.source="https://github.com/vigoferrel/quantum-nlp-service"

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
ENV NODE_ENV=production
ENV PORT=5000
ENV HOST=0.0.0.0
ENV WORKERS=4

# Políticas de seguridad VIGOLEONROCKS (obligatorias)
ENV BACKGROUND_EXECUTION=true
ENV PROMETHEUS_ENABLED=true
ENV METRICS_RNG_ENABLED=true
ENV QUANTUM_PROCESSOR_ENABLED=true
ENV SYSTEM_ENTROPY_ENABLED=true
ENV MATH_RANDOM_DISABLED=true

# Configuración de performance
ENV GUNICORN_WORKERS=4
ENV GUNICORN_THREADS=2
ENV GUNICORN_MAX_REQUESTS=1000
ENV GUNICORN_TIMEOUT=30

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Crear directorios necesarios
RUN mkdir -p logs run data /var/log/vigoleonrocks metrics monitoring

# Copiar código fuente
COPY . .

# Crear usuario no-root para seguridad
RUN useradd -r -u 1001 -g root vigoleonrocks && \
    chown -R vigoleonrocks:root /app && \
    chown -R vigoleonrocks:root /var/log/vigoleonrocks && \
    chmod -R 755 /app && \
    chmod -R 755 /var/log/vigoleonrocks

# Cambiar a usuario no-root
USER vigoleonrocks

# Exponer puertos
EXPOSE 5000 8000 9090

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Comando por defecto - usar flask_app.py con aplicación completa
# Ejecutar en segundo plano con métricas para depuración (Política #1)
CMD ["python", "flask_app.py", "--background", "--metrics", "--prometheus"]
