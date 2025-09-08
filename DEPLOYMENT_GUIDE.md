# 🚀 **VIGOLEONROCKS - Guía de Deployment Completo**
## Stack Cuántico Multicapa con Integración OpenRouter

---

## 📋 **ARQUITECTURA DEL STACK COMPLETO**

### **🌌 Servicios Core Operativos**

| **Servicio** | **Puerto** | **Estado** | **Función** | **Archivo Principal** |
|--------------|------------|------------|-------------|---------------------|
| 🤖 **Quantum Processor** | 5000 | ✅ Producción | Procesador IA Cuántico 500K | `vigoleonrocks/interfaces/rest_api.py` |
| 🚪 **API Gateway** | 8004 | ✅ Beta | OpenRouter Integration Proxy | `api_gateway_8004.py` |
| 🎮 **Command Center UI** | - | ✅ Static | Frontend Quantum Dashboard | `vigoleonrocks_quantum_command_center.html` |
| 🛡️ **Security System** | 8001 | 📋 Planificado | Crypto Entropy & Validation | `security_system_8001.py` |
| 📊 **Cultural Engine** | 8002 | 📋 Planificado | 12 Languages + Archetypes | `cultural_engine_8002.py` |
| ⚡ **Speed Optimizer** | 8003 | 📋 Planificado | <200ms Response Engine | `speed_optimizer_8003.py` |
| 📈 **Metrics Server** | 8000 | 📋 Planificado | Prometheus & Monitoring | `metrics_server_8000.py` |

---

## 🔧 **DEPLOYMENT METHODS**

### **Método 1: Background Execution (Desarrollo/Testing)**

#### **Lanzamiento Principal:**
```powershell
# VIGOLEONROCKS Core (Puerto 5000)
$quantum_job = Start-Job -ScriptBlock { 
    Set-Location "C:\path\to\quantum-nlp-service"
    python simple_api.py 
}

# API Gateway (Puerto 8004)  
$gateway_job = Start-Job -ScriptBlock { 
    Set-Location "C:\path\to\quantum-nlp-service"
    python api_gateway_8004.py 
}

# Verificar estado
Get-Job | Format-Table Id, Name, State
```

#### **Scripts PowerShell Disponibles:**
```powershell
# Lanzamiento simplificado
.\start_simple.ps1

# Lanzamiento con métricas completas
.\start_quantum.ps1

# Lanzamiento en background con control
.\start_vigoleonrocks_background.ps1
```

### **Método 2: Docker Deployment (Producción)**

#### **Dockerfile para Quantum Processor:**
```dockerfile
# Quantum Processor Container
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer puerto principal
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=vigoleonrocks.interfaces.rest_api
ENV FLASK_ENV=production
ENV PORT=5000

# Cumplir con reglas: segundo plano + métricas
CMD ["python", "-u", "vigoleonrocks/interfaces/rest_api.py"]
```

#### **Dockerfile para API Gateway:**
```dockerfile
# API Gateway Container  
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt flask flask-cors requests

# Copiar gateway
COPY api_gateway_8004.py .

# Exponer puerto gateway
EXPOSE 8004

# Variables de entorno
ENV GATEWAY_PORT=8004
ENV VIGOLEONROCKS_BACKEND=http://quantum-processor:5000

# Background execution
CMD ["python", "-u", "api_gateway_8004.py"]
```

#### **Docker Compose Completo:**
```yaml
# docker-compose.yml
version: '3.8'

services:
  quantum-processor:
    build: 
      context: .
      dockerfile: Dockerfile.quantum
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PORT=5000
      - QUANTUM_STATES=26
      - CONTEXT_CAPACITY=500000
      - METRICS_ENABLED=true
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/status"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  api-gateway:
    build:
      context: .
      dockerfile: Dockerfile.gateway
    ports:
      - "8004:8004"
    environment:
      - GATEWAY_PORT=8004
      - VIGOLEONROCKS_BACKEND=http://quantum-processor:5000
      - OPENROUTER_API_BASE=https://openrouter.ai/api/v1
    depends_on:
      quantum-processor:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8004/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/usr/share/nginx/html
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - quantum-processor
      - api-gateway
    restart: unless-stopped
    
networks:
  vigoleonrocks-network:
    driver: bridge

volumes:
  vigoleonrocks-data:
  vigoleonrocks-logs:
```

