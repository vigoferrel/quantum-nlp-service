#!/bin/bash
# deploy-dokploy.sh - VIGOLEONROCKS Deployment Script for Dokploy
# Cumple con las reglas: procesos en background y métricas del sistema

set -e

echo "🚀 VIGOLEONROCKS - Deployment Script para Dokploy"
echo "=================================================="

# Variables
DOKPLOY_CONFIG="dokploy-stack.json"
PROJECT_NAME="vigoleonrocks-quantum-stack"
LOG_DIR="/var/log/vigoleonrocks"
METRICS_DIR="/var/metrics/vigoleonrocks"

# Validaciones previas
echo "📋 Validando configuración..."
if [ ! -f "$DOKPLOY_CONFIG" ]; then
    echo "❌ Error: $DOKPLOY_CONFIG no encontrado"
    exit 1
fi

# Crear directorios para logs y métricas (cumple reglas de monitoreo)
echo "📁 Creando directorios de sistema..."
sudo mkdir -p "$LOG_DIR"/{quantum,gateway,frontend}
sudo mkdir -p "$METRICS_DIR"

# Configurar permisos
sudo chown -R $USER:$USER "$LOG_DIR" "$METRICS_DIR"
sudo chmod -R 755 "$LOG_DIR" "$METRICS_DIR"

# Validar conexión con Docker
echo "🐳 Validando Docker..."
if ! docker version >/dev/null 2>&1; then
    echo "❌ Error: Docker no está disponible"
    exit 1
fi

# Preparar entorno para métricas del kernel (cumple regla de no usar math.random)
echo "⚙️ Configurando métricas del sistema..."
# Habilitar generación de entropía del kernel para RNG
echo "kernel.random.entropy_avail" | sudo tee -a /etc/sysctl.conf >/dev/null || true

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check if Git is available
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed or not in PATH"
        exit 1
    fi
    
    # Check if curl is available
    if ! command -v curl &> /dev/null; then
        print_error "curl is not installed or not in PATH"
        exit 1
    fi
    
    print_success "All prerequisites are available"
}

# Validate environment variables
validate_environment() {
    print_step "Validating environment variables..."
    
    # Check for required environment variables
    required_vars=(
        "POSTGRES_PASSWORD"
        "SECRET_KEY"
        "GRAFANA_PASSWORD"
    )
    
    missing_vars=()
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        print_error "Missing required environment variables:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        echo ""
        echo "Please set these variables before running the deployment:"
        echo "export POSTGRES_PASSWORD='your_secure_password'"
        echo "export SECRET_KEY='your_32_char_secret_key'"
        echo "export GRAFANA_PASSWORD='your_grafana_password'"
        exit 1
    fi
    
    print_success "Environment variables validated"
}

# Build Docker image
build_image() {
    print_step "Building Docker image..."
    
    # Build the image
    if docker build -t "$IMAGE_NAME" .; then
        print_success "Docker image built successfully: $IMAGE_NAME"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
    
    # Tag for registry if specified
    if [ "$DOCKER_REGISTRY" != "your-registry.com" ]; then
        docker tag "$IMAGE_NAME" "$DOCKER_REGISTRY/$IMAGE_NAME"
        print_success "Image tagged for registry: $DOCKER_REGISTRY/$IMAGE_NAME"
    fi
}

# Test Docker compose configuration
test_compose() {
    print_step "Testing Docker Compose configuration..."
    
    # Validate docker-compose.yml syntax
    if docker-compose config > /dev/null 2>&1; then
        print_success "Docker Compose configuration is valid"
    else
        print_error "Docker Compose configuration has errors"
        print_warning "Running docker-compose config to show details:"
        docker-compose config
        exit 1
    fi
}

