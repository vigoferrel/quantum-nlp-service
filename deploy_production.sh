#!/bin/bash
# VIGOLEONROCKS Production Deployment Script
# Target: srv984842.hstgr.cloud
# Stack: Quantum Processor + API Gateway + Frontend

set -e

echo "🚀 VIGOLEONROCKS PRODUCTION DEPLOYMENT"
echo "====================================="
echo "Target: srv984842.hstgr.cloud"
echo "Stack: Complete quantum AI ecosystem"
echo ""

# Configuration
SERVER_HOST="srv984842.hstgr.cloud"
SERVER_USER="root"
PROJECT_DIR="/var/www/vigoleonrocks"
BACKUP_DIR="/var/backups/vigoleonrocks"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Step 1: Pre-deployment checks
log "Step 1: Pre-deployment checks"
echo "Checking local files..."

# Check critical files exist
FILES_TO_CHECK=(
    "vigoleonrocks/interfaces/rest_api.py"
    "api_gateway_8004.py"
    "vigoleonrocks_quantum_command_center.html"
    "simple_api.py"
    "requirements.txt"
)

for file in "${FILES_TO_CHECK[@]}"; do
    if [ ! -f "$file" ]; then
        error "Critical file missing: $file"
    fi
    log "✓ Found: $file"
done

# Check server connectivity
log "Testing server connectivity..."
if ! ssh -q $SERVER_USER@$SERVER_HOST "echo 'Connection OK'"; then
    error "Cannot connect to server $SERVER_HOST"
fi
log "✓ Server connection established"

# Step 2: Backup existing deployment
log "Step 2: Creating backup of existing deployment"
ssh $SERVER_USER@$SERVER_HOST "
    if [ -d '$PROJECT_DIR' ]; then
        mkdir -p $BACKUP_DIR
        backup_name=\"vigoleonrocks-backup-\$(date +%Y%m%d-%H%M%S)\"
        cp -r $PROJECT_DIR $BACKUP_DIR/\$backup_name
        echo 'Backup created: $BACKUP_DIR/\$backup_name'
    else
        echo 'No existing deployment to backup'
    fi
"

# Step 3: Prepare server environment
log "Step 3: Preparing server environment"
ssh $SERVER_USER@$SERVER_HOST "
    # Update system
    apt update && apt upgrade -y
    
    # Install required packages
    apt install -y python3 python3-pip python3-venv nginx supervisor htop curl jq
    
    # Create project directory
    mkdir -p $PROJECT_DIR
    mkdir -p $PROJECT_DIR/logs
    mkdir -p $PROJECT_DIR/static
    
    # Create virtual environment
    python3 -m venv $PROJECT_DIR/venv
    
    # Create vigoleonrocks user if not exists
    if ! id 'vigoleonrocks' &>/dev/null; then
        useradd -r -s /bin/false vigoleonrocks
        usermod -d $PROJECT_DIR vigoleonrocks
    fi
    
    # Set permissions
    chown -R vigoleonrocks:vigoleonrocks $PROJECT_DIR
"

# Step 4: Upload files
log "Step 4: Uploading application files"
rsync -avz --delete \
    --exclude='.git/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='logs/' \
    ./ $SERVER_USER@$SERVER_HOST:$PROJECT_DIR/

# Step 5: Install Python dependencies
log "Step 5: Installing Python dependencies"
ssh $SERVER_USER@$SERVER_HOST "
    cd $PROJECT_DIR
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install flask flask-cors requests psutil prometheus_client gunicorn
"

# Step 6: Configure services
log "Step 6: Configuring system services"

# Create supervisor configs
ssh $SERVER_USER@$SERVER_HOST "cat > /etc/supervisor/conf.d/vigoleonrocks-quantum.conf << 'EOF'
[program:vigoleonrocks-quantum]
command=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/simple_api.py
directory=$PROJECT_DIR
user=vigoleonrocks
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$PROJECT_DIR/logs/quantum-processor.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=3
environment=PORT=5000,FLASK_ENV=production
EOF"

ssh $SERVER_USER@$SERVER_HOST "cat > /etc/supervisor/conf.d/vigoleonrocks-gateway.conf << 'EOF'
[program:vigoleonrocks-gateway]
command=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/api_gateway_8004.py
directory=$PROJECT_DIR
user=vigoleonrocks
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$PROJECT_DIR/logs/api-gateway.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=3
environment=GATEWAY_PORT=8004,VIGOLEONROCKS_BACKEND=http://localhost:5000
EOF"

