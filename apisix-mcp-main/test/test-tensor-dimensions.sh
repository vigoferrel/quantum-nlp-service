#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Función para probar una dimensión específica
test_dimension() {
    local n=$1
    local symbol=$2
    echo -e "${BLUE}Probando tensor ${n}x${n}x${n}x${n} para $symbol${NC}"
    
    response=$(curl -s -X POST "http://localhost:9080/qbtc/tensor-4d/calculate/$symbol" \
        -H "Content-Type: application/json" \
        -d "{\"dimensions\":[$n,$n,$n,$n]}")
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Respuesta:${NC}"
        echo "$response" | python -m json.tool
        
        # Extraer métricas importantes
        coherence=$(echo "$response" | grep -o '"coherence":[0-9.]*' | cut -d':' -f2)
        fidelity=$(echo "$response" | grep -o '"fidelity":[0-9.]*' | cut -d':' -f2)
        
        echo -e "${BLUE}Métricas:${NC}"
        echo "- Coherencia: $coherence"
        echo "- Fidelidad: $fidelity"
    else
        echo -e "${RED}Error en la petición${NC}"
    fi
    echo "----------------------------------------"
}

# Símbolos a probar
symbols=("BTCUSDT" "ETHUSDT" "ADAUSDT")

# Dimensiones a probar
dimensions=(2 3 4 5 8)

echo "=== PRUEBAS AUTOMATIZADAS DE TENSORES NXN ==="
echo "Iniciando pruebas..."

for symbol in "${symbols[@]}"; do
    echo -e "\n${BLUE}=== Probando símbolo: $symbol ===${NC}"
    for n in "${dimensions[@]}"; do
        test_dimension $n $symbol
        sleep 1  # Esperar 1 segundo entre pruebas
    done
done

echo -e "${GREEN}Pruebas completadas${NC}"