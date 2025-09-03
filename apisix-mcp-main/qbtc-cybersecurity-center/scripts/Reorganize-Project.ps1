# Reorganize-Project.ps1
# Script to reorganize QBTC Cybersecurity Center structure

$ErrorActionPreference = "Stop"

$SYSTEM_ROOT = "C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED\3.0"
$SECURITY_CENTER = "$SYSTEM_ROOT\qbtc-cybersecurity-center"

# Create new directories if they don't exist
$directories = @(
    "$SECURITY_CENTER\core",
    "$SECURITY_CENTER\engines",
    "$SECURITY_CENTER\services",
    "$SECURITY_CENTER\middleware",
    "$SECURITY_CENTER\tests",
    "$SECURITY_CENTER\scripts",
    "$SECURITY_CENTER\config",
    "$SECURITY_CENTER\dashboard",
    "$SECURITY_CENTER\dashboard\api",
    "$SECURITY_CENTER\dashboard\web"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        Write-Host "Creating directory: $dir"
        New-Item -ItemType Directory -Path $dir -Force
    }
}

# Move existing content to new structure
# Core components
if (Test-Path "$SECURITY_CENTER\modules") {
    Get-ChildItem "$SECURITY_CENTER\modules\security*" | Move-Item -Destination "$SECURITY_CENTER\core" -Force
    Get-ChildItem "$SECURITY_CENTER\modules\quantum*" | Move-Item -Destination "$SECURITY_CENTER\core" -Force
}

# Engines
if (Test-Path "$SECURITY_CENTER\engines") {
    # Engines directory already exists, just ensure structure
    @("monitoring", "simulation", "analysis", "response") | ForEach-Object {
        $engineDir = "$SECURITY_CENTER\engines\$_"
        if (-not (Test-Path $engineDir)) {
            New-Item -ItemType Directory -Path $engineDir -Force
        }
    }
}

# Services setup
@("redis", "rabbitmq", "supabase") | ForEach-Object {
    $serviceDir = "$SECURITY_CENTER\services\$_"
    if (-not (Test-Path $serviceDir)) {
        New-Item -ItemType Directory -Path $serviceDir -Force
    }
}

# Move existing config files
if (Test-Path "$SECURITY_CENTER\configs") {
    Get-ChildItem "$SECURITY_CENTER\configs\*" | Move-Item -Destination "$SECURITY_CENTER\config" -Force
    Remove-Item "$SECURITY_CENTER\configs" -Force
}

# Create base service files
$services = @{
    "redis" = @"
// Redis Service Configuration and Setup
const Redis = require('ioredis');
const config = require('../../config/redis.config');

class RedisService {
    constructor() {
        this.client = new Redis(config);
        this.setupEventHandlers();
    }

    setupEventHandlers() {
        this.client.on('error', (err) => console.error('Redis Error:', err));
        this.client.on('connect', () => console.log('Redis Connected'));
    }
}

module.exports = new RedisService();
"@

    "rabbitmq" = @"
// RabbitMQ Service Configuration and Setup
const amqp = require('amqplib');
const config = require('../../config/rabbitmq.config');

class RabbitMQService {
    constructor() {
        this.connection = null;
        this.channel = null;
        this.setupConnection();
    }

    async setupConnection() {
        try {
            this.connection = await amqp.connect(config.url);
            this.channel = await this.connection.createChannel();
            console.log('RabbitMQ Connected');
        } catch (err) {
            console.error('RabbitMQ Connection Error:', err);
        }
    }
}

module.exports = new RabbitMQService();
"@

    "supabase" = @"
// Supabase Service Configuration and Setup
const { createClient } = require('@supabase/supabase-js');
const config = require('../../config/supabase.config');

class SupabaseService {
    constructor() {
        this.client = createClient(config.url, config.key);
    }

    async healthCheck() {
        try {
            const { data, error } = await this.client.from('health').select('*').limit(1);
            return !error;
        } catch (err) {
            console.error('Supabase Health Check Error:', err);
            return false;
        }
    }
}

module.exports = new SupabaseService();
"@
}

foreach ($service in $services.Keys) {
    $servicePath = "$SECURITY_CENTER\services\$service\index.js"
    if (-not (Test-Path $servicePath)) {
        Set-Content -Path $servicePath -Value $services[$service]
    }
}

Write-Host "Project structure reorganization completed!"