# Step 7: Configure Nginx
log "Step 7: Configuring Nginx reverse proxy"
ssh $SERVER_USER@$SERVER_HOST "cat > /etc/nginx/sites-available/vigoleonrocks << 'EOF'
server {
    listen 80;
    server_name srv984842.hstgr.cloud vigoleonrocks.srv984842.hstgr.cloud;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name srv984842.hstgr.cloud vigoleonrocks.srv984842.hstgr.cloud;
    
    # SSL Configuration (using Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/srv984842.hstgr.cloud/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/srv984842.hstgr.cloud/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection \"1; mode=block\";
    add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\";
    
    # Serve static files
    location / {
        root $PROJECT_DIR;
        try_files \$uri \$uri/ @quantum-ui;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control \"public, immutable\";
        }
    }
    
    # Frontend fallback
    location @quantum-ui {
        try_files /vigoleonrocks_quantum_command_center.html =404;
    }
    
    # API Gateway proxy
    location /gateway/ {
        proxy_pass http://localhost:8004/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Headers for API Gateway
        proxy_set_header X-Gateway-Route \"nginx-proxy\";
    }
    
    # Main API proxy
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Enable streaming for long responses
        proxy_buffering off;
        proxy_request_buffering off;
        
        # Timeouts for quantum processing
        proxy_connect_timeout 5s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    
    # Health checks (no logging)
    location /health {
        proxy_pass http://localhost:8004/health;
        access_log off;
    }
    
    # Metrics endpoint (restricted)
    location /metrics {
        proxy_pass http://localhost:5000/api/status;
        allow 127.0.0.1;
        deny all;
    }
}
EOF"

# Enable site
ssh $SERVER_USER@$SERVER_HOST "
    ln -sf /etc/nginx/sites-available/vigoleonrocks /etc/nginx/sites-enabled/
    nginx -t || exit 1
"

# Step 8: SSL Certificate setup
log "Step 8: Setting up SSL certificate"
ssh $SERVER_USER@$SERVER_HOST "
    # Install certbot if not present
    if ! command -v certbot &> /dev/null; then
        apt install -y certbot python3-certbot-nginx
    fi
    
    # Get or renew certificate
    certbot --nginx -d srv984842.hstgr.cloud -d vigoleonrocks.srv984842.hstgr.cloud --non-interactive --agree-tos --email admin@vigoleonrocks.com || true
"

# Step 9: Start services
log "Step 9: Starting services"
ssh $SERVER_USER@$SERVER_HOST "
    # Reload supervisor
    supervisorctl reread
    supervisorctl update
    
    # Start VIGOLEONROCKS services
    supervisorctl start vigoleonrocks-quantum
    supervisorctl start vigoleonrocks-gateway
    
    # Reload nginx
    systemctl reload nginx
    
    # Enable auto-start on boot
    systemctl enable supervisor
    systemctl enable nginx
"

# Step 10: Health checks
log "Step 10: Running health checks"
echo "Waiting for services to start..."
sleep 10

# Test quantum processor
if ssh $SERVER_USER@$SERVER_HOST "curl -f -s http://localhost:5000/api/status > /dev/null"; then
    log "✓ Quantum Processor (5000) - OK"
else
    warn "⚠ Quantum Processor (5000) - NOT RESPONDING"
fi

# Test API gateway
if ssh $SERVER_USER@$SERVER_HOST "curl -f -s http://localhost:8004/health > /dev/null"; then
    log "✓ API Gateway (8004) - OK"
else
    warn "⚠ API Gateway (8004) - NOT RESPONDING"
fi

# Test HTTPS
if curl -f -s https://srv984842.hstgr.cloud > /dev/null; then
    log "✓ HTTPS Frontend - OK"
else
    warn "⚠ HTTPS Frontend - NOT RESPONDING"
fi

# Step 11: Final status
log "Step 11: Deployment summary"
ssh $SERVER_USER@$SERVER_HOST "
    echo '🔍 Service Status:'
    supervisorctl status vigoleonrocks-quantum vigoleonrocks-gateway
    echo ''
    echo '📊 System Resources:'
    free -h
    df -h /
    echo ''
    echo '📝 Log Files:'
    ls -la $PROJECT_DIR/logs/
    echo ''
    echo '🌐 Endpoints:'
    echo '  • Frontend: https://srv984842.hstgr.cloud'
    echo '  • API Status: https://srv984842.hstgr.cloud/api/status'
    echo '  • Gateway Health: https://srv984842.hstgr.cloud/gateway/health'
    echo '  • Quantum Metrics: https://srv984842.hstgr.cloud/api/quantum-metrics'
"

echo ""
log "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "====================================="
echo "🌐 Frontend: https://srv984842.hstgr.cloud"
echo "📊 API Status: https://srv984842.hstgr.cloud/api/status"
echo "🚪 Gateway Health: https://srv984842.hstgr.cloud/gateway/health"
echo "⚛️ Quantum Metrics: https://srv984842.hstgr.cloud/api/quantum-metrics"
echo ""
echo "📋 Management Commands:"
echo "  • View logs: ssh root@srv984842.hstgr.cloud 'supervisorctl tail -f vigoleonrocks-quantum'"
echo "  • Restart services: ssh root@srv984842.hstgr.cloud 'supervisorctl restart vigoleonrocks-*'"
echo "  • Check status: ssh root@srv984842.hstgr.cloud 'supervisorctl status'"
echo ""
log "VIGOLEONROCKS quantum AI stack is now live in production! 🌌⚛️"
