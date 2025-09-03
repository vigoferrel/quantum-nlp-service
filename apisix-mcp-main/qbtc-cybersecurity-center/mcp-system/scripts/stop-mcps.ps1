# Stop-MCPs.ps1
# Script to stop all MCP services

$ErrorActionPreference = "Stop"
$configPath = Join-Path $PSScriptRoot "..\config\mcp-ports.json"
$ports = Get-Content $configPath | ConvertFrom-Json

function Stop-ProcessesByPort {
    param($port)
    $processId = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | 
                Select-Object -ExpandProperty OwningProcess
    if ($processId) {
        Write-Host "Stopping process on port $port (PID: $processId)"
        Stop-Process -Id $processId -Force
    }
}

Write-Host "Stopping MCP System..."

# Stop all processes on configured ports
$allPorts = @($ports.core_mcps.PSObject.Properties.Value) + 
            @($ports.google_mcps.PSObject.Properties.Value) + 
            @($ports.monitoring.PSObject.Properties.Value)

foreach ($port in $allPorts) {
    Stop-ProcessesByPort $port
}

Write-Host "All MCP services stopped successfully!"
