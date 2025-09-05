# 🔧 **Guía de Instalación y Desarrollo VIGOLEONROCKS**
## Sistema de IA Cuántica de Supremacía Contextual

---

## 📋 **Prerrequisitos del Sistema**

### **Requisitos Mínimos**
- **Python**: v3.11.0 o superior
- **Node.js**: v20.0.0 o superior (para componentes híbridos)
- **pip**: v23.0.0 o superior
- **Git**: v2.40.0 o superior
- **RAM**: 16GB mínimo (32GB recomendado para 500K tokens)
- **Almacenamiento**: 50GB libres (SSD recomendado)
- **CPU**: 8 cores mínimo (16+ recomendado)

### **Sistemas Operativos Soportados**
- Windows 10/11 Pro (recomendado)
- macOS 12.0+ (Monterey o superior)
- Ubuntu 22.04+ LTS / Debian 12+
- Fedora 38+
- Docker containers (multiplataforma)

### **Requisitos Adicionales para 500K Tokens**
- **GPU**: NVIDIA RTX 3080+ o AMD RX 6800+ (opcional, acelera procesamiento)
- **Conexión**: Ancho de banda mínimo 100 Mbps
- **Memoria Virtual**: Mínimo 64GB configurado

---

## 🚀 **Instalación Rápida (5 minutos)**

### **1. Clonar el Repositorio**
```bash
# Opción 1: HTTPS (público)
git clone https://github.com/vigoferrel/quantum-nlp-service.git

# Opción 2: SSH (desarrolladores autorizados)
git clone git@github.com:vigoferrel/quantum-nlp-service.git

cd quantum-nlp-service
```

### **2. Verificar Versiones del Sistema**
```bash
# Verificar Python (debe ser 3.11+)
python --version
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"

# Verificar pip
pip --version

# Verificar Git
git --version

# Verificar recursos del sistema
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().total//1024**3}GB')"
```

### **3. Setup Automático del Entorno**
```bash
# Script automático de instalación
chmod +x scripts/setup.sh
./scripts/setup.sh

# O manualmente:
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Instalación de dependencias optimizada para 500K tokens
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Tiempo estimado**: 3-7 minutos dependiendo de la conexión.

### **4. Configuración de Variables de Entorno**
```bash
# Copiar template de configuración
cp .env.template .env

# Editar configuración (usar tu editor preferido)
nano .env  # Linux/Mac
notepad .env  # Windows
```

**Configuración mínima .env:**
```env
# === CONFIGURACIÓN CORE VIGOLEONROCKS ===
# Quantum Processor (OBLIGATORIO)
QUANTUM_PROCESSOR_ENABLED=true
QUANTUM_CONTEXT_CAPACITY=500000  # UNIFIED STANDARD - LÍDER 2025
QUANTUM_DIMENSIONS=26
QUANTUM_COHERENCE_TIME=300

# Metrics-Based RNG (CRÍTICO - NO Math.random)
METRICS_RNG_ENABLED=true
METRICS_RNG_SEED_SOURCE=kernel
METRICS_RNG_ENTROPY_POOL_SIZE=4096
VIGOLEONROCKS_CONTEXT_SUPERIORITY=true

# Background Process (OBLIGATORIO)
BACKGROUND_EXECUTION=true
PROMETHEUS_ENABLED=true
METRICS_ENDPOINT=/api/status
QUANTUM_METRICS_ENDPOINT=/api/quantum-metrics

# API Configuration
HOST=0.0.0.0
PORT=5000
API_VERSION=v2
SECRET_KEY=your-super-secure-key-here-change-this

# OpenRouter Integration (Opcional)
OPENROUTER_API_KEY=your-openrouter-key-here
OPENROUTER_MODEL=vigoleonrocks/quantum-contextual-500k

# Logging & Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn-here
PROMETHEUS_PORT=8000
```

### **5. Primer Arranque y Verificación**
```bash
# Iniciar sistema en modo desarrollo
python -m vigoleonrocks.main --dev