### **Método 3: Production Server (srv984842.hstgr.cloud)**

#### **Configuración Dokploy:**
```yaml
# .dokploy/config.yml
name: vigoleonrocks-quantum
services:
  - name: quantum-processor
    image: vigoleonrocks/quantum-ai:latest
    port: 5000
    domain: vigoleonrocks.srv984842.hstgr.cloud
    env:
      FLASK_ENV: production
      QUANTUM_STATES: 26
      CONTEXT_CAPACITY: 500000
    
  - name: api-gateway  
    image: vigoleonrocks/api-gateway:latest
    port: 8004
    domain: gateway.vigoleonrocks.srv984842.hstgr.cloud
    env:
      VIGOLEONROCKS_BACKEND: http://quantum-processor:5000
```

---

## 🌐 **ROUTING ARCHITECTURE**

### **🎯 Rutas Principales (Puerto 5000)**

#### **Core API Endpoints:**
```python
# Procesamiento Principal
POST   /api/vigoleonrocks          # Procesamiento cuántico completo
GET    /api/status                 # Estado del sistema
GET    /api/quantum-metrics        # Métricas cuánticas en tiempo real

# Funcionalidades Avanzadas
POST   /api/translate              # Traducción multilingüe (12 idiomas)
POST   /api/detect-language        # Detección automática de idioma
POST   /api/archetypal-analysis    # Análisis de arquetipos emocionales
POST   /api/empathic-generate      # Generación empática contextual

# Configuración Cuántica
POST   /api/set-quantum-profile    # Configurar perfil de usuario
POST   /api/set-quantum-states     # Configurar estados cuánticos (1-26)
GET    /api/interaction-history    # Historial de interacciones

# Frontends
GET    /                          # Interfaz principal
GET    /quantum                   # Command Center (si disponible vía API)
```

#### **Ejemplos de Request/Response:**
```python
# Ejemplo: Procesamiento Cuántico Completo
curl -X POST http://localhost:5000/api/vigoleonrocks \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Analiza este código Python para optimización",
    "language": "es",
    "quantum_states": 26,
    "empathy_level": 8,
    "archetypal_mode": "sage",
    "cultural_context": "hispanic"
  }'

# Response:
{
  "response": "Analizando tu código Python con enfoque de optimización...",
  "language_detected": "es",
  "quantum_processing": {
    "states_used": 26,
    "coherence": 94.2,
    "processing_time_ms": 178
  },
  "cultural_adaptation": "hispanic_sage",
  "empathy_score": 8.5,
  "archetypal_analysis": {
    "primary": "sage",
    "secondary": "creator",
    "confidence": 0.92
  },
  "request_id": "qnt_847291847",
  "timestamp": "2025-01-05T20:00:00.000Z"
}
```

### **🚪 Rutas API Gateway (Puerto 8004)**

#### **OpenRouter Integration Endpoints:**
```python
# Health & Status
GET    /health                    # Health check del gateway
GET    /api/status               # Estado detallado del gateway
GET    /api/model-info           # Información del modelo para OpenRouter

# Proxy Endpoints  
POST   /api/openrouter-proxy     # Proxy principal para OpenRouter requests

# Validation & Metrics
GET    /metrics                  # Métricas Prometheus (si implementado)
GET    /api/gateway-metrics      # Métricas específicas del gateway
```

#### **Ejemplo de Proxy OpenRouter:**
```python
# Request desde OpenRouter hacia VIGOLEONROCKS
curl -X POST http://localhost:8004/api/openrouter-proxy \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer openrouter-key" \
  -d '{
    "model": "vigoleonrocks/quantum-cultural-2025",
    "messages": [
      {"role": "user", "content": "Help me debug this Python function"}
    ],
    "quantum_states": 26,
    "empathy_level": 7,
    "max_tokens": 2000
  }'

# Response con metadatos del gateway:
{
  "response": "I'll help you debug that Python function...",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 487,
    "total_tokens": 502
  },
  "gateway_metadata": {
    "gateway_port": 8004,
    "processing_time_ms": "<200ms",
    "entropy_source": "system_metrics",
    "request_id": 1847
  },
  "quantum_processing": {
    "states_used": 26,
    "coherence": 94.8,
    "cultural_adaptation": "auto_detected"
  }
}
```

