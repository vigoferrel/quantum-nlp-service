# LocalGPT - Instalador Adaptativo

## 🚀 Descripción
LocalGPT es una herramienta de chat local completamente privada que permite hacer preguntas sobre documentos sin conexiones externas.

## 🔧 Instalación

### Requisitos Previos
- Python 3.8+
- pip
- Entorno virtual recomendado

### Pasos de Instalación

1. Clonar o descargar el repositorio
```bash
git clone https://github.com/tu-usuario/localgpt-installer.git
cd localgpt-installer
```

2. Crear entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Ejecutar instalador
```bash
python localgpt_installer.py
```

## 💬 Uso

1. Añadir documentos:
   - Coloca archivos .txt en la carpeta `SOURCE_DOCUMENTS/`

2. Procesar documentos:
```bash
python ingest_adaptive.py
```

3. Iniciar chat:
```bash
python run_adaptive.py
```

## 🎯 Características

- 100% local y privado
- Soporte para múltiples formatos de documento
- Adaptación automática según capacidades del sistema
- Sin conexiones externas

## 🆘 Solución de Problemas

- Asegúrate de tener los permisos necesarios
- Revisa `localgpt_config.json` para detalles de instalación
- Consulta la salida del instalador para información de paquetes

## 📄 Licencia
[Especificar licencia]

## 🤝 Contribuciones
[Información de contribuciones]
