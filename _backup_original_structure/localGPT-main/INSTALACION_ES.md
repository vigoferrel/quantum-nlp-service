# LocalGPT - Instalación y Uso en Español

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)
1. Haz doble clic en `instalar.bat`
2. Sigue las instrucciones en pantalla
3. ¡Listo!

### Opción 2: Instalación Manual
1. Abre una terminal/cmd en esta carpeta
2. Ejecuta: `python install_localgpt.py`

## 📋 Requisitos del Sistema

- **Python 3.10 o superior** (obligatorio)
- **8GB RAM mínimo** (16GB recomendado)
- **10GB espacio libre** para modelos
- **GPU NVIDIA** (opcional, mejora rendimiento)

## 🔧 Configuración Inicial

### 1. Verificar Instalación
```bash
python --version  # Debe mostrar 3.10+
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Para GPU NVIDIA (Opcional)
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir
```

## 📖 Uso Básico

### Inicio Rápido
1. Haz doble clic en `iniciar.bat`
2. Selecciona la opción que necesites

### Paso a Paso

#### 1. Añadir Documentos
- Copia tus archivos a `SOURCE_DOCUMENTS/`
- Formatos soportados: PDF, TXT, DOCX, CSV, MD, HTML

#### 2. Procesar Documentos
```bash
python ingest.py
```

#### 3. Hacer Preguntas
```bash
python run_localGPT.py
```

#### 4. Interfaz Web
```bash
# Terminal 1
python run_localGPT_API.py

# Terminal 2
cd localGPTUI
python localGPTUI.py
```
Luego abre: http://localhost:5111/

## ⚙️ Configuración Avanzada

### Cambiar Modelo LLM
Edita `constants.py`:
```python
MODEL_ID = "TheBloke/Llama-2-7b-Chat-GGUF"
MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"
```

### Opciones de Comando
```bash
# Mostrar fuentes
python run_localGPT.py --show_sources

# Usar historial de chat
python run_localGPT.py --use_history

# Guardar conversaciones
python run_localGPT.py --save_qa

# Forzar CPU
python ingest.py --device_type cpu
```

## 🛠️ Resolución de Problemas

### Error: "No module named..."
```bash
pip install -r requirements.txt
```

### Error: "Microsoft Visual C++ 14.0 is required"
- Instala Visual Studio Build Tools
- O instala Visual Studio Community

### GPU no detectada
- Verifica drivers NVIDIA actualizados
- Reinstala CUDA si es necesario
- Usa `--device_type cpu` como alternativa

### Memoria insuficiente
- Cierra otras aplicaciones
- Edita `constants.py`:
```python
N_GPU_LAYERS = 10  # Reducir de 100
N_BATCH = 256      # Reducir de 512
```

## 📁 Estructura de Archivos

```
localGPT-main/
├── SOURCE_DOCUMENTS/     # Tus documentos aquí
├── DB/                   # Base de datos vectorial
├── models/               # Modelos descargados
├── localGPTUI/          # Interfaz web
├── install_localgpt.py  # Instalador
├── instalar.bat         # Instalador Windows
├── iniciar.bat          # Menú de inicio
└── requirements.txt     # Dependencias
```

## 🔒 Privacidad y Seguridad

- ✅ **100% Local**: Ningún dato sale de tu computadora
- ✅ **Sin Internet**: Funciona offline después de la instalación
- ✅ **Privado**: Tus documentos nunca se envían a servidores externos
- ✅ **Seguro**: No se almacenan logs remotos

## 📊 Requisitos de VRAM por Modelo

| Modelo | float32 | float16 | GPTQ 8bit | GPTQ 4bit |
|--------|---------|---------|-----------|-----------|
| 7B     | 28 GB   | 14 GB   | 7-9 GB    | 3.5-5 GB  |
| 13B    | 52 GB   | 26 GB   | 13-15 GB  | 6.5-8 GB  |
| 32B    | 130 GB  | 65 GB   | 32-35 GB  | 16-19 GB  |

## 🆘 Obtener Ayuda

1. **GitHub Issues**: https://github.com/PromtEngineer/localGPT/issues
2. **Documentación Original**: README.md
3. **Videos Tutorial**: Ver enlaces en README.md

## 📝 Notas Importantes

- La primera ejecución descarga modelos (~4-7GB)
- El procesamiento inicial puede tomar tiempo
- Los modelos más grandes son más precisos pero requieren más recursos
- Funciona mejor con documentos en inglés (modelos estándar)

---
*¿Problemas con la instalación? Revisa los errores comunes arriba o abre un issue en GitHub.*