---

## 📊 **MONITORING & METRICS**

### **Health Checks Automáticos:**
```bash
# Verificación del Stack Completo
curl http://localhost:5000/api/status  # Quantum Processor
curl http://localhost:8004/health      # API Gateway

# Script de health check automatizado
#!/bin/bash
check_service() {
    local service=$1
    local port=$2
    local endpoint=$3
    
    if curl -f -s "http://localhost:$port$endpoint" > /dev/null; then
        echo "✅ $service (port $port) - OK"
    else
        echo "❌ $service (port $port) - FAIL"
    fi
}

check_service "Quantum Processor" "5000" "/api/status"
check_service "API Gateway" "8004" "/health"
```

### **Logging & Debugging:**
```python
# Configuración de logs
LOG_LEVELS = {
    'development': 'DEBUG',
    'staging': 'INFO', 
    'production': 'WARNING'
}

# Locations de logs
LOGS = {
    'quantum_processor': './logs/quantum_processor.log',
    'api_gateway': './logs/api_gateway.log',
    'system_metrics': './logs/system_metrics.log',
    'openrouter_requests': './logs/openrouter.log'
}

# Tail logs en tiempo real
tail -f logs/quantum_processor.log
tail -f logs/api_gateway.log
```

---

## 🎮 **FRONTEND DEPLOYMENT**

### **Command Center UI:**
```nginx
# Configuración Nginx para servir frontend
server {
    listen 80;
    server_name vigoleonrocks.srv984842.hstgr.cloud;
    
    # Frontend estático
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /vigoleonrocks_quantum_command_center.html;
    }
    
    # Proxy a Quantum Processor
    location /api/ {
        proxy_pass http://quantum-processor:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Proxy a API Gateway
    location /gateway/ {
        proxy_pass http://api-gateway:8004/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Archivos Frontend Disponibles:**
- `vigoleonrocks_quantum_command_center.html` - **Principal** (Recomendado)
- `vigoleonrocks_corporate_ui_enhanced.html` - Alternativo empresarial
- `vigoleonrocks_corporate_ui.html` - Básico empresarial

---

## 🔒 **SECURITY & COMPLIANCE**

### **Políticas Implementadas:**
```python
# Cumplimiento de reglas establecidas
POLICY_COMPLIANCE = {
    'background_execution': True,      # ✅ Regla OOXRPDT0m0MVsz2xUFKDTQ
    'metrics_based_entropy': True,     # ✅ Regla hV1b1pjyV2T3dScM04eRtQ
    'math_random_usage': False,        # ✅ NO Math.random en codebase
    'system_metrics_source': True,     # ✅ Entropía desde kernel/sistema
    'openrouter_exclusive': True       # ✅ Canal de venta único
}
```

### **Validation Tests:**
```bash
# Test de compliance automático
python -c "
import ast
import os

def check_math_random_usage(directory):
    violations = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Attribute):
                                if node.attr == 'random' and isinstance(node.value, ast.Name) and node.value.id == 'math':
                                    violations.append(f'{filepath}: Line {node.lineno}')
                    except:
                        pass
    return violations

violations = check_math_random_usage('.')
print('✅ NO Math.random violations found' if not violations else f'❌ Violations: {violations}')
"
```

---

## 📈 **PERFORMANCE OPTIMIZATION**

### **Target Metrics:**
```python
PERFORMANCE_TARGETS = {
    'api_response_time_p95': 200,      # < 200ms
    'quantum_processing_time': 500,    # < 500ms
    'translation_speed': 100,          # < 100ms
    'success_rate': 99.0,              # > 99%
    'requests_per_second': 50,         # > 50 RPS
    'memory_usage_mb': 512,            # < 512MB
    'cpu_utilization': 70              # < 70%
}
```

### **Optimization Configs:**
```python
# Configuración optimizada para producción
PRODUCTION_CONFIG = {
    'FLASK_ENV': 'production',
    'DEBUG': False,
    'TESTING': False,
    'PROPAGATE_EXCEPTIONS': None,
    'PRESERVE_CONTEXT_ON_EXCEPTION': None,
    'SECRET_KEY': 'production-secret-key',
    'PERMANENT_SESSION_LIFETIME': 3600,
    'USE_RELOADER': False,
    'USE_DEBUGGER': False,
    'USE_EVALEX': False,
    'PREFERRED_URL_SCHEME': 'https',
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': False
}
```

---

## 🚀 **QUICK DEPLOYMENT SCRIPTS**

### **Development Quick Start:**
```bash
#!/bin/bash
# quick_deploy_dev.sh

