# VIGOLEONROCKS Deployment Dockerfile
# Optimizado para producción con todas las políticas aplicadas
FROM python:3.11-slim

# Metadata
LABEL maintainer="VIGOLEONROCKS"
LABEL description="Quantum NLP Service con métricas del sistema y soporte multilingüe"
LABEL version="2.0.0"

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
ENV PORT=5000
ENV HOST=0.0.0.0

# Políticas obligatorias
ENV BACKGROUND_EXECUTION=true
ENV PROMETHEUS_ENABLED=true
ENV METRICS_RNG_ENABLED=true
ENV QUANTUM_PROCESSOR_ENABLED=true

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Crear directorios necesarios
RUN mkdir -p logs run /var/log/vigoleonrocks

# Copiar código fuente
COPY . .

# Crear usuario no-root para seguridad
RUN useradd -r -u 1001 vigoleonrocks && \
    chown -R vigoleonrocks:vigoleonrocks /app && \
    chown -R vigoleonrocks:vigoleonrocks /var/log/vigoleonrocks

# Cambiar a usuario no-root
USER vigoleonrocks

# Exponer puertos
EXPOSE 5000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Comando por defecto - usar simple_api.py que cumple todas las políticas
CMD ["python", "simple_api.py"]
