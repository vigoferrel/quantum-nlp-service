#!/bin/bash

# Este script se ejecuta DENTRO del contenedor de Docker de SWE-bench.
# Recibe como argumentos el repositorio, la versión y la ruta al parche.

set -e # Termina inmediatamente si un comando falla

REPO_URL=$1
VERSION=$2
PATCH_FILE=$3

echo "--- Iniciando Test de SWE-bench ---"
echo "Repositorio: $REPO_URL"
echo "Version: $VERSION"
echo "Parche: $PATCH_FILE"

# Clona el repositorio
git clone $REPO_URL
cd $(basename "$REPO_URL" .git)

# Checkout a la versión específica
git checkout -f $VERSION

# Instala las dependencias del repositorio
# SWE-bench utiliza conda, por lo que buscamos un environment.yml
if [ -f "environment.yml" ]; then
    echo "Instalando dependencias con Conda..."
    conda env create -f environment.yml
    source activate swe-bench-test
fi

# Aplica el parche
echo "Aplicando parche..."
git apply $PATCH_FILE

# Ejecuta los tests
# El comando de testeo es proporcionado por los metadatos de SWE-bench
# Aquí asumimos que es 'pytest' como un ejemplo común.
echo "Ejecutando tests..."
if pytest; then
    echo "SUCCESS"
else
    echo "FAILURE"
fi

echo "--- Test de SWE-bench finalizado ---"
