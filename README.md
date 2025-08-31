# 🚀 VIGOLEONROCKS - Quantum NLP Service

[![CI/CD](https://github.com/vigoferrel/quantum-nlp-service/actions/workflows/deploy.yml/badge.svg)](https://github.com/vigoferrel/quantum-nlp-service/actions/workflows/deploy.yml)
[![Tests](https://github.com/vigoferrel/quantum-nlp-service/actions/workflows/test.yml/badge.svg)](https://github.com/vigoferrel/quantum-nlp-service/actions/workflows/test.yml)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://python.org)

> **Sistema de IA Cuántica Avanzado** - Respuestas humanas naturales con arquitectura de 26 dimensiones cuánticas

## ✨ Características

- 🧠 **Procesamiento Cuántico**: 26 dimensiones de análisis simultáneo
- 🎯 **Respuestas Humanas**: IA con empatía y personalidad natural
- 🌍 **Multi-idioma**: Soporte para español, inglés y portugués
- 🔬 **Análisis Arquetipal**: Detección de patrones profundos
- 🎨 **Generación Empática**: Respuestas adaptadas al contexto emocional
- 📊 **Benchmarking Elite**: Comparación con modelos de vanguardia
- 🏗️ **Arquitectura Modular**: Componentes especializados y escalables

## 🚀 Inicio Rápido

### Opción 1: Dokploy (Recomendado - Producción)

#### Método A: Dashboard Web
```bash
# 1. Instalar Dokploy en tu VPS
curl -sSL https://dokploy.com/install.sh | sh

# 2. Acceder al dashboard web
# http://tu-vps-ip:3000

# 3. Conectar repositorio GitHub
# - Ir a Projects → Create Project
# - Seleccionar "Connect Git Repository"
# - URL: https://github.com/vigoferrel/quantum-nlp-service
# - Dokploy detectará automáticamente dokploy.json

# 4. Configurar variables de entorno
# En Project Settings → Environment Variables:
DATABASE_URL=postgresql://user:password@postgres:5432/vigoleonrocks
REDIS_URL=redis://redis:6379
SECRET_KEY=tu-secret-key-aqui
OPENROUTER_API_KEY=tu-api-key-aqui
POSTGRES_PASSWORD=tu-password-postgres

# 5. Deploy automático
# Push a main → Deploy producción
# Push a develop → Deploy staging
```

#### Método B: API de Dokploy
```bash
# 1. Configurar variables de entorno
export DOKPLOY_SERVER_URL="http://tu-vps-ip:3000"
export DOKPLOY_API_TOKEN="tu-api-token"

# 2. Ejecutar script de deployment
python deploy_dokploy.py

# 3. Verificar estado
curl http://tu-vps-ip/api/status
```

#### Método C: GitHub Actions (Automático)
```yaml
# Configurar secrets en GitHub:
# DOKPLOY_SERVER_URL
# DOKPLOY_API_TOKEN
# DATABASE_URL
# REDIS_URL
# SECRET_KEY
# OPENROUTER_API_KEY
# POSTGRES_PASSWORD

# El workflow .github/workflows/dokploy-deploy.yml
# se ejecutará automáticamente en cada push
```

### Opción 2: Docker Local (Desarrollo)

```bash
# Clonar repositorio
git clone https://github.com/vigoferrel/quantum-nlp-service.git
cd quantum-nlp-service

# Copiar variables de entorno
cp .env.example .env

# Ejecutar con Docker Compose
docker-compose up -d

# Verificar estado
curl http://localhost:5000/api/status
```

### Opción 2: Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python vigoleonrocks_server.py

# Acceder a la aplicación
# Web: http://localhost:5000
# API: http://localhost:5000/api/status
```

## 📚 API Documentation

### Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `GET /` | GET | Interfaz web principal |
| `GET /api/status` | GET | Estado del sistema |
| `POST /api/vigoleonrocks` | POST | Procesamiento principal |
| `POST /api/translate` | POST | Traducción de textos |
| `POST /api/detect-language` | POST | Detección automática de idioma |
| `POST /api/archetypal-analysis` | POST | Análisis arquetipal |
| `POST /api/empathic-generate` | POST | Generación de respuestas empáticas |
| `GET /api/quantum-metrics` | GET | Métricas del sistema |

### Ejemplo de Uso

```python
import requests

# Procesar texto
response = requests.post('http://localhost:5000/api/vigoleonrocks', json={
    'text': 'Hola, ¿cómo estás?',
    'profile': 'human',
    'quantum_states': 26
})

print(response.json())
```

## 🏗️ Arquitectura

```
VIGOLEONROCKS ECOSYSTEM
├── 🎯 Core Services (Flask APIs)
├── 🧠 Quantum Engines (26D, Ion Fusion, Orchestrator)
├── 🎨 Web Interfaces (Corporate UI, Trinity System)
├── 📊 Benchmarking & Metrics
└── 🔬 Specialized Modules (Translation, Archetypal Analysis, Empathy)
```

### Componentes Principales

- **`vigoleonrocks_server.py`**: Servidor Flask principal con APIs REST
- **`quantum_orchestrator.py`**: Orquestador multi-modelo con fallback
- **`quantum_core_26d_engine.py`**: Motor de 26 dimensiones cuánticas
- **`vigoleonrocks_corporate_ui_enhanced.html`**: Interfaz web avanzada

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=. --cov-report=html

# Tests específicos
pytest tests/test_api.py -v
```

## 🚀 Deployment

### Desarrollo Local
```bash
./deploy.sh local build
./deploy.sh local deploy
```

### Staging
```bash
./deploy.sh staging deploy
```

### Producción
```bash
./deploy.sh prod deploy
```

### Con Docker
```bash
# Construir imagen
docker build -t vigoleonrocks .

# Ejecutar contenedor
docker run -p 5000:5000 vigoleonrocks
```

## 🔧 Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/vigoleonrocks

# Redis para cache
REDIS_URL=redis://localhost:6379

# APIs externas
OPENROUTER_API_KEY=your-api-key

# Configuración Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

## 📊 Monitoreo

### Métricas Disponibles
- CPU, Memoria, Disco
- Latencia de respuestas
- Tasa de éxito de APIs
- Estados cuánticos activos
- Historial de interacciones

### Dashboard
Accede a `http://localhost:5000` para ver el dashboard completo.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia Apache 2.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **Arquitectura Cuántica**: Inspirado en conceptos de procesamiento cuántico
- **Modelos de IA**: Integración con Claude, GPT-5, Gemini
- **Comunidad Open Source**: Por las herramientas y librerías utilizadas

## 📞 Contacto

- **Autor**: Vigo Ferrel
- **Email**: vigoferrel@quantum-nlp.com
- **GitHub**: [@vigoferrel](https://github.com/vigoferrel)
- **Web**: [https://vigoleonrocks.com](https://vigoleonrocks.com)

---

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Integración con Dokploy para deployment automático
- [ ] API de voz con Whisper
- [ ] Soporte para imágenes con CLIP
- [ ] Fine-tuning de modelos personalizados
- [ ] Dashboard de analytics avanzado

### Versiones
- **v1.0.0**: Sistema base funcional
- **v1.1.0**: Integración con Dokploy
- **v2.0.0**: Multi-modal (voz, imagen, texto)

---

**⭐ Si te gusta el proyecto, dale una estrella en GitHub!**
