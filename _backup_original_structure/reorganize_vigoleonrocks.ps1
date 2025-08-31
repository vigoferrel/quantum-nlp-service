# VIGOLEONROCKS Architecture Reorganization Script
# Generated automatically by VIGOLEONROCKS Architect Reorganizer

param(
    [switch]$DryRun = $false,
    [switch]$CreateBackup = $true
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = $PSScriptRoot

Write-Host '🚀 Iniciando reorganización de VIGOLEONROCKS...' -ForegroundColor Green

# Crear backup si es necesario
if ($CreateBackup) {
    $BackupDir = Join-Path $ProjectRoot '_backup_original_structure'
    Write-Host '📦 Creando backup...' -ForegroundColor Yellow
    if (Test-Path $BackupDir) { Remove-Item $BackupDir -Recurse -Force }
    New-Item $BackupDir -ItemType Directory -Force | Out-Null
    Get-ChildItem $ProjectRoot -Exclude '_backup_*','_new_optimized_*','.git' | ForEach-Object {
        if ($_.PSIsContainer) {
            Copy-Item $_.FullName -Destination $BackupDir -Recurse -Force
        } else {
            Copy-Item $_.FullName -Destination $BackupDir -Force
        }
    }
}

# Crear estructura objetivo
$NewStructureDir = Join-Path $ProjectRoot '_new_optimized_structure'
if (Test-Path $NewStructureDir) { Remove-Item $NewStructureDir -Recurse -Force }
New-Item $NewStructureDir -ItemType Directory | Out-Null

# Paso 1: Reorganizar componentes de prioridad 1
$src = Join-Path $ProjectRoot '.'
$dst = Join-Path $NewStructureDir 'vigoleonrocks-core\quantum-nlp-service'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: . -> vigoleonrocks-core\quantum-nlp-service' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: quantum-nlp-service' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'localGPT-main'
$dst = Join-Path $NewStructureDir 'application\localGPT-main'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: localGPT-main -> application\localGPT-main' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: localGPT-main' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'mcp\core'
$dst = Join-Path $NewStructureDir 'vigoleonrocks-core\core'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: mcp\core -> vigoleonrocks-core\core' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: core' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'services\quantum-core'
$dst = Join-Path $NewStructureDir 'vigoleonrocks-core\quantum-core'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: services\quantum-core -> vigoleonrocks-core\quantum-core' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: quantum-core' -ForegroundColor Green
    }
}

# Paso 2: Reorganizar componentes de prioridad 2
$src = Join-Path $ProjectRoot 'cache'
$dst = Join-Path $NewStructureDir 'infrastructure\cache'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: cache -> infrastructure\cache' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: cache' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\api'
$dst = Join-Path $NewStructureDir 'interfaces\api'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\api -> interfaces\api' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: api' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\build'
$dst = Join-Path $NewStructureDir 'interfaces\build'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\build -> interfaces\build' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: build' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\preview-deployments'
$dst = Join-Path $NewStructureDir 'interfaces\preview-deployments'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\preview-deployments -> interfaces\preview-deployments' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: preview-deployments' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\api'
$dst = Join-Path $NewStructureDir 'interfaces\api'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\api -> interfaces\api' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: api' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\ui'
$dst = Join-Path $NewStructureDir 'interfaces\ui'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\ui -> interfaces\ui' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ui' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api'
$dst = Join-Path $NewStructureDir 'interfaces\api'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api -> interfaces\api' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: api' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\api'
$dst = Join-Path $NewStructureDir 'interfaces\api'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\api -> interfaces\api' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: api' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\api\routers'
$dst = Join-Path $NewStructureDir 'interfaces\routers'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\api\routers -> interfaces\routers' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: routers' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\templates'
$dst = Join-Path $NewStructureDir 'interfaces\templates'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\templates -> interfaces\templates' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: templates' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\templates'
$dst = Join-Path $NewStructureDir 'interfaces\templates'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\templates -> interfaces\templates' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: templates' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\monitoring\database'
$dst = Join-Path $NewStructureDir 'infrastructure\database'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\monitoring\database -> infrastructure\database' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: database' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\templates'
$dst = Join-Path $NewStructureDir 'interfaces\templates'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\templates -> interfaces\templates' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: templates' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\builders'
$dst = Join-Path $NewStructureDir 'interfaces\builders'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\builders -> interfaces\builders' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: builders' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\databases'
$dst = Join-Path $NewStructureDir 'infrastructure\databases'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\databases -> infrastructure\databases' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: databases' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'openvpn-gui-master'
$dst = Join-Path $NewStructureDir 'interfaces\openvpn-gui-master'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: openvpn-gui-master -> interfaces\openvpn-gui-master' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: openvpn-gui-master' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'services\api-gateway'
$dst = Join-Path $NewStructureDir 'interfaces\api-gateway'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: services\api-gateway -> interfaces\api-gateway' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: api-gateway' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'services\cache'
$dst = Join-Path $NewStructureDir 'infrastructure\cache'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: services\cache -> infrastructure\cache' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: cache' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'services\database'
$dst = Join-Path $NewStructureDir 'infrastructure\database'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: services\database -> infrastructure\database' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: database' -ForegroundColor Green
    }
}