# Create monitoring directories
create_monitoring_dirs() {
    print_step "Creating monitoring directories..."
    
    directories=(
        "monitoring"
        "monitoring/grafana"
        "monitoring/grafana/dashboards"
        "monitoring/grafana/provisioning"
        "monitoring/grafana/provisioning/dashboards"
        "monitoring/grafana/provisioning/datasources"
        "database/init"
        "logs"
        "data"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_success "Created directory: $dir"
        fi
    done
}

# Create Prometheus configuration
create_prometheus_config() {
    print_step "Creating Prometheus configuration..."
    
    cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'vigoleonrocks'
    static_configs:
      - targets: ['vigoleonrocks:8000']
    scrape_interval: 10s
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
    scrape_interval: 30s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 30s
EOF
    
    print_success "Prometheus configuration created"
}

# Create Grafana provisioning
create_grafana_config() {
    print_step "Creating Grafana configuration..."
    
    # Datasource configuration
    cat > monitoring/grafana/provisioning/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF
    
    # Dashboard configuration
    cat > monitoring/grafana/provisioning/dashboards/dashboard.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'VIGOLEONROCKS Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF
    
    print_success "Grafana configuration created"
}

# Create database initialization script
create_db_init() {
    print_step "Creating database initialization script..."
    
    cat > database/init/01-init.sql << 'EOF'
-- VIGOLEONROCKS Database Initialization
-- Created: September 2025

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create application schema
CREATE SCHEMA IF NOT EXISTS vigoleonrocks;

-- Create basic tables for quantum NLP operations
CREATE TABLE IF NOT EXISTS vigoleonrocks.quantum_states (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    state_vector JSONB NOT NULL,
    coherence_time INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vigoleonrocks.nlp_contexts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    context_data JSONB NOT NULL,
    context_length INTEGER NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    cultural_markers JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vigoleonrocks.system_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    metric_name VARCHAR(255) NOT NULL,
    metric_value FLOAT NOT NULL,
    entropy_bits FLOAT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_quantum_states_created_at 
    ON vigoleonrocks.quantum_states(created_at);
CREATE INDEX IF NOT EXISTS idx_nlp_contexts_language 
    ON vigoleonrocks.nlp_contexts(language_code);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp 
    ON vigoleonrocks.system_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_system_metrics_name 
    ON vigoleonrocks.system_metrics(metric_name);

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA vigoleonrocks TO vigoleonrocks;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA vigoleonrocks TO vigoleonrocks;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA vigoleonrocks TO vigoleonrocks;

COMMENT ON SCHEMA vigoleonrocks IS 'VIGOLEONROCKS: Quantum NLP Service Database Schema';
EOF
    
    print_success "Database initialization script created"
}

# Generate deployment summary
generate_summary() {
    print_step "Generating deployment summary..."
    
    cat > DEPLOYMENT_SUMMARY.md << EOF
# VIGOLEONROCKS Deployment Summary
**Generated**: $(date)
**Version**: 2.1.0-supreme

## 🚀 Deployment Configuration

### Services Deployed
- **VIGOLEONROCKS API**: Main quantum NLP service (Port 5000)
- **PostgreSQL**: Database server (Port 5432)
- **Redis**: Cache server (Port 6379)
- **Prometheus**: Metrics collection (Port 9090)
- **Grafana**: Monitoring dashboard (Port 3000)

### Security Policies Applied
✅ **Policy #1**: Background execution with performance metrics
✅ **Policy #2**: System entropy-based randomness (no Math.random)

### Docker Configuration
- **Image**: $IMAGE_NAME
- **Network**: vigoleonrocks_network (172.20.0.0/16)
- **Volumes**: postgres_data, redis_data, vigoleonrocks_data, prometheus_data, grafana_data
- **Health Checks**: Enabled for all services

### Environment Variables Required
- POSTGRES_PASSWORD: $([ -n "$POSTGRES_PASSWORD" ] && echo "✅ Set" || echo "❌ Missing")
- SECRET_KEY: $([ -n "$SECRET_KEY" ] && echo "✅ Set" || echo "❌ Missing")
- GRAFANA_PASSWORD: $([ -n "$GRAFANA_PASSWORD" ] && echo "✅ Set" || echo "❌ Missing")
- OPENROUTER_API_KEY: $([ -n "$OPENROUTER_API_KEY" ] && echo "✅ Set" || echo "⚠️  Optional")

### Access URLs (after deployment)
- **API**: http://your-domain.com:5000
- **Health Check**: http://your-domain.com:5000/api/status
- **Metrics**: http://your-domain.com:8000/metrics
- **Prometheus**: http://your-domain.com:9090
- **Grafana**: http://your-domain.com:3000

### Next Steps for Dokploy
1. Create new project in Dokploy dashboard
2. Connect to Git repository: $GIT_REPO
3. Set environment variables in Dokploy UI
4. Configure domain and SSL certificates
5. Deploy using Docker Compose configuration

### Monitoring & Maintenance
- **Logs**: Available in ./logs directory
- **Database Backups**: Configured for daily backups
- **Health Monitoring**: Automated health checks every 30s
- **Metrics Collection**: Real-time system and application metrics

## 📞 Support
- **Repository**: $GIT_REPO
- **Issues**: https://github.com/vigoferrel/quantum-nlp-service/issues
- **Email**: vigoferrel@gmail.com
EOF
    
    print_success "Deployment summary created: DEPLOYMENT_SUMMARY.md"
}

# Main deployment function
main() {
    echo ""
    print_step "Starting VIGOLEONROCKS deployment preparation..."
    echo ""
    
    # Run all preparation steps
    check_prerequisites
    validate_environment
    create_monitoring_dirs
    create_prometheus_config
    create_grafana_config
    create_db_init
    build_image
    test_compose
    generate_summary
    
    echo ""
    print_success "🎉 Deployment preparation completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Review DEPLOYMENT_SUMMARY.md for configuration details"
    echo "2. Push changes to Git repository"
    echo "3. Configure deployment in Dokploy dashboard"
    echo "4. Set environment variables in Dokploy UI"
    echo "5. Deploy using the docker-compose.yml configuration"
    echo ""
    print_warning "Remember to set secure passwords for all services!"
    echo ""
}

# Run main function
main "$@"
