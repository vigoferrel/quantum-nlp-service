# Colores para output
$GREEN = [System.ConsoleColor]::Green
$BLUE = [System.ConsoleColor]::Cyan
$RED = [System.ConsoleColor]::Red

# Función para probar una dimensión específica
function Test-Dimension {
    param (
        [int]$n,
        [string]$symbol
    )
    Write-Host "Probando tensor ${n}x${n}x${n}x${n} para $symbol" -ForegroundColor $BLUE
    
    try {
        $body = @{
            dimensions = @($n, $n, $n, $n)
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "http://localhost:9080/qbtc/tensor-4d/calculate/$symbol" `
            -Method Post `
            -ContentType "application/json" `
            -Body $body

        Write-Host "Respuesta:" -ForegroundColor $GREEN
        $response | ConvertTo-Json -Depth 10 | Write-Host
        
        Write-Host "Métricas:" -ForegroundColor $BLUE
        Write-Host "- Coherencia: $($response.metrics.coherence)"
        Write-Host "- Fidelidad: $($response.metrics.fidelity)"
    }
    catch {
        Write-Host "Error en la petición: $_" -ForegroundColor $RED
    }
    Write-Host ("=" * 50)
}

# Símbolos a probar
$symbols = @("BTCUSDT", "ETHUSDT", "ADAUSDT")

# Dimensiones a probar
$dimensions = @(2, 3, 4, 5, 8)

Write-Host "=== PRUEBAS AUTOMATIZADAS DE TENSORES NXN ===" -ForegroundColor $BLUE
Write-Host "Iniciando pruebas..."

foreach ($symbol in $symbols) {
    Write-Host "`n=== Probando símbolo: $symbol ===" -ForegroundColor $BLUE
    foreach ($n in $dimensions) {
        Test-Dimension -n $n -symbol $symbol
        Start-Sleep -Seconds 1  # Esperar 1 segundo entre pruebas
    }
}

Write-Host "Pruebas completadas" -ForegroundColor $GREEN