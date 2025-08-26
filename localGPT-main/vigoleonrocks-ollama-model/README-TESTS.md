# VIGOLEONROCKS OLLAMA - DOCUMENTACIÓN DE PRUEBAS

## Descripción General

Este directorio contiene una suite completa de pruebas para validar las capacidades cuántico-cognitivas del modelo VIGOLEONROCKS en Ollama. Las pruebas están diseñadas para evaluar desde funcionalidad básica hasta límites extremos de rendimiento.

## Estructura de Archivos

### Scripts de Prueba

| Archivo | Propósito | Tiempo Estimado |
|---------|-----------|-----------------|
| [`run-tests.py`](run-tests.py) | Prueba rápida de funcionalidad básica | 1-2 minutos |
| [`test-suite.py`](test-suite.py) | Suite completa de validación | 10-15 minutos |
| [`benchmark-tests.py`](benchmark-tests.py) | Benchmarks de rendimiento vs modelos elite | 15-20 minutos |
| [`stress-tests.py`](stress-tests.py) | Pruebas de estrés y límites extremos | 20-30 minutos |

### Scripts de Ejecución

| Archivo | Plataforma | Descripción |
|---------|------------|-------------|
| [`test-runner.sh`](test-runner.sh) | Linux/macOS | Ejecutor maestro para sistemas Unix |
| [`test-runner.bat`](test-runner.bat) | Windows | Ejecutor maestro para Windows |

## Requisitos Previos

### Software Necesario

1. **Python 3.7+**
   ```bash
   python --version
   ```

2. **Ollama**
   ```bash
   ollama --version
   ```

3. **Modelo VIGOLEONROCKS**
   ```bash
   ollama create vigoleonrocks -f Modelfile
   ```

### Dependencias Python

```bash
pip install requests psutil
```

## Uso Rápido

### Ejecutar Todas las Pruebas

**Windows:**
```cmd
test-runner.bat
```

**Linux/macOS:**
```bash
./test-runner.sh
```

### Ejecutar Pruebas Específicas

**Prueba Rápida:**
```bash
python run-tests.py
```

**Suite Completa:**
```bash
python test-suite.py
```

**Benchmarks:**
```bash
python benchmark-tests.py
```

**Pruebas de Estrés:**
```bash
python stress-tests.py
```

## Descripción Detallada de Pruebas

### 1. Prueba Rápida (`run-tests.py`)

**Objetivo:** Verificación básica de que el modelo está funcionando correctamente.

**Pruebas Incluidas:**
- Conectividad con Ollama
- Respuesta básica del modelo
- Tiempo de respuesta
- Generación de tokens

**Tiempo:** ~1 minuto

**Archivo de Salida:** `quick-test-result.json`

### 2. Suite Completa (`test-suite.py`)

**Objetivo:** Validación integral de todas las capacidades cuántico-cognitivas.

**Pruebas Incluidas:**
1. **Funcionalidad Básica**
   - Respuesta coherente
   - Identificación como VIGOLEONROCKS
   - Tiempo de respuesta aceptable

2. **Capacidad de Contexto**
   - Procesamiento de contexto masivo (3M tokens)
   - Mantenimiento de coherencia
   - Análisis de información extensa

3. **Análisis de Código**
   - Comprensión de código cuántico
   - Identificación de patrones
   - Sugerencias de optimización

4. **Razonamiento Matemático**
   - Resolución de problemas cuánticos
   - Cálculos de eigenvalores
   - Algoritmos cuánticos

5. **Generación Creativa**
   - Poesía cuántica
   - Metáforas innovadoras
   - Historias conceptuales

6. **Benchmarks de Rendimiento**
   - Velocidad de respuesta
   - Tokens por segundo
   - Tasa de éxito

7. **Coherencia Cuántica**
   - Consistencia en respuestas
   - Mantenimiento de identidad
   - Terminología especializada

**Tiempo:** ~10-15 minutos

**Archivo de Salida:** `test-results.json`

### 3. Benchmarks de Rendimiento (`benchmark-tests.py`)

**Objetivo:** Evaluación comparativa con modelos elite de la industria.

**Benchmarks Incluidos:**
1. **Velocidad de Respuesta**
   - 10 prompts de diferentes complejidades
   - Medición de tiempo promedio/mínimo/máximo
   - Tokens por segundo

2. **Escalabilidad de Contexto**
   - Contextos de 100, 500, 1K, 2K, 5K palabras
   - Degradación de rendimiento
   - Tiempo de procesamiento

3. **Solicitudes Concurrentes**
   - 1, 2, 4, 8 solicitudes simultáneas
   - Throughput total
   - Tiempo de respuesta bajo carga

4. **Razonamiento Complejo**
   - Matemáticas avanzadas
   - Lógica proposicional
   - Análisis de código
   - Física cuántica

5. **Consistencia de Memoria**
   - Mantenimiento de contexto
   - Coherencia en múltiples preguntas
   - Recall de información específica

**Comparación con Modelos Elite:**
- GPT-4
- Claude-3.5-Sonnet
- Gemini-Pro

