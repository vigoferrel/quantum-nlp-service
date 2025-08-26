# 🚀 QBTC SYSTEM LAUNCHER

Sistema de inicialización robusto para el proyecto QBTC con manejo automático de dependencias, ubicación de archivos y servicios.

## 📋 **CARACTERÍSTICAS**

### **✅ Problemas Solucionados:**
- **Ubicación de archivos**: Detección automática de rutas
- **Dependencias**: Instalación automática de paquetes
- **Virtual Environment**: Activación automática
- **Servicios múltiples**: Gestión unificada de procesos
- **Manejo de errores**: Recuperación automática
- **Configuración**: Sistema de configuración persistente

### **🔧 Componentes del Sistema:**
- `start_qbtc_system.py` - Launcher principal
- `install_dependencies.py` - Instalador de dependencias
- `start_qbtc.bat` - Script para Windows
- `start_qbtc.sh` - Script para Linux/Mac
- `qbtc_config.json` - Configuración del sistema

## 🚀 **INICIO RÁPIDO**

### **Windows:**
```bash
# Opción 1: Doble clic en el archivo
start_qbtc.bat

# Opción 2: Desde PowerShell
.\start_qbtc.bat

# Opción 3: Directo con Python
python start_qbtc_system.py
```

### **Linux/Mac:**
```bash
# Opción 1: Script shell
chmod +x start_qbtc.sh
./start_qbtc.sh

# Opción 2: Directo con Python
python3 start_qbtc_system.py
```

## 📁 **ESTRUCTURA DEL PROYECTO**

```
quantum-nlp-service/
├── start_qbtc_system.py          # 🚀 Launcher principal
├── install_dependencies.py       # 📦 Instalador de dependencias
├── start_qbtc.bat               # 🪟 Script Windows
├── start_qbtc.sh                # 🐧 Script Linux/Mac
├── qbtc_config.json             # ⚙️ Configuración
├── .venv/                       # 🐍 Virtual environment
└── localGPT-main/
    └── integrated_llm_system/
        ├── optimal_ui.py        # 🖥️ UI principal
        ├── integrate.py         # 🔧 Sistema integrado
        └── requirements.txt     # 📋 Dependencias
```

## ⚙️ **CONFIGURACIÓN**

El sistema crea automáticamente `qbtc_config.json` con la siguiente estructura:

```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": false
  },
  "ollama": {
    "host": "http://localhost:11434",
    "models": ["llama2", "gemma2", "mistral"]
  },
  "openrouter": {
    "api_key": "tu-api-key-aqui"
  },
  "services": {
    "llm_core": true,
    "web_interface": true,
    "agents": true
  }
}
```

## 🔧 **FUNCIONALIDADES**

### **1. Verificación de Requisitos**
- ✅ Python 3.8+
- ✅ Virtual environment
- ✅ Directorios críticos
- ✅ Dependencias básicas

### **2. Configuración Automática**
- 🔧 Activación de virtual environment
- 📦 Instalación de dependencias
- ⚙️ Configuración de rutas
- 🔍 Verificación de servicios

### **3. Gestión de Servicios**
- 🚀 Servidor LLM principal
- 🧠 Agentes BMAD
- ⚛️ Quantum Core
- 🧠 CIO Brain
- 🌐 API Server

### **4. Monitoreo y Control**
- 📊 Estado en tiempo real
- 🔄 Gestión de procesos
- 🛑 Detención limpia
- 🧹 Limpieza de recursos

## 🎯 **INTERFACES DISPONIBLES**

Una vez iniciado el sistema, accede a:

- **🏠 Página Principal**: http://127.0.0.1:5000
- **💬 Chat Inteligente**: http://127.0.0.1:5000/chat
- **🧠 Agentes BMAD**: http://127.0.0.1:5000/agents
- **🚀 Entrenamiento**: http://127.0.0.1:5000/training
- **📊 Evaluación**: http://127.0.0.1:5000/evaluation
- **🔧 Desarrollo**: http://127.0.0.1:5000/development

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### **Error: "Python no encontrado"**
```bash
# Instalar Python 3.8+ desde python.org
# O usar el gestor de paquetes del sistema
```

### **Error: "Virtual environment no encontrado"**
```bash
# El sistema lo crea automáticamente
# O manualmente:
python -m venv .venv
```

### **Error: "Dependencias faltantes"**
```bash
# Ejecutar manualmente:
python install_dependencies.py
```

### **Error: "Puerto ocupado"**
```bash
# Cambiar puerto en qbtc_config.json
# O detener procesos en el puerto 5000
```

### **Error: "Ollama no disponible"**
```bash
# Instalar Ollama desde ollama.ai
# O deshabilitar en configuración
```

## 🔄 **COMANDOS ÚTILES**

### **Reiniciar sistema:**
```bash
# Detener con Ctrl+C y volver a ejecutar
python start_qbtc_system.py
```

### **Verificar estado:**
```bash
# El sistema muestra estado automáticamente
# O verificar manualmente:
curl http://127.0.0.1:5000
```

### **Limpiar instalación:**
```bash
# Eliminar virtual environment
rm -rf .venv
# Recrear desde cero
python start_qbtc_system.py
```

## 📊 **LOGS Y MONITOREO**

El sistema genera logs automáticamente:
- ✅ Estado de servicios
- ⚠️ Advertencias
- ❌ Errores
- 🔄 Procesos activos

## 🎉 **¡LISTO PARA USAR!**

Con este sistema de inicialización robusto, ya no tendrás problemas de:
- ❌ Ubicación de archivos
- ❌ Dependencias faltantes
- ❌ Virtual environment
- ❌ Configuración manual
- ❌ Gestión de procesos

¡Simplemente ejecuta `start_qbtc.bat` (Windows) o `./start_qbtc.sh` (Linux/Mac) y todo funcionará automáticamente! 🚀
