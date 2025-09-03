# MCP System Quick Start Guide

## Prerequisites
- Node.js and npm installed
- PowerShell with Administrator privileges
- Required API keys and credentials

## Environment Setup
1. Copy your Google credentials to `config/google_credentials.json`
2. Set up environment variables in `config/env.json`
3. Ensure all ports in range 55000-55999 are available

## Starting the System
1. Open PowerShell as Administrator
2. Navigate to the mcp-system directory
3. Run `.\scripts\start-mcps.ps1`
4. Check the console output for service status

## Stopping the System
1. Open PowerShell as Administrator
2. Navigate to the mcp-system directory
3. Run `.\scripts\stop-mcps.ps1`

## Verifying Installation
Run these commands to verify installation:
```powershell
mcp-git-tools --help
mcp-brave-search --version
mcp-time --help
```

## Troubleshooting
1. Port conflicts:
   - Check `netstat -ano | findstr "55"`
   - Kill any processes using required ports

2. Module errors:
   - Run `npm install` in the services directory
   - Check Node.js version (recommended: latest LTS)

3. Permission issues:
   - Ensure PowerShell is running as Administrator
   - Check file permissions in service directories

## Logging
- All logs are stored in `C:\Users\Hp\AppData\Roaming\Claude`
- Each MCP has its own log file
- Monitor `mcp-system.log` for system-wide issues
