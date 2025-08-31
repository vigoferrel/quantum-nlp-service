# 🔧 **Guía de Instalación - VIGOLEONROCKS**

## 📋 **Prerrequisitos del Sistema**

### **Requisitos Mínimos**
- **Python**: v3.8.0 o superior
- **Node.js**: v18.0.0 o superior (opcional para UI web)
- **pip**: v21.0.0 o superior
- **Git**: v2.25.0 o superior
- **RAM**: 8GB mínimo (16GB recomendado)
- **Almacenamiento**: 10GB libres

### **Sistemas Operativos Soportados**
- Windows 10/11
- macOS 10.15+
- Ubuntu 20.04+ / Debian 11+
- Fedora 35+

---

## 🚀 **Instalación Rápida**

### **1. Clonar el Repositorio**

```bash
# Opción 1: HTTPS
git clone https://github.com/vigoleonrocks/quantum-nlp-service.git

# Opción 2: SSH (recomendado para contribuidores)
git clone git@github.com:vigoleonrocks/quantum-nlp-service.git

cd quantum-nlp-service
```

### **2. Verificar Versiones**

```bash
# Verificar Python
python --version  # Debe ser v3.8+

# Verificar pip
pip --version     # Debe ser v21+

# Verificar Git
git --version     # Debe ser v2.25+
```

### **3. Instalación de Dependencias**

```bash
# Usando pip (recomendado)
pip install -r requirements.txt

# O usando conda
conda env create -f environment.yml
conda activate vigoleonrocks

# O usando pipenv
pipenv install
pipenv shell
```

**Tiempo estimado**: 3-5 minutos dependiendo de la conexión.

### **4. Configuración de Variables de Entorno**

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
nano .env  # o tu editor preferido
```

**Contenido mínimo de .env:**

```bash
# OpenRouter (Obligatorio para comparaciones)
OPENROUTER_API_KEY=tu_clave_openrouter_aqui

# OpenAI (Opcional)
OPENAI_API_KEY=tu_clave_openai_aqui

# Anthropic (Opcional)
ANTHROPIC_API_KEY=tu_clave_anthropic_aqui

# Google AI (Opcional)
GOOGLE_AI_API_KEY=tu_clave_google_aqui

# Configuración de Vigoleonrocks
VIGOLEONROCKS_MODE=quantum_ultra_extended
CONTEXT_CAPACITY=500000
QUANTUM_DIMENSIONS=32
PROCESSING_MODE=ultra_fast

# Modo de desarrollo
ENVIRONMENT=development
DEBUG_MODE=true
```

### **5. Primer Arranque**

```bash
# Iniciar sistema principal
python vigoleonrocks_quantum_ultra_extended.py

# O iniciar interfaz web
python vigoleonrocks_web_ui.py

# O ejecutar evaluación exhaustiva
python exhaustive_impossible_evaluation.py
```

**El sistema estará disponible en:** `http://localhost:8080`

---

## 🔧 **Configuración Avanzada**

### **Configuración Cuántica Completa**

```bash
# Variables avanzadas en .env
QUANTUM_COHERENCE=0.95
PROCESSING_THREADS=32
ENABLE_MULTIMODAL=true
SACRIFICE_SPEED_FOR_QUALITY=false
ENABLE_HOME_FIELD_DOMINATION=true
COMPETITIVE_MODE=aggressive
```

### **Configuración IDE**

#### **VSCode (Recomendado)**

Crear `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.pylint",
    "ms-toolsai.jupyter",
    "ms-vscode.vscode-json"
  ]
}
```

#### **Configuración de Python**

Crear `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"]
}
```

### **Configuración Docker (Recomendada)**

```bash
# Build imagen de Vigoleonrocks
docker build -t vigoleonrocks:latest .

# Ejecutar contenedor
docker run -d \
  --name vigoleonrocks \
  -p 8080:8080 \
  -v $(pwd)/.env:/app/.env \
  vigoleonrocks:latest

# O usar docker-compose
docker-compose up -d
```

---

## 🧪 **Configuración de Testing**

### **Instalación de Dependencias de Testing**

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# O individualmente
pip install pytest pytest-cov pytest-mock pytest-asyncio
pip install black flake8 pylint mypy
```

### **Ejecutar Tests**

```bash
# Tests básicos
pytest tests/

