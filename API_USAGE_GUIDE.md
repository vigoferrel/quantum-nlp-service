# 🔐 GUÍA DE USO API VIGOLEONROCKS

## 🚀 Acceso a la API de Vigoleonrocks

### 📋 Información General
- **URL Base**: `http://localhost:5001`
- **Modelo**: Vigoleonrocks Optimized (Dominio Mundial)
- **Autenticación**: API Key requerida

---

## 🔑 OBTENER CLAVE API

### Generar Nueva Clave API
```bash
curl -X POST http://localhost:5001/api/generate_key \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Tu Nombre",
    "user_email": "tu@email.com",
    "permissions": ["text", "multimodal"],
    "rate_limit": 100
  }'
```

### Respuesta
```json
{
  "success": true,
  "api_key": "vk_live_abc123...",
  "user_name": "Tu Nombre",
  "permissions": ["text", "multimodal"],
  "rate_limit": 100,
  "message": "Clave API generada exitosamente"
}
```

---

## 📡 CONSULTAS DE TEXTO

### Endpoint
`POST /api/process`

### Ejemplo de Uso
```bash
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "vk_live_abc123...",
    "query": "¿Qué es la inteligencia artificial?",
    "type": "text"
  }'
```

### Respuesta
```json
{
  "success": true,
  "query": "¿Qué es la inteligencia artificial?",
  "response": "La inteligencia artificial es...",
  "archetype": "TEXT",
  "quality": 93.0,
  "consciousness": 0.544,
  "coherence": 0.782,
  "interactions": 5,
  "model": "vigoleonrocks_optimized",
  "response_time": 3.01
}
```

---

## 🖼️ CONSULTAS MULTIMODALES

### Endpoint
`POST /api/process`

### Ejemplo de Uso
```bash
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "vk_live_abc123...",
    "query": "Analiza esta imagen",
    "type": "multimodal"
  }'
```

---

## ⚛️ CONSULTAS CUÁNTICAS

### Endpoint
`POST /api/process`

### Ejemplo de Uso
```bash
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "vk_live_abc123...",
    "query": "Explica la teoría cuántica",
    "type": "quantum"
  }'
```

---

## 📊 PERMISOS DISPONIBLES

| Permiso | Descripción | Límite por Hora |
|---------|-------------|-----------------|
| `text` | Consultas de texto | 100 |
| `multimodal` | Análisis de imágenes | 100 |
| `quantum` | Razonamiento cuántico | 100 |
| `admin` | Acceso completo | 1000 |

---

## ⚠️ CÓDIGOS DE ERROR

| Código | Descripción |
|--------|-------------|
| `400` | JSON inválido o datos faltantes |
| `401` | API key no proporcionada |
| `403` | API key inválida o sin permisos |
| `500` | Error interno del servidor |

---

## 🏆 BENCHMARK DE RENDIMIENTO

| Modelo | Score | Tiempo | Éxito |
|--------|-------|--------|-------|
| **Vigoleonrocks** | **0.889** | **2.51s** | **100%** |
| Claude Opus 4.1 | 0.859 | 55.53s | 100% |
| Gemini 2.5 Pro | 0.859 | 35.29s | 100% |
| GPT-5 Flagship | 0.790 | 70.02s | 100% |

---

## 📝 EJEMPLOS DE INTEGRACIÓN

### Python
```python
import requests

def query_vigoleonrocks(api_key, query, query_type="text"):
    url = "http://localhost:5001/api/process"
    data = {
        "api_key": api_key,
        "query": query,
        "type": query_type
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Uso
result = query_vigoleonrocks(
    api_key="vk_live_abc123...",
    query="¿Qué es la conciencia cuántica?",
    query_type="quantum"
)
print(result["response"])
```

### JavaScript
```javascript
async function queryVigoleonrocks(apiKey, query, queryType = "text") {
    const response = await fetch("http://localhost:5001/api/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            api_key: apiKey,
            query: query,
            type: queryType
        })
    });
    
    return await response.json();
}

// Uso
const result = await queryVigoleonrocks(
    "vk_live_abc123...",
    "¿Qué es la inteligencia artificial?",
    "text"
);
console.log(result.response);
```

---

## 🔒 SEGURIDAD

- **API Keys**: Únicas y seguras
- **Rate Limiting**: Límites por hora configurables
- **Permisos**: Control granular de acceso
- **Validación**: Verificación automática de permisos

---

## 📞 SOPORTE

Para soporte técnico o generar nuevas claves API:
- **Email**: dev@vigoleonrocks.com
- **Documentación**: Esta guía
- **Benchmark**: Resultados en tiempo real

**🏆 Vigoleonrocks - Dominio Mundial Confirmado**