# O usar el script optimizado
./scripts/start-dev.sh

# Verificar estado del sistema
curl http://localhost:5000/api/status
curl http://localhost:5000/api/quantum-metrics
```

**La aplicación estará disponible en:** `http://localhost:5000`

---

## 🔧 **Configuración Avanzada**

### **Configuración GPU (Aceleración 500K Tokens)**
```bash
# Para sistemas con GPU NVIDIA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verificar GPU disponible
python -c "import torch; print(f'GPU disponible: {torch.cuda.is_available()}')"
python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"No disponible\"}')"
```

### **Configuración IDE Optimizada**

#### **VSCode (Recomendado)**
Instalar extensiones para VIGOLEONROCKS:
```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter", 
    "ms-python.isort",
    "ms-python.pylint",
    "ms-toolsai.jupyter",
    "redhat.vscode-yaml",
    "ms-vscode.docker",
    "github.copilot",
    "visualstudioexptteam.vscodeintellicode"
  ]
}
```

#### **Configuración Python Estricta**
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "python.isortArgs": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true
  }
}
```

### **Configuración Docker (Opcional)**
```dockerfile
# Dockerfile.dev
FROM python:3.11-slim

# Optimizaciones para 500K tokens
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV QUANTUM_CONTEXT_CAPACITY=500000

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear usuario no-root
RUN useradd -m -u 1000 vigoleonrocks
USER vigoleonrocks

# Exponer puerto
EXPOSE 5000

# Comando por defecto
CMD ["python", "-m", "vigoleonrocks.main", "--production"]
```

```bash
# Construir y ejecutar con Docker
docker build -f Dockerfile.dev -t vigoleonrocks:dev .
docker run -p 5000:5000 --env-file .env vigoleonrocks:dev
```

---

## 🧪 **Configuración de Testing**

### **Suite de Testing Completa**
```bash
# Tests básicos
pytest tests/ -v

# Tests con coverage
pytest tests/ --cov=vigoleonrocks --cov-report=html --cov-report=term

# Tests de políticas críticas (MUST PASS)
pytest tests/unit/test_randomness_policy.py -v
pytest tests/unit/test_metrics_exposure.py -v

# Tests de rendimiento 500K tokens
pytest tests/performance/ -v --timeout=300

# Tests de integración completos
pytest tests/integration/ -v --timeout=600
```

### **Benchmarks de Rendimiento**
```bash
# Benchmark completo del sistema
python benchmarks/performance_test.py

# Benchmark específico 500K tokens
python benchmarks/context_500k_benchmark.py

# Comparativa con competidores
python benchmarks/competitive_analysis.py
```

---

## 🚀 **Scripts de Desarrollo**

### **Scripts Principales**
```bash
# === DESARROLLO ===
./scripts/start-dev.sh              # Desarrollo estándar
./scripts/start-dev-gpu.sh          # Desarrollo con GPU
./scripts/start-debug.sh            # Debug mode con logs verbose

# === TESTING ===
./scripts/run-tests.sh              # Suite completa de tests
./scripts/test-policies.sh          # Tests de políticas críticas
./scripts/benchmark.sh              # Benchmarks de rendimiento
./scripts/security-audit.sh         # Auditoría de seguridad

# === CALIDAD ===
./scripts/lint.sh                   # Linting completo
./scripts/format.sh                 # Auto-formatting
./scripts/type-check.sh             # Type checking estricto
./scripts/security-scan.sh          # Escaneo de vulnerabilidades

# === DEPLOYMENT ===
./scripts/build.sh                  # Build para producción
./scripts/deploy-staging.sh         # Deploy a staging
./scripts/deploy-production.sh      # Deploy a producción