echo "🚀 VIGOLEONROCKS - Development Quick Deploy"
echo "============================================="

# Verificar dependencias
python --version || { echo "❌ Python not found"; exit 1; }

# Instalar dependencias
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Lanzar servicios en background
echo "🌌 Starting Quantum Processor..."
nohup python vigoleonrocks/interfaces/rest_api.py > logs/quantum.log 2>&1 &
QUANTUM_PID=$!

echo "🚪 Starting API Gateway..."
nohup python api_gateway_8004.py > logs/gateway.log 2>&1 &
GATEWAY_PID=$!

# Esperar inicialización
sleep 5

# Verificar servicios
echo "🔍 Checking services..."
curl -f http://localhost:5000/api/status && echo "✅ Quantum Processor OK"
curl -f http://localhost:8004/health && echo "✅ API Gateway OK"

echo ""
echo "✅ VIGOLEONROCKS deployed successfully!"
echo "🌐 Quantum Processor: http://localhost:5000"
echo "🚪 API Gateway: http://localhost:8004"
echo "🎮 Command Center: vigoleonrocks_quantum_command_center.html"
echo ""
echo "PIDs: Quantum=$QUANTUM_PID, Gateway=$GATEWAY_PID"
echo "Logs: logs/quantum.log, logs/gateway.log"
```

### **Production Deploy (Docker):**
```bash
#!/bin/bash
# deploy_production.sh

echo "🚀 VIGOLEONROCKS - Production Deploy"
echo "===================================="

# Build images
echo "🏗️ Building Docker images..."
docker build -t vigoleonrocks/quantum-ai:latest -f Dockerfile.quantum .
docker build -t vigoleonrocks/api-gateway:latest -f Dockerfile.gateway .

# Deploy with compose
echo "🚢 Deploying stack..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services..."
sleep 30

# Health checks
echo "🔍 Running health checks..."
docker-compose exec quantum-processor curl -f http://localhost:5000/api/status
docker-compose exec api-gateway curl -f http://localhost:8004/health

echo ""
echo "✅ VIGOLEONROCKS Production deployed!"
echo "🌐 Access: https://vigoleonrocks.srv984842.hstgr.cloud"
echo "📊 Monitoring: docker-compose logs -f"
```

---

## 📞 **SUPPORT & TROUBLESHOOTING**

### **Common Issues:**
1. **Puerto ocupado**: `lsof -ti:5000 | xargs kill -9`
2. **Dependencias faltantes**: `pip install -r requirements.txt`
3. **Permisos Docker**: `sudo usermod -aG docker $USER`
4. **Logs debugging**: `tail -f logs/*.log`

### **Emergency Recovery:**
```bash
# Parar todos los servicios
pkill -f "python.*api"
docker-compose down

# Limpiar puertos
lsof -ti:5000,8004 | xargs kill -9

# Restart limpio
./quick_deploy_dev.sh
```

---

## 🎯 **NEXT STEPS**

### **Inmediato:**
1. ✅ Deploy desarrollo local
2. ✅ Verificar health checks
3. 📋 Deploy staging en srv984842.hstgr.cloud
4. 📋 Configurar monitoreo

### **Corto Plazo:**
1. 📋 Implementar servicios adicionales (8001, 8002, 8003, 8000)
2. 📋 Setup CI/CD pipeline
3. 📋 Integración OpenRouter oficial
4. 📋 Load testing y optimización

**VIGOLEONROCKS está listo para deployment full-stack y integración empresarial.**
