# 🚀 VIGOLEONROCKS - Guía de Desarrollo

Este documento proporciona información completa para desarrolladores que trabajen en el proyecto VIGOLEONROCKS, incluyendo las políticas críticas que DEBEN seguirse.

## 🚨 Políticas Críticas del Proyecto

### 1. 🚫 Política de Aleatoriedad
**ESTRICTAMENTE PROHIBIDO**:
- `Math.random()`
- `random.random()`, `random.choice()`, `random.randint()`
- `numpy.random.*`
- Cualquier generación de números aleatorios tradicional

**✅ CORRECTO**: Utiliza métricas del kernel y sistema para aleatoriedad:
```python
# ❌ PROHIBIDO
import random
value = random.choice([1, 2, 3])

# ✅ CORRECTO
from vigoleonrocks.core.metrics_based_rng import MetricsBasedRNG
rng = MetricsBasedRNG()
value = rng.choice_from_metrics([1, 2, 3])
```

### 2. 🔄 Política de Procesos en Segundo Plano
**OBLIGATORIO**:
- Todos los procesos y servidores DEBEN ejecutarse en segundo plano
- DEBEN reportar métricas de desempeño y lógica  
- DEBEN facilitar debugging y mantenimiento

**✅ CORRECTO**:
```bash
# Iniciar servidor en segundo plano
make start-bg

# Verificar métricas expuestas
curl http://localhost:5000/api/status
curl http://localhost:5000/api/quantum-metrics
```

## 📦 Setup de Desarrollo

### Prerrequisitos
- Python 3.8+
- Docker y Docker Compose
- Make
- Git

### 🏗️ Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd quantum-nlp-service

# 2. Setup completo de desarrollo
make dev-setup

# 3. Instalar dependencias
make install-dev

# 4. Verificar instalación
make test-policies  # CRÍTICO: debe pasar
```

## 🛠️ Comandos de Desarrollo

### Comandos Básicos
```bash
# Setup inicial completo
make dev-setup

# Instalar dependencias (runtime + development)
make install
make install-dev

# Limpiar archivos temporales
make clean
```

### 🧹 Calidad de Código
```bash
# Formateo automático
make format

# Linting completo
make lint

# Verificación de tipos
make type-check

# Todo lo anterior de una vez
make quality
```

### 🧪 Testing
```bash
# Tests críticos de política (DEBE pasar siempre)
make test-policies

# Tests unitarios
make test-unit

# Tests de integración  
make test-integration

# Todos los tests con cobertura
make test

# Tests con reporte de cobertura
make coverage
```

### 🔄 Gestión del Servidor

```bash
# Iniciar en primer plano (desarrollo)
make start

# Iniciar en segundo plano (producción/testing)
make start-bg

# Detener servidor
make stop

# Ver logs
make logs

# Estado del servidor
make status

# Health check completo
make health
```

### 🐳 Docker

```bash
# Build imagen Docker
make docker-build

# Ejecutar con Docker
make docker-run

# Stack completo con dependencias
make docker-stack

# Monitoreo (Prometheus, Grafana, etc.)
make monitoring-up
make monitoring-down
```

## 🧪 Testing y Validación

### Tests Críticos
**SIEMPRE ejecuta antes de commit**:
```bash
make test-policies
```

Este comando verifica:
- ✅ No uso de generadores aleatorios prohibidos
- ✅ Procesos ejecutándose en segundo plano
- ✅ Exposición correcta de métricas
- ✅ Cumplimiento de políticas multilinguales

### Estructura de Tests
```
tests/
├── unit/
│   ├── test_randomness_policy.py      # CRÍTICO
│   ├── test_metrics_exposure.py       # CRÍTICO
│   └── test_*.py
├── integration/
│   ├── test_api_integration.py
│   └── test_multilingual_integration.py
└── fixtures/
    └── *.py
```

### Markers de Tests
```bash
# Tests por categoría
pytest -m randomness    # Tests de política de aleatoriedad  
pytest -m metrics      # Tests de métricas
pytest -m multilingual # Tests multilinguales
pytest -m quantum      # Tests de funcionalidad quantum
pytest -m security     # Tests de seguridad
pytest -m slow         # Tests lentos (integración)
```

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios
```
vigoleonrocks/
├── core/
│   ├── metrics_based_rng.py     # CRÍTICO: RNG basado en métricas
│   ├── quantum_processor.py     # Procesamiento quantum
│   └── multilingual_engine.py   # Motor multilingual
├── interfaces/
│   ├── rest_api.py              # API REST con métricas
│   └── cli.py                   # Interfaz CLI
├── models/
│   └── *.py                     # Modelos de datos
└── utils/
    └── *.py                     # Utilidades