# === UTILIDADES ===
./scripts/health-check.sh           # Verificación completa
./scripts/backup-config.sh          # Backup configuraciones
./scripts/system-info.sh            # Info del sistema
./scripts/cleanup.sh                # Limpieza completa
```

### **NPM Scripts (Componentes Híbridos)**
```json
// package.json
{
  "scripts": {
    "dev": "python -m vigoleonrocks.main --dev",
    "start": "python -m vigoleonrocks.main",
    "test": "pytest tests/ -v",
    "test:watch": "pytest-watch tests/",
    "test:coverage": "pytest tests/ --cov=vigoleonrocks --cov-report=html",
    "lint": "pylint vigoleonrocks/ && black --check vigoleonrocks/",
    "format": "black vigoleonrocks/ && isort vigoleonrocks/",
    "type-check": "mypy vigoleonrocks/",
    "benchmark": "python benchmarks/performance_test.py",
    "health-check": "./scripts/health-check.sh",
    "build": "./scripts/build.sh",
    "deploy": "./scripts/deploy-production.sh"
  }
}
```

---

## 🐛 **Troubleshooting Avanzado**

### **Problemas Comunes 500K Tokens**

#### **1. Error de Memoria Insuficiente**
```bash
# Error: MemoryError - insufficient memory for 500K context
# Solución:
export VIGOLEONROCKS_MEMORY_OPTIMIZATION=true
export QUANTUM_BATCH_SIZE=1000
python -c "import psutil; print(f'RAM disponible: {psutil.virtual_memory().available//1024**3}GB')"

# Aumentar memoria virtual (Windows)
# System > Advanced > Performance Settings > Virtual Memory > Custom Size: 65536MB

# Aumentar swap (Linux)
sudo fallocate -l 64G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### **2. Error de Política Randomness**
```bash
# Error: CRITICAL POLICY VIOLATION: Math.random detected
# Solución:
export METRICS_RNG_ENABLED=true
export VIGOLEONROCKS_CONTEXT_SUPERIORITY=true
python -c "from vigoleonrocks.config.env_validator import EnvironmentValidator; EnvironmentValidator().validate_environment()"
```

#### **3. Error de GPU/CUDA**
```bash
# Error: CUDA out of memory
# Solución:
export CUDA_VISIBLE_DEVICES=0
export VIGOLEONROCKS_GPU_MEMORY_FRACTION=0.7
python -c "import torch; torch.cuda.empty_cache() if torch.cuda.is_available() else None"
```

#### **4. Error de Puerto/Conexión**
```bash
# Error: Port 5000 already in use
# Solución:
export PORT=5001
lsof -ti:5000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :5000   # Windows
```

### **Verificación de Salud Completa**
```bash
# Script automático de verificación
./scripts/health-check.sh

# O verificación manual:
python -c "
import sys, psutil, torch
print(f'Python: {sys.version}')
print(f'RAM: {psutil.virtual_memory().total//1024**3}GB')
print(f'GPU: {torch.cuda.is_available()}')
print(f'CUDA: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')
"

# Verificar servicios
curl -f http://localhost:5000/api/status || echo "API no disponible"
curl -f http://localhost:8000/metrics || echo "Métricas no disponibles"

# Tests de políticas críticas
pytest tests/unit/test_randomness_policy.py::test_no_math_random_usage -v
pytest tests/unit/test_metrics_exposure.py::test_background_metrics_exposure -v
```

### **Logs de Debug Avanzados**
```bash
# Habilitar debug completo
export DEBUG=vigoleonrocks:*
export LOG_LEVEL=DEBUG
export QUANTUM_DEBUG=true

# Ver logs en tiempo real
tail -f logs/vigoleonrocks.log

# Análisis de performance
export VIGOLEONROCKS_PROFILING=true
python -m cProfile -o profile_output.prof -m vigoleonrocks.main
python -c "import pstats; p = pstats.Stats('profile_output.prof'); p.sort_stats('cumulative'); p.print_stats(20)"
```

---

