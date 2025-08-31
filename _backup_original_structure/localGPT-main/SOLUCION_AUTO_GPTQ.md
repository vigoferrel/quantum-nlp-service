# 🛠️ SOLUCIÓN ERROR AUTO-GPTQ en LocalGPT

## ❌ PROBLEMA IDENTIFICADO

```
Error: AttributeError: 'NoneType' object has no attribute 'split'
Archivo: auto-gptq setup.py, línea 60
Causa: CUDA_VERSION es None en Windows
```

## ✅ SOLUCIÓN RÁPIDA

### Opción 1: Reparación Automática (Recomendada)
1. **Haz doble clic** en `reparar_auto_gptq.bat`
2. Selecciona opción "1" (Reparación completa)
3. ¡Listo!

### Opción 2: Reparación Manual
```bash
python reparar_definitivo.py
```

## 🎯 QUÉ HACE LA REPARACIÓN

### ❌ Paquetes Omitidos (Causan Problemas)
- `auto-gptq` - Error de CUDA_VERSION
- `bitsandbytes` - Reemplazado por versión Windows
- `unstructured[pdf]` - Dependencias problemáticas

### ✅ Paquetes Instalados (Funcionan)
- `torch` - PyTorch
- `transformers` - HuggingFace Transformers
- `langchain==0.0.267` - LangChain
- `chromadb==0.4.6` - Base de datos vectorial
- `sentence-transformers` - Embeddings
- `streamlit` - Interfaz web
- `llama-cpp-python` - Modelos GGUF
- `bitsandbytes-windows` - Versión para Windows

## 📋 DESPUÉS DE LA REPARACIÓN

### 1. Verificar Instalación
```bash
python iniciar_seguro.py
```

### 2. Añadir Documentos
- Copia tus archivos a `SOURCE_DOCUMENTS/`
- Formatos: PDF, TXT, DOCX, CSV, MD

### 3. Procesar Documentos
```bash
python ingest.py --device_type cpu
```

### 4. Hacer Preguntas
```bash
python run_localGPT.py --device_type cpu
```

## ⚙️ CONFIGURACIÓN OPTIMIZADA

### Archivo: `constants_windows.py`
```python
# Modelo optimizado para Windows
MODEL_ID = "TheBloke/Llama-2-7b-Chat-GGUF"
MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"

# Configuración de memoria reducida
N_GPU_LAYERS = 20    # Reducido de 100
N_BATCH = 256        # Reducido de 512
```

## 🚫 LIMITACIONES POST-REPARACIÓN

### ❌ No Funcionan
- Modelos GPTQ (requieren auto-gptq)
- Cuantización avanzada GPU
- Algunos loaders de PDF especializados

### ✅ Sí Funcionan
- Modelos GGUF (más compatibles)
- Modelos HuggingFace estándar
- Procesamiento CPU
- Interfaz web completa
- Todos los formatos de documento básicos

## 🎯 MODELOS RECOMENDADOS

### Para CPU (Siempre Funciona)
```python
MODEL_ID = "TheBloke/Llama-2-7b-Chat-GGUF"
MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"
```

### Para GPU NVIDIA (Si Disponible)
```python
MODEL_ID = "TheBloke/Llama-2-7b-Chat-GGUF"
MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"
```

## 🔧 COMANDOS ÚTILES

### Siempre Usar CPU (Más Estable)
```bash
python ingest.py --device_type cpu
python run_localGPT.py --device_type cpu
```

### Con Opciones Adicionales
```bash
# Mostrar fuentes
python run_localGPT.py --device_type cpu --show_sources

# Con historial
python run_localGPT.py --device_type cpu --use_history

# Guardar conversaciones
python run_localGPT.py --device_type cpu --save_qa
```

## 🆘 RESOLUCIÓN DE PROBLEMAS

### Si Sigue Fallando
1. **Limpia completamente**:
   ```bash
   python -m pip uninstall auto-gptq bitsandbytes -y
   python -m pip cache purge
   ```

2. **Instala mínimo**:
   ```bash
   pip install -r requirements_minimal.txt
   ```

3. **Usa solo CPU**:
   - Siempre añade `--device_type cpu`

### Error de Memoria
- Cierra otras aplicaciones
- Usa modelos más pequeños
- Reduce `N_BATCH` en constants.py

### GPU No Detectada
- Es normal, usa `--device_type cpu`
- Verifica drivers NVIDIA si tienes GPU

## 📁 ARCHIVOS CREADOS

```
localGPT-main/
├── reparar_definitivo.py        # Script de reparación
├── reparar_auto_gptq.bat       # Reparación fácil
├── iniciar_seguro.py           # Verificación de instalación
├── constants_windows.py        # Configuración optimizada
├── requirements_minimal.txt    # Dependencias mínimas
└── SOLUCION_AUTO_GPTQ.md      # Esta guía
```

## ✅ RESULTADO FINAL

Después de la reparación tendrás:
- ✅ LocalGPT funcionando al 100%
- ✅ Procesamiento de documentos
- ✅ Interfaz de preguntas y respuestas
- ✅ Interfaz web (opcional)
- ✅ Compatibilidad total con Windows
- ❌ Sin modelos GPTQ (pero GGUF funciona igual o mejor)

---

## 🚀 INICIO RÁPIDO POST-REPARACIÓN

1. `reparar_auto_gptq.bat` (solo una vez)
2. Copiar documentos a `SOURCE_DOCUMENTS/`
3. `python ingest.py --device_type cpu`
4. `python run_localGPT.py --device_type cpu`
5. ¡Hacer preguntas!

**¡Tu LocalGPT estará funcionando perfectamente sin el error de auto-gptq!**
