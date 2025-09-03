# MCP System Documentation

## Overview
This repository contains the Model Context Protocol (MCP) system configuration, scripts, and services.

## Directory Structure
- `config/`: Configuration files for all MCPs
- `scripts/`: PowerShell scripts for managing MCP services
- `services/`: MCP service implementations
- `docs/`: System documentation

## Available MCPs
1. Core MCPs:
   - brave-search
   - context7
   - git-tools
   - puppeteer
   - server-filesystem
   - sequential-thinking
   - supabase
   - webresearch
   - time

2. Google MCPs:
   - google-calendar
   - google-gmail
   - google-maps

## Quick Start
1. Ensure you have administrator privileges
2. Configure environment variables in `config/env.json`
3. Run `scripts/start-mcps.ps1` to start all services
4. Use `scripts/stop-mcps.ps1` to stop services

## Port Allocation
- Core MCPs: 55100-55199
- Google MCPs: 55200-55299
- Monitoring: 55900-55999

## Important Paths
- Global MCPs: C:\Users\Hp\mcp-servers
- Google MCPs: C:\Users\Hp\Documents\google-mcps
- Logs: C:\Users\Hp\AppData\Roaming\Claude