## 🔧 **Configuración por Entorno**

### **Desarrollo Local**
```env
# .env.development
FLASK_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
QUANTUM_COHERENCE_TIME=60
METRICS_RNG_RESEED_INTERVAL=300
VIGOLEONROCKS_PROFILING=true
```

### **Testing/CI**
```env
# .env.test
FLASK_ENV=test
DEBUG=false
LOG_LEVEL=WARNING
QUANTUM_CONTEXT_CAPACITY=50000  # Reducido para tests rápidos
METRICS_RNG_ENABLED=true
DATABASE_URL=sqlite:///test.db
```

### **Staging**
```env
# .env.staging
FLASK_ENV=staging
DEBUG=false
LOG_LEVEL=INFO
QUANTUM_CONTEXT_CAPACITY=500000
PROMETHEUS_ENABLED=true
SENTRY_DSN=https://staging-sentry-dsn
```

### **Producción**
```env
# .env.production
FLASK_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
QUANTUM_CONTEXT_CAPACITY=500000
VIGOLEONROCKS_CONTEXT_SUPERIORITY=true
PROMETHEUS_ENABLED=true
METRICS_ENDPOINT=/api/status
QUANTUM_METRICS_ENDPOINT=/api/quantum-metrics
BACKGROUND_EXECUTION=true
SENTRY_DSN=https://production-sentry-dsn
```

---

## 📊 **Monitoreo de Performance**

### **Métricas de Desarrollo**
```bash
# Análisis de bundle/código
python -m py_compile vigoleonrocks/
python -m flake8 vigoleonrocks/ --statistics

# Performance profiling
python -m cProfile -s tottime -m vigoleonrocks.main --benchmark

# Memory profiling
pip install memory_profiler
python -m memory_profiler vigoleonrocks/core/quantum_processor.py

# Benchmark 500K tokens
python benchmarks/context_benchmark.py --tokens=500000 --iterations=10
```

### **Dashboard de Métricas**
```python
# Acceder a métricas en vivo
import requests
response = requests.get('http://localhost:8000/metrics')
print(response.text)

# Métricas cuánticas específicas
response = requests.get('http://localhost:5000/api/quantum-metrics')
print(response.json())
```

---

## 🤝 **Configuración para Contribuidores**

### **Git Hooks (Pre-commit)**
```bash
# Instalar pre-commit hooks
pip install pre-commit
pre-commit install

# Configurar hooks personalizados
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: local
    hooks:
      - id: test-policies
        name: Test Critical Policies
        entry: pytest tests/unit/test_randomness_policy.py -v
        language: system
        pass_filenames: false
EOF

# Ejecutar manualmente
pre-commit run --all-files
```

### **Conventional Commits**
```bash
# Ejemplos de commits válidos para VIGOLEONROCKS
git commit -m "feat: add 500K token context processing"
git commit -m "fix: resolve metrics-based RNG entropy issue"  
git commit -m "docs: update quantum processor documentation"
git commit -m "test: add coverage for cultural intelligence"
git commit -m "perf: optimize 26D quantum analysis speed"
git commit -m "security: enhance entropy validation"
```

---

## 🚢 **Deployment Avanzado**

### **Build Optimizado para Producción**
```bash
# Build con optimizaciones 500K tokens
python setup.py build_ext --inplace
python -m compileall vigoleonrocks/

# Crear distribución
python setup.py sdist bdist_wheel

# Verificar build
python -m vigoleonrocks.main --verify-build
./scripts/integration-test.sh
```

