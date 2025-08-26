# VIGOLEONROCKS OLLAMA - GUÍA DE SOLUCIÓN DE PROBLEMAS

## Problemas Comunes y Soluciones

### 1. Error: "model requires more system memory"

**Síntoma:**
```
model requires more system memory (56.7 GiB) than is available (8.5 GiB)
```

**Causa:** El modelo está configurado con parámetros que requieren más memoria de la disponible.

**Solución:**

#### Opción A: Usar Configuración Automática
```bash
# Windows
setup-optimized.bat

# Linux/macOS
./setup-optimized.sh
```

#### Opción B: Configuración Manual
```bash
# Para sistemas con 16GB+ RAM
ollama rm vigoleonrocks
ollama create vigoleonrocks -f Modelfile-lightweight

# Para sistemas con 32GB+ RAM
ollama rm vigoleonrocks
ollama create vigoleonrocks -f Modelfile-optimized
```

### 2. Error: "Ollama no está ejecutándose"

**Síntoma:**
```
✗ Error: No se puede conectar a Ollama
```

**Solución:**
```bash
# Iniciar Ollama manualmente
ollama serve

# En otra terminal, verificar
curl http://localhost:11434/api/tags
```

### 3. Error: "Modelo VIGOLEONROCKS no encontrado"

**Síntoma:**
```
✗ Error: Modelo VIGOLEONROCKS no encontrado
```

**Solución:**
```bash
# Verificar modelos instalados
ollama list

# Crear modelo si no existe
ollama create vigoleonrocks -f Modelfile-lightweight
```

### 4. Rendimiento Lento

**Síntomas:**
- Respuestas muy lentas (>30 segundos)
- Alto uso de memoria
- Sistema congelado

**Soluciones:**

#### Reducir Parámetros de Contexto
```bash
# Usar configuración más ligera
ollama rm vigoleonrocks
ollama create vigoleonrocks -f Modelfile-lightweight
```

#### Optimizar Configuración del Sistema
```bash
# Cerrar aplicaciones innecesarias
# Verificar memoria disponible
free -h  # Linux
vm_stat  # macOS
```

### 5. Error HTTP 500 en Pruebas

**Síntoma:**
```
[GIN] 2025/07/16 - 22:25:26 | 500 | 181.3159ms | 127.0.0.1 | POST "/api/generate"
```

**Causa:** Modelo requiere más recursos de los disponibles.

**Solución:**
```bash
# Recrear con configuración ligera
ollama rm vigoleonrocks
ollama create vigoleonrocks -f Modelfile-lightweight

# Verificar funcionamiento
echo "Hola VIGOLEONROCKS" | ollama run vigoleonrocks
```

### 6. Pruebas Fallan Completamente

**Síntoma:**
```
Tasa de éxito: 0.0%
❌ VIGOLEONROCKS REQUIERE ATENCIÓN
```

**Solución Paso a Paso:**

1. **Verificar Ollama:**
```bash
ollama --version
ollama serve &
```

2. **Recrear Modelo:**
```bash
ollama rm vigoleonrocks
ollama create vigoleonrocks -f Modelfile-lightweight
```

3. **Prueba Manual:**
```bash
ollama run vigoleonrocks "Hola, ¿funcionas correctamente?"
```

4. **Ejecutar Prueba Rápida:**
```bash
python run-tests.py
```

### 7. Error de Dependencias Python

**Síntoma:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solución:**
```bash
pip install requests psutil
# o
pip3 install requests psutil
```

### 8. Problemas de Permisos (Linux/macOS)

**Síntoma:**
```
Permission denied: ./setup-optimized.sh
```

**Solución:**
```bash
chmod +x setup-optimized.sh
chmod +x test-runner.sh
```

### 9. Puerto 11434 Ocupado

**Síntoma:**
```
Error: bind: address already in use
```

**Solución:**
```bash
# Encontrar proceso usando el puerto
lsof -i :11434  # Linux/macOS
netstat -ano | findstr :11434  # Windows

# Terminar proceso si es necesario
kill -9 [PID]

# Reiniciar Ollama
ollama serve
```

### 10. Modelo No Responde

**Síntoma:**
- Comando se cuelga sin respuesta
- Timeout en pruebas

**Solución:**
```bash
# Verificar logs de Ollama
ollama logs

# Reiniciar servicio
pkill ollama
ollama serve

# Recrear modelo con configuración mínima
ollama create vigoleonrocks-test -f Modelfile-lightweight
ollama run vigoleonrocks-test "test"
```

## Configuraciones Recomendadas por Sistema

### Sistemas de 8GB RAM o menos
```bash
# Usar solo configuración lightweight
ollama create vigoleonrocks -f Modelfile-lightweight

# Parámetros adicionales para sistemas muy limitados
# Editar Modelfile-lightweight y reducir:
# num_ctx 4096
# num_predict 1024
# num_batch 128
```

### Sistemas de 16GB RAM
```bash
# Configuración lightweight estándar
ollama create vigoleonrocks -f Modelfile-lightweight
```

### Sistemas de 32GB+ RAM
```bash
# Configuración optimizada
ollama create vigoleonrocks -f Modelfile-optimized
```

### Sistemas de 64GB+ RAM
```bash
# Configuración original (si está disponible)
ollama create vigoleonrocks -f Modelfile
```

## Monitoreo de Recursos

### Verificar Uso de Memoria
```bash
# Linux
free -h
htop

# macOS
vm_stat
Activity Monitor

# Windows
Task Manager
wmic computersystem get TotalPhysicalMemory
```

### Verificar Uso de CPU
```bash
# Linux/macOS
top
htop

# Windows
Task Manager
```

## Logs y Debugging

### Habilitar Logs Detallados
```bash
# Ejecutar Ollama con logs verbosos
OLLAMA_DEBUG=1 ollama serve

# Ver logs en tiempo real
tail -f ~/.ollama/logs/server.log  # Linux/macOS
```

### Verificar Estado del Sistema
```bash
# Verificar conectividad
curl -v http://localhost:11434/api/tags

# Verificar modelos
ollama list

# Verificar espacio en disco
df -h  # Linux/macOS
dir C:\  # Windows
```

## Contacto y Soporte

Si los problemas persisten después de seguir esta guía:

1. Verifica que tienes la versión más reciente de Ollama
2. Consulta la documentación oficial de Ollama
3. Revisa los logs detallados del sistema
4. Considera usar una configuración más ligera temporalmente

## Scripts de Diagnóstico

### Script de Diagnóstico Rápido
```bash
#!/bin/bash
echo "=== DIAGNÓSTICO VIGOLEONROCKS ==="
echo "Ollama version: $(ollama --version)"
echo "Memoria total: $(free -h | grep '^Mem:' | awk '{print $2}')"
echo "Memoria libre: $(free -h | grep '^Mem:' | awk '{print $7}')"
echo "Modelos instalados:"
ollama list
echo "Estado del servicio:"
curl -s http://localhost:11434/api/tags > /dev/null && echo "✓ Ollama activo" || echo "✗ Ollama inactivo"
```

Guarda este script como `diagnose.sh`, dale permisos de ejecución y ejecútalo para obtener información rápida del sistema.