# Tests con coverage
pytest --cov=vigoleonrocks tests/

# Tests de rendimiento
python tests/performance_tests.py

# Tests competitivos
python tests/competitive_tests.py

# Tests de supremacía
python home_field_domination.py
```

---

## 🚀 **Scripts de Desarrollo**

```bash
# Evaluación
python exhaustive_impossible_evaluation.py    # Evaluación exhaustiva
python home_field_domination.py               # Dominación campo ajeno
python vigoleonrocks_ultra_speed.py          # Pruebas de velocidad

# Benchmarking
python latest_llm_comparison.py               # Comparación LLMs
python real_llm_comparison.py                 # Comparación real
python live_api_comparison.py                 # API en vivo

# Testing específico
python test_vigoleonrocks_quality.py         # Tests de calidad
python test_blueberry_challenge.py           # Desafío específico
python test_quantum_refinement_final.py      # Refinamiento cuántico

# Optimización
python vigoleonrocks_optimized_final.py      # Versión optimizada
python vigoleonrocks_hybrid_multimodal_service.py  # Servicio multimodal

# Interfaces
python vigoleonrocks_web_ui.py                # UI web
python vigoleonrocks_conversational_ui.py    # UI conversacional
```

---

## 🐛 **Troubleshooting**

### **Problemas Comunes**

#### **1. Error de Python Version**

```bash
# Error: Python version not supported
# Solución: Instalar Python 3.8+
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
```

#### **2. Error de API Keys**

```bash
# Error: API key not found
# Verificar configuración
cat .env | grep API_KEY

# Verificar permisos
chmod 600 .env
```

#### **3. Error de Memoria**

```bash
# Error: Out of memory
# Reducir capacidad de contexto en .env
CONTEXT_CAPACITY=250000
QUANTUM_DIMENSIONS=16
```

#### **4. Error de Dependencias**

```bash
# Error: Package not found
# Limpiar e instalar dependencias
pip cache purge
pip install --no-cache-dir -r requirements.txt
```

### **Verificación de Salud del Sistema**

```bash
# Script de verificación completa
python -c "
import sys
print(f'Python: {sys.version}')
import vigoleonrocks_quantum_ultra_extended
print('✅ Vigoleonrocks importado correctamente')
"

# Verificar configuración
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ Variables de entorno cargadas')
print(f'Modo: {os.getenv(\"VIGOLEONROCKS_MODE\")}')
print(f'Contexto: {os.getenv(\"CONTEXT_CAPACITY\")}')
"
```

### **Logs de Debug**

```bash
# Habilitar logs detallados
export DEBUG=1
python vigoleonrocks_quantum_ultra_extended.py

# Logs específicos de componentes
export DEBUG_QUANTUM=1
export DEBUG_SPEED=1
export DEBUG_COMPETITION=1
```

---

## 🔧 **Configuración por Entorno**

### **Desarrollo Local**

```bash
# .env.development
ENVIRONMENT=development
DEBUG_MODE=true
VIGOLEONROCKS_MODE=development
LOG_LEVEL=DEBUG
ENABLE_TESTING_MODE=true
```

### **Testing/CI**

```bash
# .env.test
ENVIRONMENT=test
VIGOLEONROCKS_MODE=test
MOCK_APIS=true
CONTEXT_CAPACITY=100000
QUANTUM_DIMENSIONS=8
```

### **Staging**

```bash
# .env.staging
ENVIRONMENT=staging
VIGOLEONROCKS_MODE=staging
DEBUG_MODE=false
COMPETITIVE_MODE=moderate
```

### **Producción**

```bash
# .env.production
ENVIRONMENT=production
VIGOLEONROCKS_MODE=quantum_ultra_extended
DEBUG_MODE=false
COMPETITIVE_MODE=aggressive
CONTEXT_CAPACITY=500000
QUANTUM_DIMENSIONS=32
```

---

## 📊 **Monitoreo de Performance**

### **Métricas de Desarrollo**

```bash
# Análisis de rendimiento
python -m cProfile -o profile.stats vigoleonrocks_quantum_ultra_extended.py

# Análisis de memoria
python -m memory_profiler vigoleonrocks_quantum_ultra_extended.py

