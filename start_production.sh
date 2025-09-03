#!/bin/bash
cd /var/www/vigoleonrocks.com
export FLASK_APP=vigoleonrocks_server.py
export FLASK_ENV=production
export PYTHONPATH=/var/www/vigoleonrocks.com

# Iniciar con Gunicorn
gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 2 \
    --threads 2 \
    --worker-class gthread \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --timeout 60 \
    --keep-alive 10 \
    --daemon \
    vigoleonrocks_server:app
