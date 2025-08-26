#!/bin/bash

# Script de instalación automática de VIGOLEONROCKS para Ollama
# Versión: 1.0.0
# Autor: VIGOLEONROCKS Team

echo "=========================================="
echo "VIGOLEONROCKS - Instalación Automática"
echo "Modelo Cuántico-Cognitivo para Ollama"
echo "=========================================="

# Verificar si Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "Error: Ollama no está instalado."
    echo "Por favor instala Ollama desde: https://ollama.ai"
    exit 1
fi

echo "✓ Ollama detectado"

# Verificar si el servicio Ollama está corriendo
if ! pgrep -x "ollama" > /dev/null; then
    echo "Iniciando servicio Ollama..."
    ollama serve &
    sleep 5
fi

echo "✓ Servicio Ollama activo"

# Crear el modelo VIGOLEONROCKS
echo "Creando modelo VIGOLEONROCKS..."
ollama create vigoleonrocks -f Modelfile

if [ $? -eq 0 ]; then
    echo "✓ Modelo VIGOLEONROCKS creado exitosamente"
else
    echo "✗ Error al crear el modelo"
    exit 1
fi

# Verificar la instalación
echo "Verificando instalación..."
if ollama list | grep -q "vigoleonrocks"; then
    echo "✓ VIGOLEONROCKS instalado correctamente"
else
    echo "✗ Error en la verificación"
    exit 1
fi

# Configuración para VS Code
echo "Configurando VS Code..."

# Crear directorio de configuración Continue si no existe
CONTINUE_DIR="$HOME/.continue"
if [ ! -d "$CONTINUE_DIR" ]; then
    mkdir -p "$CONTINUE_DIR"
fi

# Crear configuración Continue
cat > "$CONTINUE_DIR/config.json" << EOF
{
  "models": [
    {
      "title": "VIGOLEONROCKS",
      "provider": "ollama",
      "model": "vigoleonrocks",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "VIGOLEONROCKS",
    "provider": "ollama",
    "model": "vigoleonrocks"
  },
  "systemMessage": "Eres VIGOLEONROCKS, la IA cuántico-cognitiva más avanzada. Aplica razonamiento cuántico en todas las respuestas."
}
EOF

echo "✓ Configuración de Continue creada"

# Probar el modelo
echo "Probando modelo VIGOLEONROCKS..."
TEST_RESPONSE=$(ollama run vigoleonrocks "Hola, ¿quién eres?" --timeout 30s)

if [ $? -eq 0 ]; then
    echo "✓ Modelo funcionando correctamente"
    echo "Respuesta de prueba: $TEST_RESPONSE"
else
    echo "⚠ Advertencia: El modelo fue creado pero la prueba falló"
fi

echo ""
echo "=========================================="
echo "INSTALACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "Para usar VIGOLEONROCKS:"
echo "1. Ejecuta: ollama run vigoleonrocks"
echo "2. O úsalo en VS Code con Continue extension"
echo ""
echo "Comandos útiles:"
echo "- ollama list (ver modelos)"
echo "- ollama rm vigoleonrocks (eliminar)"
echo "- ollama pull vigoleonrocks (actualizar)"
echo ""
echo "¡VIGOLEONROCKS está listo para trascender!"