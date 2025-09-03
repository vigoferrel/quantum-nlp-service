# Start-MCPs.ps1
# Script to start all MCP services with proper port allocation

$ErrorActionPreference = "Stop"
$configPath = Join-Path $PSScriptRoot "..\config\mcp-ports.json"
$ports = Get-Content $configPath | ConvertFrom-Json

function Test-PortAvailable {
    param($port)
    $listener = $null
    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, $port)
        $listener.Start()
        return $true
    }
    catch {
        return $false
    }
    finally {
        if ($listener) {
            $listener.Stop()
        }
    }
}

function Start-MonitoringServices {
    Write-Host "Starting monitoring services..."
    # Add monitoring service startup logic here
}

function Start-GoogleMCPs {
    Write-Host "Starting Google MCPs..."
    $env:CALENDAR_PORT = $ports.google_mcps.calendar
    $env:GMAIL_PORT = $ports.google_mcps.gmail
    $env:MAPS_PORT = $ports.google_mcps.maps
    
    Start-Process pwsh -ArgumentList "-File `"$PSScriptRoot\..\services\google-calendar\server.js`"" -NoNewWindow
    Start-Sleep -Seconds 2
    Start-Process pwsh -ArgumentList "-File `"$PSScriptRoot\..\services\google-gmail\server.js`"" -NoNewWindow
    Start-Sleep -Seconds 2
    Start-Process pwsh -ArgumentList "-File `"$PSScriptRoot\..\services\google-maps\server.js`"" -NoNewWindow
}

function Start-CoreMCPs {
    Write-Host "Starting Core MCPs..."
    mcp-brave-search --port $ports.core_mcps.brave_search
    Start-Sleep -Seconds 1
    mcp-git-tools --port $ports.core_mcps.git_tools
    Start-Sleep -Seconds 1
    # Add other core MCPs here
}

# Main execution
Write-Host "Starting MCP System..."

# Check ports
$allPorts = @($ports.core_mcps.PSObject.Properties.Value) + 
            @($ports.google_mcps.PSObject.Properties.Value) + 
            @($ports.monitoring.PSObject.Properties.Value)

foreach ($port in $allPorts) {
    if (-not (Test-PortAvailable $port)) {
        Write-Error "Port $port is not available. Please check for conflicting processes."
        exit 1
    }
}

# Start services in order
Start-MonitoringServices
Start-Sleep -Seconds 2
Start-GoogleMCPs
Start-Sleep -Seconds 2
Start-CoreMCPs

Write-Host "All MCP services started successfully!"
Write-Host "Monitor logs at: C:\Users\Hp\AppData\Roaming\Claude"