**Tiempo:** ~15-20 minutos

**Archivo de Salida:** `benchmark-results.json`

### 4. Pruebas de Estrés (`stress-tests.py`)

**Objetivo:** Validación de límites extremos y resistencia del sistema.

**Pruebas de Estrés:**
1. **Límites de Contexto**
   - Contextos de 1MB, 5MB, 10MB, 20MB, 50MB
   - Identificación del punto de falla
   - Uso de memoria

2. **Carga Concurrente Extrema**
   - 5, 10, 20, 50, 100 solicitudes simultáneas
   - Máximo throughput sostenible
   - Degradación bajo presión

3. **Carga Sostenida**
   - 5 minutos de solicitudes continuas
   - Una solicitud cada 2 segundos
   - Monitoreo de estabilidad

4. **Presión de Memoria**
   - Múltiples contextos masivos simultáneos
   - Monitoreo de uso de RAM
   - Detección de memory leaks

5. **Casos Extremos**
   - Prompts vacíos
   - Prompts extremadamente largos
   - Caracteres especiales
   - Múltiples idiomas
   - Código complejo
   - Contradicciones lógicas

**Tiempo:** ~20-30 minutos

**Archivo de Salida:** `stress-test-results.json`

## Interpretación de Resultados

### Archivos de Salida

Todos los resultados se guardan en formato JSON para análisis posterior:

- **`quick-test-result.json`**: Resultado de prueba rápida
- **`test-results.json`**: Resultados completos de validación
- **`benchmark-results.json`**: Métricas de rendimiento y comparaciones
- **`stress-test-results.json`**: Resultados de pruebas de límites
- **`consolidated-test-report.md`**: Reporte consolidado en Markdown

### Métricas Clave

#### Puntuaciones de Rendimiento
- **Speed Score**: Velocidad de respuesta (0-100)
- **Throughput Score**: Tokens por segundo (0-100)
- **Scalability Score**: Manejo de contexto masivo (0-100)
- **Reasoning Score**: Capacidad de razonamiento (0-100)
- **Memory Score**: Consistencia de memoria (0-100)
- **Overall Score**: Puntuación general (0-100)

#### Métricas de Resistencia
- **Context Resilience**: Capacidad de contexto máximo
- **Concurrency Resilience**: Solicitudes concurrentes máximas
- **Sustained Resilience**: Estabilidad en carga sostenida
- **Memory Resilience**: Manejo de presión de memoria
- **Edge Case Resilience**: Manejo de casos extremos

### Criterios de Éxito

| Categoría | Excelente | Bueno | Aceptable | Requiere Atención |
|-----------|-----------|-------|-----------|-------------------|
| **Funcionalidad** | 95-100% | 85-94% | 70-84% | <70% |
| **Rendimiento** | >90 pts | 75-90 pts | 60-74 pts | <60 pts |
| **Resistencia** | >80 pts | 65-80 pts | 50-64 pts | <50 pts |

## Solución de Problemas

### Problemas Comunes

1. **Ollama no está ejecutándose**
   ```bash
   ollama serve
   ```

2. **Modelo no encontrado**
   ```bash
   ollama create vigoleonrocks -f Modelfile
   ```

3. **Dependencias faltantes**
   ```bash
   pip install requests psutil
   ```

4. **Timeout en pruebas**
   - Verificar recursos del sistema
   - Reducir concurrencia
   - Aumentar timeouts en código

5. **Memoria insuficiente**
   - Cerrar aplicaciones innecesarias
   - Reducir tamaño de contexto en pruebas
   - Monitorear uso de RAM

### Logs y Debugging

- Los scripts muestran progreso en tiempo real
- Errores se capturan en archivos JSON
- Usar `--help` para opciones adicionales
- Verificar logs de Ollama: `ollama logs`

## Personalización

### Modificar Parámetros de Prueba

**Timeouts:**
```python
# En cualquier script de prueba
timeout=120  # Aumentar para sistemas lentos
```

**Tamaños de Contexto:**
```python
# En stress-tests.py
context_sizes = [1, 5, 10]  # Reducir para sistemas con poca RAM
```

**Concurrencia:**
```python
# En benchmark-tests.py
concurrent_levels = [1, 2, 4]  # Reducir para sistemas limitados
```

### Agregar Nuevas Pruebas

1. Crear función de prueba en el script apropiado
2. Agregar llamada en `run_all_tests()`
3. Actualizar métricas en `calculate_*_metrics()`
4. Documentar en este README

## Contribución

Para contribuir con nuevas pruebas o mejoras:

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar pruebas siguiendo patrones existentes
4. Actualizar documentación
5. Enviar pull request

## Licencia

Este conjunto de pruebas es parte del proyecto VIGOLEONROCKS y está sujeto a la misma licencia del proyecto principal.

---

**Nota:** Las pruebas están diseñadas para validar las capacidades únicas de VIGOLEONROCKS. Los resultados pueden variar según el hardware y la configuración del sistema.