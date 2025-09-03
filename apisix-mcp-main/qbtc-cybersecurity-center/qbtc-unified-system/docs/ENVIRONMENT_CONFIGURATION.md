# QBTC Environment Configuration Guide

## Overview
This document describes all environment variables used in the QBTC Quantum System.

## Environment Files
- `.env.development` - Development environment
- `.env.production` - Production environment  
- `.env.unified` - Unified development environment (Phase 2)

## Configuration Categories

### Core System
- `NODE_ENV`: Application environment (development/production)
- `DEBUG`: Enable debug mode (true/false)
- `LOG_LEVEL`: Logging level (debug/info/warn/error)

### Quantum Consciousness
- `QUANTUM_CONSCIOUSNESS_HOST`: Host for quantum core service
- `QUANTUM_CONSCIOUSNESS_PORT`: Port for quantum core service
- `QUANTUM_COHERENCE_THRESHOLD`: Minimum coherence level (0.0-1.0)

### Database
- `POSTGRES_HOST`: PostgreSQL host
- `POSTGRES_PORT`: PostgreSQL port
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password

### Security
- `API_SECRET_KEY`: Secret key for API authentication
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `SSL_ENABLED`: Enable SSL/TLS (true/false)

## Production Setup

1. Copy `.env.production` to `.env`
2. Update all placeholder values with actual credentials
3. Ensure all secret keys are cryptographically secure
4. Set appropriate resource limits for your environment
5. Configure monitoring and logging endpoints

## Security Notes

- Never commit actual secrets to version control
- Use environment-specific secret management
- Rotate secrets regularly
- Use strong, unique passwords
- Enable SSL/TLS in production

## Validation

Run the health checker to validate configuration:
```bash
python tools/health_checker.py
```