# Paso 3: Reorganizar componentes de prioridad 3
$src = Join-Path $ProjectRoot 'config'
$dst = Join-Path $NewStructureDir 'config\config'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: config -> config\config' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: config' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary'
$dst = Join-Path $NewStructureDir 'application\dokploy-canary'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary -> application\dokploy-canary' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: dokploy-canary' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\.vscode'
$dst = Join-Path $NewStructureDir 'application\.vscode'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\.vscode -> application\.vscode' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: .vscode' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\api\src'
$dst = Join-Path $NewStructureDir 'application\src'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\api\src -> application\src' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: src' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy'
$dst = Join-Path $NewStructureDir 'application\dokploy'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy -> application\dokploy' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: dokploy' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard'
$dst = Join-Path $NewStructureDir 'application\dashboard'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard -> application\dashboard' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: dashboard' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application'
$dst = Join-Path $NewStructureDir 'application\application'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application -> application\application' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: application' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced'
$dst = Join-Path $NewStructureDir 'application\advanced'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced -> application\advanced' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: advanced' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\cluster'
$dst = Join-Path $NewStructureDir 'application\cluster'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\cluster -> application\cluster' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: cluster' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\import'
$dst = Join-Path $NewStructureDir 'application\import'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\import -> application\import' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: import' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\ports'
$dst = Join-Path $NewStructureDir 'application\ports'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\ports -> application\ports' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ports' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\redirects'
$dst = Join-Path $NewStructureDir 'application\redirects'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\redirects -> application\redirects' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: redirects' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\security'
$dst = Join-Path $NewStructureDir 'security\security'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\security -> security\security' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: security' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\traefik'
$dst = Join-Path $NewStructureDir 'application\traefik'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\traefik -> application\traefik' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: traefik' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\advanced\volumes'
$dst = Join-Path $NewStructureDir 'application\volumes'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\advanced\volumes -> application\volumes' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: volumes' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\deployments'
$dst = Join-Path $NewStructureDir 'deployment\deployments'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\deployments -> deployment\deployments' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: deployments' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\domains'
$dst = Join-Path $NewStructureDir 'domain\domains'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\domains -> domain\domains' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: domains' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\environment'
$dst = Join-Path $NewStructureDir 'config\environment'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\environment -> config\environment' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: environment' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\general\generic'
$dst = Join-Path $NewStructureDir 'application\generic'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\general\generic -> application\generic' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: generic' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\logs'
$dst = Join-Path $NewStructureDir 'application\logs'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\logs -> application\logs' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: logs' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\rollbacks'
$dst = Join-Path $NewStructureDir 'application\rollbacks'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\rollbacks -> application\rollbacks' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: rollbacks' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\schedules'
$dst = Join-Path $NewStructureDir 'application\schedules'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\schedules -> application\schedules' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: schedules' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\application\volume-backups'
$dst = Join-Path $NewStructureDir 'application\volume-backups'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\application\volume-backups -> application\volume-backups' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: volume-backups' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\compose'
$dst = Join-Path $NewStructureDir 'application\compose'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\compose -> application\compose' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: compose' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\compose\advanced'
$dst = Join-Path $NewStructureDir 'application\advanced'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\compose\advanced -> application\advanced' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: advanced' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\compose\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\compose\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\compose\general\generic'
$dst = Join-Path $NewStructureDir 'application\generic'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\compose\general\generic -> application\generic' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: generic' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\compose\logs'
$dst = Join-Path $NewStructureDir 'application\logs'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\compose\logs -> application\logs' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: logs' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\database\backups'
$dst = Join-Path $NewStructureDir 'application\backups'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\database\backups -> application\backups' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: backups' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\docker\config'
$dst = Join-Path $NewStructureDir 'config\config'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\docker\config -> config\config' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: config' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\docker\logs'
$dst = Join-Path $NewStructureDir 'application\logs'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\docker\logs -> application\logs' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: logs' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\docker\show'
$dst = Join-Path $NewStructureDir 'application\show'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\docker\show -> application\show' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: show' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\docker\terminal'
$dst = Join-Path $NewStructureDir 'application\terminal'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\docker\terminal -> application\terminal' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: terminal' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\file-system'
$dst = Join-Path $NewStructureDir 'application\file-system'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\file-system -> application\file-system' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: file-system' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\impersonation'
$dst = Join-Path $NewStructureDir 'application\impersonation'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\impersonation -> application\impersonation' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: impersonation' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\mariadb'
$dst = Join-Path $NewStructureDir 'application\mariadb'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\mariadb -> application\mariadb' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: mariadb' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\mariadb\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\mariadb\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\mongo'
$dst = Join-Path $NewStructureDir 'application\mongo'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\mongo -> application\mongo' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: mongo' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\mongo\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\mongo\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\monitoring\free\container'
$dst = Join-Path $NewStructureDir 'application\container'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\monitoring\free\container -> application\container' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: container' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\monitoring\paid\container'
$dst = Join-Path $NewStructureDir 'application\container'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\monitoring\paid\container -> application\container' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: container' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\monitoring\paid\servers'
$dst = Join-Path $NewStructureDir 'application\servers'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\monitoring\paid\servers -> application\servers' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: servers' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\mysql'
$dst = Join-Path $NewStructureDir 'application\mysql'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\mysql -> application\mysql' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: mysql' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\mysql\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\mysql\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\organization'
$dst = Join-Path $NewStructureDir 'application\organization'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\organization -> application\organization' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: organization' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\postgres'
$dst = Join-Path $NewStructureDir 'application\postgres'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\postgres -> application\postgres' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: postgres' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\postgres\advanced'
$dst = Join-Path $NewStructureDir 'application\advanced'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\postgres\advanced -> application\advanced' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: advanced' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\postgres\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\postgres\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\project'
$dst = Join-Path $NewStructureDir 'application\project'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\project -> application\project' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: project' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\project\ai'
$dst = Join-Path $NewStructureDir 'application\ai'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\project\ai -> application\ai' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ai' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\projects'
$dst = Join-Path $NewStructureDir 'application\projects'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\projects -> application\projects' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: projects' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\redis'
$dst = Join-Path $NewStructureDir 'application\redis'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\redis -> application\redis' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: redis' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\redis\general'
$dst = Join-Path $NewStructureDir 'application\general'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\redis\general -> application\general' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: general' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\requests'
$dst = Join-Path $NewStructureDir 'application\requests'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\requests -> application\requests' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: requests' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings'
$dst = Join-Path $NewStructureDir 'config\settings'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings -> config\settings' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: settings' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\billing'
$dst = Join-Path $NewStructureDir 'application\billing'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\billing -> application\billing' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: billing' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\certificates'
$dst = Join-Path $NewStructureDir 'application\certificates'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\certificates -> application\certificates' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: certificates' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\nodes'
$dst = Join-Path $NewStructureDir 'application\nodes'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\nodes -> application\nodes' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: nodes' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\nodes\manager'
$dst = Join-Path $NewStructureDir 'domain\manager'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\nodes\manager -> domain\manager' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: manager' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\nodes\workers'
$dst = Join-Path $NewStructureDir 'application\workers'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\nodes\workers -> application\workers' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: workers' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\registry'
$dst = Join-Path $NewStructureDir 'application\registry'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\cluster\registry -> application\registry' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: registry' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\destination'
$dst = Join-Path $NewStructureDir 'application\destination'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\destination -> application\destination' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: destination' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\git'
$dst = Join-Path $NewStructureDir 'application\git'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\git -> application\git' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: git' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\git\bitbucket'
$dst = Join-Path $NewStructureDir 'application\bitbucket'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\git\bitbucket -> application\bitbucket' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: bitbucket' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\git\gitea'
$dst = Join-Path $NewStructureDir 'application\gitea'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\git\gitea -> application\gitea' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: gitea' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\git\github'
$dst = Join-Path $NewStructureDir 'application\github'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\git\github -> application\github' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: github' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\git\gitlab'
$dst = Join-Path $NewStructureDir 'application\gitlab'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\git\gitlab -> application\gitlab' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: gitlab' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\notifications'
$dst = Join-Path $NewStructureDir 'application\notifications'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\notifications -> application\notifications' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: notifications' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\profile'
$dst = Join-Path $NewStructureDir 'application\profile'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\profile -> application\profile' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: profile' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\servers'
$dst = Join-Path $NewStructureDir 'application\servers'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\servers -> application\servers' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: servers' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\servers\actions'
$dst = Join-Path $NewStructureDir 'application\actions'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\servers\actions -> application\actions' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: actions' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\servers\welcome-stripe'
$dst = Join-Path $NewStructureDir 'application\welcome-stripe'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\servers\welcome-stripe -> application\welcome-stripe' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: welcome-stripe' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\ssh-keys'
$dst = Join-Path $NewStructureDir 'security\ssh-keys'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\ssh-keys -> security\ssh-keys' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ssh-keys' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\users'
$dst = Join-Path $NewStructureDir 'application\users'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\users -> application\users' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: users' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\settings\web-server'
$dst = Join-Path $NewStructureDir 'application\web-server'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\settings\web-server -> application\web-server' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: web-server' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\shared'
$dst = Join-Path $NewStructureDir 'application\shared'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\shared -> application\shared' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: shared' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\swarm'
$dst = Join-Path $NewStructureDir 'application\swarm'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\swarm -> application\swarm' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: swarm' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\swarm\applications'
$dst = Join-Path $NewStructureDir 'application\applications'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\swarm\applications -> application\applications' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: applications' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\dashboard\swarm\details'
$dst = Join-Path $NewStructureDir 'application\details'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\dashboard\swarm\details -> application\details' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: details' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\icons'
$dst = Join-Path $NewStructureDir 'application\icons'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\icons -> application\icons' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: icons' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\layouts'
$dst = Join-Path $NewStructureDir 'application\layouts'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\layouts -> application\layouts' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: layouts' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\components\shared'
$dst = Join-Path $NewStructureDir 'application\shared'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\components\shared -> application\shared' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: shared' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\drizzle'
$dst = Join-Path $NewStructureDir 'application\drizzle'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\drizzle -> application\drizzle' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: drizzle' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\drizzle\meta'
$dst = Join-Path $NewStructureDir 'application\meta'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\drizzle\meta -> application\meta' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: meta' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\hooks'
$dst = Join-Path $NewStructureDir 'application\hooks'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\hooks -> application\hooks' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: hooks' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\lib'
$dst = Join-Path $NewStructureDir 'application\lib'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\lib -> application\lib' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: lib' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages'
$dst = Join-Path $NewStructureDir 'application\pages'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages -> application\pages' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: pages' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\accept-invitation'
$dst = Join-Path $NewStructureDir 'application\accept-invitation'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\accept-invitation -> application\accept-invitation' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: accept-invitation' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\auth'
$dst = Join-Path $NewStructureDir 'security\auth'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\auth -> security\auth' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: auth' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\deploy'
$dst = Join-Path $NewStructureDir 'deployment\deploy'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\deploy -> deployment\deploy' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: deploy' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\deploy\compose'
$dst = Join-Path $NewStructureDir 'application\compose'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\deploy\compose -> application\compose' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: compose' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\providers\gitea'
$dst = Join-Path $NewStructureDir 'application\gitea'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\providers\gitea -> application\gitea' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: gitea' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\providers\github'
$dst = Join-Path $NewStructureDir 'application\github'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\providers\github -> application\github' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: github' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\providers\gitlab'
$dst = Join-Path $NewStructureDir 'application\gitlab'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\providers\gitlab -> application\gitlab' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: gitlab' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\stripe'
$dst = Join-Path $NewStructureDir 'application\stripe'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\stripe -> application\stripe' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: stripe' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\api\trpc'
$dst = Join-Path $NewStructureDir 'application\trpc'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\api\trpc -> application\trpc' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: trpc' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard'
$dst = Join-Path $NewStructureDir 'application\dashboard'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard -> application\dashboard' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: dashboard' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project'
$dst = Join-Path $NewStructureDir 'application\project'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project -> application\project' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: project' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\application'
$dst = Join-Path $NewStructureDir 'application\application'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\application -> application\application' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: application' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\compose'
$dst = Join-Path $NewStructureDir 'application\compose'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\compose -> application\compose' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: compose' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\mariadb'
$dst = Join-Path $NewStructureDir 'application\mariadb'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\mariadb -> application\mariadb' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: mariadb' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\mongo'
$dst = Join-Path $NewStructureDir 'application\mongo'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\mongo -> application\mongo' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: mongo' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\mysql'
$dst = Join-Path $NewStructureDir 'application\mysql'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\mysql -> application\mysql' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: mysql' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\postgres'
$dst = Join-Path $NewStructureDir 'application\postgres'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\postgres -> application\postgres' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: postgres' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\redis'
$dst = Join-Path $NewStructureDir 'application\redis'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\project\[projectId]\services\redis -> application\redis' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: redis' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\pages\dashboard\settings'
$dst = Join-Path $NewStructureDir 'config\settings'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\pages\dashboard\settings -> config\settings' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: settings' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public'
$dst = Join-Path $NewStructureDir 'application\public'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public -> application\public' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: public' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\avatars'
$dst = Join-Path $NewStructureDir 'application\avatars'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\avatars -> application\avatars' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: avatars' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\images'
$dst = Join-Path $NewStructureDir 'application\images'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\images -> application\images' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: images' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\az'
$dst = Join-Path $NewStructureDir 'application\az'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\az -> application\az' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: az' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\de'
$dst = Join-Path $NewStructureDir 'application\de'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\de -> application\de' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: de' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\en'
$dst = Join-Path $NewStructureDir 'application\en'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\en -> application\en' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: en' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\es'
$dst = Join-Path $NewStructureDir 'application\es'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\es -> application\es' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: es' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\fa'
$dst = Join-Path $NewStructureDir 'application\fa'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\fa -> application\fa' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: fa' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\fr'
$dst = Join-Path $NewStructureDir 'application\fr'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\fr -> application\fr' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: fr' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\id'
$dst = Join-Path $NewStructureDir 'application\id'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\id -> application\id' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: id' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\it'
$dst = Join-Path $NewStructureDir 'application\it'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\it -> application\it' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: it' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\ja'
$dst = Join-Path $NewStructureDir 'application\ja'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\ja -> application\ja' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ja' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\ko'
$dst = Join-Path $NewStructureDir 'application\ko'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\ko -> application\ko' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ko' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\kz'
$dst = Join-Path $NewStructureDir 'application\kz'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\kz -> application\kz' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: kz' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\ml'
$dst = Join-Path $NewStructureDir 'application\ml'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\ml -> application\ml' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ml' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\nl'
$dst = Join-Path $NewStructureDir 'application\nl'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\nl -> application\nl' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: nl' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\no'
$dst = Join-Path $NewStructureDir 'application\no'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\no -> application\no' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: no' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\pl'
$dst = Join-Path $NewStructureDir 'application\pl'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\pl -> application\pl' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: pl' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\pt-br'
$dst = Join-Path $NewStructureDir 'application\pt-br'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\pt-br -> application\pt-br' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: pt-br' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\ru'
$dst = Join-Path $NewStructureDir 'application\ru'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\ru -> application\ru' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ru' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\tr'
$dst = Join-Path $NewStructureDir 'application\tr'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\tr -> application\tr' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: tr' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\uk'
$dst = Join-Path $NewStructureDir 'application\uk'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\uk -> application\uk' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: uk' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\zh-Hans'
$dst = Join-Path $NewStructureDir 'application\zh-Hans'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\zh-Hans -> application\zh-Hans' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: zh-Hans' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\public\locales\zh-Hant'
$dst = Join-Path $NewStructureDir 'application\zh-Hant'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\public\locales\zh-Hant -> application\zh-Hant' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: zh-Hant' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server'
$dst = Join-Path $NewStructureDir 'application\server'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server -> application\server' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: server' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\db'
$dst = Join-Path $NewStructureDir 'application\db'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\db -> application\db' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: db' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\db\schema'
$dst = Join-Path $NewStructureDir 'application\schema'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\db\schema -> application\schema' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: schema' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\db\validations'
$dst = Join-Path $NewStructureDir 'application\validations'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\db\validations -> application\validations' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: validations' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\queues'
$dst = Join-Path $NewStructureDir 'application\queues'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\queues -> application\queues' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: queues' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\utils'
$dst = Join-Path $NewStructureDir 'tools\utils'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\utils -> tools\utils' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: utils' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\server\wss'
$dst = Join-Path $NewStructureDir 'application\wss'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\server\wss -> application\wss' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: wss' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\styles'
$dst = Join-Path $NewStructureDir 'application\styles'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\styles -> application\styles' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: styles' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\templates\utils'
$dst = Join-Path $NewStructureDir 'tools\utils'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\templates\utils -> tools\utils' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: utils' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\types'
$dst = Join-Path $NewStructureDir 'application\types'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\types -> application\types' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: types' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\utils'
$dst = Join-Path $NewStructureDir 'tools\utils'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\utils -> tools\utils' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: utils' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\utils\hooks'
$dst = Join-Path $NewStructureDir 'application\hooks'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\utils\hooks -> application\hooks' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: hooks' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\compose'
$dst = Join-Path $NewStructureDir 'application\compose'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\compose -> application\compose' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: compose' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\compose\config'
$dst = Join-Path $NewStructureDir 'config\config'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\compose\config -> config\config' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: config' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\compose\domain'
$dst = Join-Path $NewStructureDir 'domain\domain'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\compose\domain -> domain\domain' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: domain' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\compose\network'
$dst = Join-Path $NewStructureDir 'application\network'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\compose\network -> application\network' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: network' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\compose\secrets'
$dst = Join-Path $NewStructureDir 'application\secrets'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\compose\secrets -> application\secrets' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: secrets' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\compose\service'
$dst = Join-Path $NewStructureDir 'domain\service'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\compose\service -> domain\service' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: service' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\compose\volume'
$dst = Join-Path $NewStructureDir 'application\volume'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\compose\volume -> application\volume' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: volume' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\deploy'
$dst = Join-Path $NewStructureDir 'deployment\deploy'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\deploy -> deployment\deploy' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: deploy' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\drop'
$dst = Join-Path $NewStructureDir 'application\drop'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\drop -> application\drop' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: drop' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\drop\zips'
$dst = Join-Path $NewStructureDir 'application\zips'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\drop\zips -> application\zips' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: zips' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\drop\zips\folder1'
$dst = Join-Path $NewStructureDir 'application\folder1'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\drop\zips\folder1 -> application\folder1' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: folder1' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\drop\zips\folder2'
$dst = Join-Path $NewStructureDir 'application\folder2'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\drop\zips\folder2 -> application\folder2' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: folder2' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\drop\zips\folder3'
$dst = Join-Path $NewStructureDir 'application\folder3'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\drop\zips\folder3 -> application\folder3' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: folder3' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\env'
$dst = Join-Path $NewStructureDir 'config\env'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\env -> config\env' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: env' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\requests'
$dst = Join-Path $NewStructureDir 'application\requests'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\requests -> application\requests' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: requests' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\traefik'
$dst = Join-Path $NewStructureDir 'application\traefik'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\traefik -> application\traefik' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: traefik' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\traefik\server'
$dst = Join-Path $NewStructureDir 'application\server'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\traefik\server -> application\server' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: server' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__\utils'
$dst = Join-Path $NewStructureDir 'tools\utils'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__\utils -> tools\utils' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: utils' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\monitoring'
$dst = Join-Path $NewStructureDir 'application\monitoring'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\monitoring -> application\monitoring' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: monitoring' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\monitoring\config'
$dst = Join-Path $NewStructureDir 'config\config'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\monitoring\config -> config\config' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: config' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\monitoring\containers'
$dst = Join-Path $NewStructureDir 'application\containers'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\monitoring\containers -> application\containers' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: containers' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\monitoring\middleware'
$dst = Join-Path $NewStructureDir 'application\middleware'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\monitoring\middleware -> application\middleware' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: middleware' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\monitoring\monitoring'
$dst = Join-Path $NewStructureDir 'application\monitoring'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\monitoring\monitoring -> application\monitoring' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: monitoring' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\schedules'
$dst = Join-Path $NewStructureDir 'application\schedules'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\schedules -> application\schedules' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: schedules' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\schedules\src'
$dst = Join-Path $NewStructureDir 'application\src'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\schedules\src -> application\src' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: src' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server'
$dst = Join-Path $NewStructureDir 'application\server'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server -> application\server' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: server' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\scripts'
$dst = Join-Path $NewStructureDir 'tools\scripts'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\scripts -> tools\scripts' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: scripts' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src'
$dst = Join-Path $NewStructureDir 'application\src'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src -> application\src' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: src' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\auth'
$dst = Join-Path $NewStructureDir 'security\auth'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\auth -> security\auth' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: auth' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\constants'
$dst = Join-Path $NewStructureDir 'application\constants'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\constants -> application\constants' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: constants' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\db'
$dst = Join-Path $NewStructureDir 'application\db'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\db -> application\db' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: db' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\db\schema'
$dst = Join-Path $NewStructureDir 'application\schema'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\db\schema -> application\schema' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: schema' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\db\validations'
$dst = Join-Path $NewStructureDir 'application\validations'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\db\validations -> application\validations' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: validations' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\emails'
$dst = Join-Path $NewStructureDir 'application\emails'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\emails -> application\emails' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: emails' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\emails\emails'
$dst = Join-Path $NewStructureDir 'application\emails'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\emails\emails -> application\emails' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: emails' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\emails\emails\static'
$dst = Join-Path $NewStructureDir 'application\static'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\emails\emails\static -> application\static' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: static' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\lib'
$dst = Join-Path $NewStructureDir 'application\lib'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\lib -> application\lib' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: lib' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\monitoring'
$dst = Join-Path $NewStructureDir 'application\monitoring'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\monitoring -> application\monitoring' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: monitoring' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\services'
$dst = Join-Path $NewStructureDir 'domain\services'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\services -> domain\services' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: services' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\setup'
$dst = Join-Path $NewStructureDir 'application\setup'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\setup -> application\setup' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: setup' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\types'
$dst = Join-Path $NewStructureDir 'application\types'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\types -> application\types' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: types' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils'
$dst = Join-Path $NewStructureDir 'tools\utils'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils -> tools\utils' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: utils' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\access-log'
$dst = Join-Path $NewStructureDir 'application\access-log'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\access-log -> application\access-log' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: access-log' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\ai'
$dst = Join-Path $NewStructureDir 'application\ai'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\ai -> application\ai' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: ai' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\backups'
$dst = Join-Path $NewStructureDir 'application\backups'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\backups -> application\backups' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: backups' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\cluster'
$dst = Join-Path $NewStructureDir 'application\cluster'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\cluster -> application\cluster' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: cluster' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\docker\collision'
$dst = Join-Path $NewStructureDir 'application\collision'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\docker\collision -> application\collision' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: collision' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\docker\compose'
$dst = Join-Path $NewStructureDir 'application\compose'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\docker\compose -> application\compose' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: compose' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\filesystem'
$dst = Join-Path $NewStructureDir 'application\filesystem'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\filesystem -> application\filesystem' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: filesystem' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\notifications'
$dst = Join-Path $NewStructureDir 'application\notifications'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\notifications -> application\notifications' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: notifications' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\process'
$dst = Join-Path $NewStructureDir 'application\process'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\process -> application\process' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: process' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\providers'
$dst = Join-Path $NewStructureDir 'integrations\providers'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\providers -> integrations\providers' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: providers' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\restore'
$dst = Join-Path $NewStructureDir 'application\restore'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\restore -> application\restore' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: restore' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\schedules'
$dst = Join-Path $NewStructureDir 'application\schedules'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\schedules -> application\schedules' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: schedules' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\servers'
$dst = Join-Path $NewStructureDir 'application\servers'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\servers -> application\servers' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: servers' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\traefik'
$dst = Join-Path $NewStructureDir 'application\traefik'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\traefik -> application\traefik' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: traefik' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\volume-backups'
$dst = Join-Path $NewStructureDir 'application\volume-backups'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\volume-backups -> application\volume-backups' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: volume-backups' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\watch-paths'
$dst = Join-Path $NewStructureDir 'application\watch-paths'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\watch-paths -> application\watch-paths' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: watch-paths' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\verification'
$dst = Join-Path $NewStructureDir 'application\verification'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\verification -> application\verification' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: verification' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\wss'
$dst = Join-Path $NewStructureDir 'application\wss'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\wss -> application\wss' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: wss' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'localGPT-main\WebAgent_Santuario'
$dst = Join-Path $NewStructureDir 'application\WebAgent_Santuario'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: localGPT-main\WebAgent_Santuario -> application\WebAgent_Santuario' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: WebAgent_Santuario' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'localGPT-main\WebAgent_Santuario\unified_chroma_db'
$dst = Join-Path $NewStructureDir 'application\unified_chroma_db'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: localGPT-main\WebAgent_Santuario\unified_chroma_db -> application\unified_chroma_db' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: unified_chroma_db' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'mcp'
$dst = Join-Path $NewStructureDir 'application\mcp'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: mcp -> application\mcp' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: mcp' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'mcp\config'
$dst = Join-Path $NewStructureDir 'config\config'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: mcp\config -> config\config' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: config' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'mcp\exports'
$dst = Join-Path $NewStructureDir 'application\exports'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: mcp\exports -> application\exports' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: exports' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'mcp\services'
$dst = Join-Path $NewStructureDir 'domain\services'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: mcp\services -> domain\services' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: services' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'openvpn-gui-master\plap'
$dst = Join-Path $NewStructureDir 'application\plap'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: openvpn-gui-master\plap -> application\plap' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: plap' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'openvpn-gui-master\qrcodegen'
$dst = Join-Path $NewStructureDir 'application\qrcodegen'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: openvpn-gui-master\qrcodegen -> application\qrcodegen' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: qrcodegen' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'openvpn-gui-master\res'
$dst = Join-Path $NewStructureDir 'application\res'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: openvpn-gui-master\res -> application\res' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: res' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'services\message-broker'
$dst = Join-Path $NewStructureDir 'application\message-broker'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: services\message-broker -> application\message-broker' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: message-broker' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'services\product-a'
$dst = Join-Path $NewStructureDir 'application\product-a'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: services\product-a -> application\product-a' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: product-a' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'services\product-b'
$dst = Join-Path $NewStructureDir 'application\product-b'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: services\product-b -> application\product-b' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: product-b' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'src'
$dst = Join-Path $NewStructureDir 'application\src'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: src -> application\src' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: src' -ForegroundColor Green
    }
}

# Paso 4: Reorganizar componentes de prioridad 4
$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\docker'
$dst = Join-Path $NewStructureDir 'docs\docker'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\docker -> docs\docker' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: docker' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\apps\dokploy\__test__'
$dst = Join-Path $NewStructureDir 'tests\__test__'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\apps\dokploy\__test__ -> tests\__test__' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: __test__' -ForegroundColor Green
    }
}

$src = Join-Path $ProjectRoot 'dokploy-canary\packages\server\src\utils\docker'
$dst = Join-Path $NewStructureDir 'docs\docker'
if (Test-Path $src) {
    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null
    if ($DryRun) {
        Write-Host '[DRY RUN] Movería: dokploy-canary\packages\server\src\utils\docker -> docs\docker' -ForegroundColor Cyan
    } else {
        Move-Item $src $dst
        Write-Host 'Movido: docker' -ForegroundColor Green
    }
}

Write-Host '✅ Reorganización completada!' -ForegroundColor Green
Write-Host 'Revisa la nueva estructura en: _new_optimized_structure/' -ForegroundColor Yellow