# Benchmarks automáticos
python benchmarks/run_all_benchmarks.py
```

### **Configuración de Monitoreo**

```python
# monitoring_config.py
MONITORING = {
    'enable_metrics': True,
    'track_performance': True,
    'log_competitions': True,
    'save_benchmarks': True,
    'alert_on_degradation': True
}
```

---

## 🤝 **Configuración para Contribuidores**

### **Pre-commit Hooks**

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar hooks
pre-commit install

# Ejecutar en todos los archivos
pre-commit run --all-files
```

### **Configuración de pre-commit**

Crear `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pycqa/pylint
    rev: v3.0.0a6
    hooks:
      - id: pylint
```

### **Conventional Commits**

```bash
# Ejemplos de commits válidos
git commit -m "feat: add quantum processing optimization"
git commit -m "fix: resolve memory leak in context handling"
git commit -m "docs: update installation guide"
git commit -m "test: add coverage for competitive evaluation"
git commit -m "perf: optimize speed supremacy algorithm"
```

---

## 🚢 **Deployment**

### **Build para Producción**

```bash
# Preparar build
python setup.py build

# Crear distribución
python setup.py sdist bdist_wheel

# Verificar build
python -m twine check dist/*
```

### **Deploy con Docker**

```bash
# Build imagen de producción
docker build -f Dockerfile.prod -t vigoleonrocks:prod .

# Push a registry
docker tag vigoleonrocks:prod registry.com/vigoleonrocks:latest
docker push registry.com/vigoleonrocks:latest
```

### **Deploy en VPS**

```bash
# Usar script automatizado
python deploy_vps_supremacy.py --environment production

# O deploy manual
scp -r . user@server:/opt/vigoleonrocks/
ssh user@server 'cd /opt/vigoleonrocks && ./deploy.sh'
```

---

## 📞 **Soporte**

### **Canales de Soporte**

- **Issues**: [GitHub Issues](https://github.com/vigoleonrocks/quantum-nlp-service/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vigoleonrocks/quantum-nlp-service/discussions)
- **Email**: support@vigoleonrocks.ai
- **Discord**: [Servidor Discord](https://discord.gg/vigoleonrocks)

### **Información para Reportar Bugs**

Incluir siempre:

1. Versión de Python (`python --version`)
2. Sistema operativo y versión
3. Contenido de requirements.txt instalado
4. Pasos para reproducir el error
5. Logs completos del error
6. Configuración de .env (sin API keys)

```bash
# Script para recopilar info del sistema
python -c "
import sys, platform, pkg_resources
print(f'Python: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Packages: {len(list(pkg_resources.working_set))}')
"
```

---

## 🎯 **Verificación Post-Instalación**

### **Tests de Verificación**

```bash
# Test básico de funcionamiento
python -c "
try:
    import vigoleonrocks_quantum_ultra_extended
    print('✅ Vigoleonrocks cargado correctamente')
    
    # Test de configuración
    processor = vigoleonrocks_quantum_ultra_extended.UltraExtendedQuantumProcessor()
    print('✅ Procesador cuántico inicializado')
    
    print('🚀 INSTALACIÓN COMPLETADA EXITOSAMENTE')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Test de APIs (opcional)
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

apis = ['OPENROUTER_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
for api in apis:
    if os.getenv(api):
        print(f'✅ {api} configurado')
    else:
        print(f'⚠️  {api} no configurado (opcional)')
"

# Test de supremacía rápido
python exhaustive_impossible_evaluation.py --quick-test
```

---

## 🏆 **¡Instalación Completada!**

Si has llegado hasta aquí, **Vigoleonrocks** está listo para demostrar su supremacía. 

### **Próximos Pasos:**

1. **Ejecutar primera evaluación**: `python exhaustive_impossible_evaluation.py`
2. **Probar dominación campo ajeno**: `python home_field_domination.py`
3. **Verificar velocidad suprema**: `python vigoleonrocks_ultra_speed.py`
4. **Iniciar interfaz web**: `python vigoleonrocks_web_ui.py`

### **🎊 ¡Bienvenido a la Era de la Supremacía IA! 🎊**

---

*Guía actualizada: Agosto 2025 • Version: 1.0.0 • Status: SUPREMACÍA CONFIRMADA* 👑
