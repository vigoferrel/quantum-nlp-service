#!/bin/bash

# 🚀 VIGOLEONROCKS - DEPLOYMENT FINAL SIMPLIFICADO
# ================================================

echo "🚀 DEPLOYMENT FINAL VIGOLEONROCKS"
echo "================================="

# Instalar nginx
echo "📦 Instalando nginx..."
apt update && apt install -y nginx

# Crear directorios
echo "📁 Creando directorios..."
mkdir -p /var/www/vigoleonrocks.com/{public_html,logs/{nginx,app}}

# Configurar nginx
echo "⚙️ Configurando nginx..."
cat > /etc/nginx/sites-available/vigoleonrocks.com << 'EOF'
server {
    listen 80;
    server_name vigoleonrocks.com www.vigoleonrocks.com;
    root /var/www/vigoleonrocks.com/public_html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Habilitar sitio
ln -sf /etc/nginx/sites-available/vigoleonrocks.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Instalar dependencias Python
echo "🐍 Instalando dependencias Python..."
cd /var/www/vigoleonrocks.com
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors psycopg2-binary gunicorn requests
deactivate

# Configurar PostgreSQL
echo "🗄️ Configurando PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE IF NOT EXISTS vigoleonrocks_db;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER IF NOT EXISTS vigoleonrocks WITH PASSWORD '0gLuiWUTaw3Q)3GOFM&J';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE vigoleonrocks_db TO vigoleonrocks;" 2>/dev/null || true

# Crear página web
echo "🌐 Creando página web..."
cat > /var/www/vigoleonrocks.com/public_html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>VIGOLEONROCKS - IA Humana</title>
    <style>body{text-align:center;padding:50px;background:linear-gradient(45deg,#667eea,#764ba2);color:white;font-family:Arial;}h1{font-size:3em;}a{color:#ff6b6b;text-decoration:none;font-weight:bold;}</style>
</head>
<body>
    <h1>🚀 VIGOLEONROCKS</h1>
    <p>Sistema de IA Humana Avanzada</p>
    <p>✅ Deployment completado exitosamente</p>
    <p><a href="/api/status">Ver estado de la API</a></p>
</body>
</html>
EOF

# Crear script de inicio
echo "🚀 Creando script de inicio..."
cat > /var/www/vigoleonrocks.com/start.sh << 'EOF'
#!/bin/bash
cd /var/www/vigoleonrocks.com
source venv/bin/activate
export FLASK_APP=vigoleonrocks/interfaces/rest_api.py
export FLASK_ENV=production
export DATABASE_URL="postgresql://vigoleonrocks:0gLuiWUTaw3Q)3GOFM&J@localhost:5432/vigoleonrocks_db"

if pgrep -f gunicorn > /dev/null; then pkill -f gunicorn; sleep 2; fi

gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 2 --access-logfile logs/app/access.log --error-logfile logs/app/error.log --log-level info --daemon vigoleonrocks.interfaces.rest_api:app

sleep 3
if pgrep -f gunicorn > /dev/null; then echo "✅ Aplicación iniciada"; else echo "❌ Error en aplicación"; fi
deactivate
EOF

chmod +x /var/www/vigoleonrocks.com/start.sh

# Configurar permisos
echo "🔒 Configurando permisos..."
chown -R www-data:www-data /var/www/vigoleonrocks.com

# Configurar firewall
echo "🛡️ Configurando firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw --force enable

# Reiniciar servicios
echo "🔄 Reiniciando servicios..."
systemctl restart nginx
systemctl enable nginx

# Iniciar aplicación
echo "🚀 Iniciando aplicación..."
cd /var/www/vigoleonrocks.com
./start.sh

# Verificación final
echo ""
echo "🎉 DEPLOYMENT COMPLETADO"
echo "======================="
echo "🌐 Sitio web: http://vigoleonrocks.com"
echo "🔗 API: http://vigoleonrocks.com/api"
echo ""
echo "📊 Verificación:"
curl -I http://localhost 2>/dev/null | head -1 || echo "Sitio no responde aún"
curl -s http://localhost:5000/api/status 2>/dev/null | grep -o "status" || echo "API no responde aún"
echo ""
echo "✅ DEPLOYMENT FINALIZADO"