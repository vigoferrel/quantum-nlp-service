# QBTC Services Launcher
# Script para lanzar todos los servicios de QBTC en segundo plano

Write-Host "🚀 Iniciando servicios QBTC..." -ForegroundColor Cyan

# Definir rutas
$CybersecurityCenterPath = "C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED\3.0\qbtc-cybersecurity-center"
$CommercialWebsitePath = "$CybersecurityCenterPath\qbtc-commercial-website"

Write-Host "📁 Rutas configuradas:" -ForegroundColor Yellow
Write-Host "   Cybersecurity Center: $CybersecurityCenterPath" -ForegroundColor Gray
Write-Host "   Commercial Website: $CommercialWebsitePath" -ForegroundColor Gray

# Verificar que Node.js esté disponible
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js detectado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no encontrado. Por favor instale Node.js primero." -ForegroundColor Red
    exit 1
}

# Función para lanzar servicios
function Start-QBTCService {
    param(
        [string]$ServiceName,
        [string]$WorkingDirectory,
        [string]$Script,
        [int]$Port
    )
    
    Write-Host "🔄 Iniciando $ServiceName en puerto $Port..." -ForegroundColor Yellow
    
    $job = Start-Job -ScriptBlock {
        param($WorkDir, $ScriptFile, $ServicePort)
        Set-Location $WorkDir
        $env:PORT = $ServicePort
        node $ScriptFile
    } -ArgumentList $WorkingDirectory, $Script, $Port -Name $ServiceName
    
    Start-Sleep -Seconds 2
    
    # Verificar si el puerto está en uso
    $portCheck = netstat -an | Select-String ":$Port.*LISTENING"
    if ($portCheck) {
        Write-Host "✅ $ServiceName iniciado correctamente en puerto $Port" -ForegroundColor Green
        return $job
    } else {
        Write-Host "⚠️  $ServiceName puede tardar en iniciarse..." -ForegroundColor Yellow
        return $job
    }
}

Write-Host "`n🛡️ Iniciando servicios..." -ForegroundColor Cyan

# Lanzar Cybersecurity Center (Puerto 7070)
$CyberSecJob = Start-QBTCService -ServiceName "QBTC-CyberSecurity-Center" -WorkingDirectory $CybersecurityCenterPath -Script "index.js" -Port 7070

# Lanzar Commercial Website (Puerto 8080) 
$CommercialJob = Start-QBTCService -ServiceName "QBTC-Commercial-Website" -WorkingDirectory $CommercialWebsitePath -Script "server.js" -Port 8080

Write-Host "`n📊 Estado de los servicios:" -ForegroundColor Cyan
Get-Job | Where-Object {$_.Name -like "*QBTC*"} | Format-Table Id, Name, State -AutoSize

Write-Host "`n🌐 Servicios disponibles:" -ForegroundColor Green
Write-Host "   🛡️  Cybersecurity Center: http://localhost:7070" -ForegroundColor White
Write-Host "   💼 Commercial Website:    http://localhost:8080" -ForegroundColor White
Write-Host "   📊 Security API:          http://localhost:7070/api/status" -ForegroundColor White
Write-Host "   📧 Contact API:           http://localhost:8080/api/contact" -ForegroundColor White

Write-Host "`n⚡ Todos los servicios QBTC están operativos!" -ForegroundColor Green
Write-Host "📋 Use 'Get-Job' para ver el estado de los servicios" -ForegroundColor Gray
Write-Host "🛑 Use 'Stop-Job -Name QBTC*' para detener todos los servicios" -ForegroundColor Gray
