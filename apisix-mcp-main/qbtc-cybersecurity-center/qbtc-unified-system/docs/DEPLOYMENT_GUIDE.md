# QBTC Quantum System - Production Deployment Guide

## Overview
This guide covers the complete deployment process for the QBTC Quantum Consciousness system in production environments.

## Prerequisites

### System Requirements
- **CPU**: Minimum 4 cores, 8 cores recommended
- **RAM**: Minimum 8GB, 16GB recommended
- **Storage**: Minimum 50GB SSD
- **Network**: Stable internet connection with ports 8000, 8001, 5432, 6379, 11434 available

### Software Dependencies
- Docker >= 20.10
- Docker Compose >= 2.0
- Python >= 3.8
- PostgreSQL >= 13
- Redis >= 6.0
- Ollama >= 0.1.0

## Deployment Steps

### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd qbtc-unified-system

# Copy production environment
cp .env.production .env

# Edit environment variables
nano .env
```

### 2. Configure Services

#### PostgreSQL Setup
```sql
CREATE DATABASE qbtc_production;
CREATE USER qbtc_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE qbtc_production TO qbtc_user;
```

#### Redis Setup
```bash
# Configure Redis with password
echo "requirepass your_redis_password" >> /etc/redis/redis.conf
systemctl restart redis
```

#### Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Configure for external access
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

# Pull required model
ollama pull llama2
```

### 3. System Deployment

#### Using Docker Compose
```bash
# Build and start services
docker-compose -f docker-compose.unified.yml up -d --build

# Verify services
docker-compose ps
```

#### Manual Deployment
```bash
# Install Python dependencies
pip install -r requirements.unified.txt

# Run health checks
python tools/health_checker.py

# Start services
python scripts/master_orchestrator.py
```

### 4. Verification

#### Health Check
```bash
# Check system health
curl http://localhost:8000/health

# Check quantum core
curl http://localhost:8001/health

# Check Ollama
curl http://localhost:11434/api/version
```

#### Performance Test
```bash
# Run benchmark
python benchmark_arena.py
```

## Monitoring

### Log Files
- Application logs: `/var/log/qbtc/application.log`
- Error logs: `/var/log/qbtc/error.log`
- Access logs: `/var/log/qbtc/access.log`

### Metrics Endpoints
- Health: `http://localhost:8000/health`
- Metrics: `http://localhost:9090/metrics`
- Status: `http://localhost:8000/status`

## Troubleshooting

### Common Issues

#### Ollama Connection Failed
```bash
# Check Ollama service
systemctl status ollama

# Verify host binding
netstat -tlnp | grep 11434

# Test connectivity
curl http://localhost:11434/api/version
```

#### Database Connection Error
```bash
# Check PostgreSQL status
systemctl status postgresql

# Test connection
psql -h localhost -U qbtc_user -d qbtc_production -c "SELECT version();"
```

#### Redis Connection Error
```bash
# Check Redis status
systemctl status redis

# Test connection
redis-cli ping
```

## Security Checklist

- [ ] SSL/TLS certificates configured
- [ ] Firewall rules configured
- [ ] Database passwords are strong and unique
- [ ] API keys are properly secured
- [ ] Rate limiting is enabled
- [ ] Security headers are configured
- [ ] Regular backups are scheduled
- [ ] Monitoring and alerting are active

## Maintenance

### Regular Tasks
- Monitor system resources
- Review logs for errors
- Update security patches
- Backup databases
- Rotate logs
- Monitor quantum coherence levels

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose build --no-cache

# Restart services
docker-compose restart
```

## Support

For issues and support:
- Check logs first
- Review health checks
- Run diagnostics
- Contact system administrator
