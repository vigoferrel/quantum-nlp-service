# Stop any existing server process
$p = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*flask_app_fast.py*' }
if ($null -ne $p) {
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    Write-Output "Stopped existing server process (PID: $($p.ProcessId))"
} else {
    Write-Output "No existing server process found."
}

# Wait a moment
Start-Sleep -Seconds 1

# Ensure logs directory exists
if (-not (Test-Path -Path 'logs')) {
    New-Item -ItemType Directory -Path 'logs' | Out-Null
}

# Start the new server process in the background, with logging
Write-Output "Starting new server process in the background..."
Start-Process python -ArgumentList '-u','flask_app_fast.py' -RedirectStandardOutput logs/flask_fast.out.log -RedirectStandardError logs/flask_fast.err.log -WindowStyle Hidden

# Wait and verify
Start-Sleep -Seconds 3
$r = try {
    (Invoke-WebRequest -Uri http://127.0.0.1:5000/health -UseBasicParsing).Content
} catch {
    $_.Exception.Message
}

if ($r -like '*{*healthy*}*') {
    Write-Host "✅ Server restarted successfully and is healthy."
    $r
} else {
    Write-Host "❌ Server failed to start. See logs for details."
    Get-Content logs/flask_fast.err.log -Tail 20
}