```

### Endpoints Obligatorios
Todos los servicios DEBEN exponer:
- `/api/status` - Estado del sistema y métricas básicas
- `/api/quantum-metrics` - Métricas quantum específicas

## 🌍 Soporte Multilingual

### Idiomas Soportados
- Español (es) - Principal
- Inglés (en)
- Portugués (pt)
- Francés (fr) 
- Alemán (de)

### Testing Multilingual
```python
@pytest.mark.multilingual
def test_multilingual_response():
    for lang in ["es", "en", "pt", "fr", "de"]:
        response = client.post("/api/vigoleonrocks", json={
            "text": "Hola mundo",
            "language": lang
        })
        assert response.status_code == 200
        assert "language" in response.json()
```

## 📊 Métricas y Monitoreo

### Métricas Obligatorias
Todo código DEBE exponer métricas de:
- Performance/latencia
- Tasa de éxito
- Estados quantum
- Uso de recursos
- Interacciones por idioma

### Ejemplo de Implementación
```python
from vigoleonrocks.core.metrics_collector import MetricsCollector

class MyService:
    def __init__(self):
        self.metrics = MetricsCollector()
    
    def process_request(self, data):
        with self.metrics.timer("request_processing"):
            result = self._process(data)
            self.metrics.increment("requests_processed")
            return result
```

## 🔐 Seguridad

### Escaneo de Seguridad
```bash
# Escaneo con Bandit
make security-scan

# Verificación de dependencias
make security-deps

# Ambos
make security
```

### Políticas de Seguridad
- No hardcodear secrets
- Validar todas las entradas
- Usar HTTPS en producción
- Auditoría regular de dependencias

## 🚀 CI/CD

### GitHub Actions
El pipeline automatizado verifica:
1. 🔒 Cumplimiento de política de aleatoriedad
2. 🔄 Verificación de procesos en segundo plano  
3. 🧹 Calidad de código (lint, format, types)
4. 🛡️ Seguridad (Bandit, Safety)
5. 🧪 Tests completos con cobertura
6. 🐳 Build de Docker
7. 🔗 Tests de integración
8. 🚀 Deploy automático

### Pre-commit Hooks
```bash
# Instalar hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

## 🆘 Debugging y Troubleshooting

### Logs
```bash
# Ver logs en tiempo real
make logs

# Logs específicos de métricas
make logs | grep "metrics"

# Logs de errores
make logs | grep "ERROR"
```

### Health Checks
```bash
# Verificar estado completo
make health

# Solo métricas
curl http://localhost:5000/api/status
curl http://localhost:5000/api/quantum-metrics
```

### Problemas Comunes

#### ❌ Error de Política de Aleatoriedad
```
ERROR: Math.random usage detected in file xyz.py
```
**Solución**: Reemplaza con `MetricsBasedRNG`

#### ❌ Servicio no en Segundo Plano
```
ERROR: Service not running in background
```
**Solución**: Usar `make start-bg` en lugar de `make start`

#### ❌ Métricas no Expuestas
```
ERROR: /api/status endpoint not found
```
**Solución**: Verificar que `rest_api.py` incluya los endpoints obligatorios

## 📚 Documentación Adicional

- `README.md` - Información general del proyecto
- `API.md` - Documentación de la API
- `DEPLOYMENT.md` - Guía de despliegue
- `CONTRIBUTING.md` - Guía de contribución

## 🤝 Contribuyendo

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. **CRÍTICO**: Ejecuta `make test-policies` antes de commit
4. Commit: `git commit -m "feat: nueva funcionalidad"`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Crea Pull Request

---

## ⚠️ RECORDATORIO CRÍTICO

**SIEMPRE antes de commit/push**:
```bash
make test-policies && make quality && make test
```

**Si alguno falla, NO PUSHEAR hasta resolver.**

Las políticas de aleatoriedad y procesos en segundo plano NO son negociables.