### **Docker Multi-stage para Producción**
```dockerfile
# Dockerfile.production
FROM python:3.11-slim as base

# Stage 1: Dependencies
FROM base as dependencies
WORKDIR /app
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Application
FROM dependencies as application
COPY . .
RUN python setup.py build_ext --inplace

# Stage 3: Production
FROM python:3.11-slim as production
WORKDIR /app
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=application /app /app

# Configurar usuario de producción
RUN useradd -m -u 1000 vigoleonrocks
USER vigoleonrocks

# Variables de entorno de producción
ENV FLASK_ENV=production
ENV QUANTUM_CONTEXT_CAPACITY=500000
ENV VIGOLEONROCKS_CONTEXT_SUPERIORITY=true

EXPOSE 5000 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/status || exit 1

CMD ["python", "-m", "vigoleonrocks.main", "--production"]
```

### **Kubernetes Deployment**
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vigoleonrocks
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vigoleonrocks
  template:
    metadata:
      labels:
        app: vigoleonrocks
    spec:
      containers:
      - name: vigoleonrocks
        image: vigoleonrocks:production
        ports:
        - containerPort: 5000
        - containerPort: 8000
        env:
        - name: QUANTUM_CONTEXT_CAPACITY
          value: "500000"
        - name: VIGOLEONROCKS_CONTEXT_SUPERIORITY
          value: "true"
        resources:
          requests:
            memory: "16Gi"
            cpu: "4000m"
          limits:
            memory: "32Gi"
            cpu: "8000m"
        livenessProbe:
          httpGet:
            path: /api/status
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/quantum-metrics
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 📞 **Soporte y Comunidad**

### **Canales de Soporte**
- **Issues Técnicos**: [GitHub Issues](https://github.com/vigoferrel/quantum-nlp-service/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vigoferrel/quantum-nlp-service/discussions)
- **Email Técnico**: dev-support@vigoleonrocks.com
- **Comercial**: vigoferrel@gmail.com

### **Información para Reportar Bugs**
Incluir siempre:
1. **Versión del Sistema**: `python -m vigoleonrocks.main --version`
2. **Configuración del Entorno**: SO, RAM, GPU, etc.
3. **Logs de Error**: Output completo de logs
4. **Pasos para Reproducir**: Secuencia exacta
5. **Variables de Entorno**: Configuración relevante (sin secrets)
6. **Tests de Políticas**: Resultado de `pytest tests/unit/test_randomness_policy.py`

```bash
# Script automático de reporte
./scripts/generate-bug-report.sh
```

### **Contribuciones Bienvenidas**
- 🧠 **AI/ML Engineering**: Mejoras al procesador cuántico
- 🔒 **Security**: Auditorías y mejoras de seguridad métrica
- 📊 **Performance**: Optimizaciones para 500K tokens
- 🌍 **i18n**: Nuevos idiomas y culturas
- 📱 **Frontend**: Interfaces y dashboards
- 🔧 **DevOps**: Mejoras de CI/CD y deployment

---

## 🎯 **Próximos Pasos**

### **Después de la Instalación:**
1. ✅ **Ejecutar tests de políticas**: `pytest tests/unit/test_randomness_policy.py`
2. ✅ **Verificar métricas cuánticas**: `curl http://localhost:5000/api/quantum-metrics`
3. ✅ **Probar procesamiento 500K**: `python benchmarks/context_500k_benchmark.py`
4. ✅ **Configurar monitoring**: Prometheus + Grafana
5. ✅ **Review documentación**: Leer ARCHITECTURE.md y API docs

### **Para Desarrollo:**
1. 🔧 **Configurar IDE** con extensiones recomendadas
2. 🧪 **Ejecutar suite completa** de tests
3. 📊 **Configurar profiling** para optimizaciones
4. 🔍 **Habilitar debug logs** para desarrollo
5. 🤝 **Configurar pre-commit hooks** para calidad

---

*Guía de Instalación VIGOLEONROCKS • Versión: 2.1.0-supreme • Actualizada: Septiembre 2025*

**🌌 "Construyendo el futuro de la IA cuántica, 500K tokens a la vez"** 🚀

<citations>
<document>
    <document_type>RULE</document_type>
    <document_id>OOXRPDT0m0MVsz2xUFKDTQ</document_id>
</document>
</citations>
