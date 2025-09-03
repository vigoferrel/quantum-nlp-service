#!/bin/bash
# VIGOLEONROCKS.COM - Script de Deployment Corregido
echo "🚀 VIGOLEONROCKS.COM - DEPLOYMENT SCRIPT CORREGIDO"
echo "=================================================="

# 1. Preparar el servidor
echo "📦 Preparando servidor..."
apt-get update && apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv apache2 supervisor curl

# 2. Crear directorio y mover archivos
echo "📁 Creando directorio y moviendo archivos..."
mkdir -p /var/www/vigoleonrocks.com
mv /root/vigoleonrocks_server.py /var/www/vigoleonrocks.com/
mv /root/requirements.txt /var/www/vigoleonrocks.com/
mv /root/.htaccess /var/www/vigoleonrocks.com/
mv /root/start_vigoleonrocks.sh /var/www/vigoleonrocks.com/
mv /root/vigoleonrocks.conf /var/www/vigoleonrocks.com/
mv /root/index.html /var/www/vigoleonrocks.com/
cd /var/www/vigoleonrocks.com

# 3. Configurar permisos
echo "🔧 Configurando permisos..."
chmod +x start_vigoleonrocks.sh
chown -R www-data:www-data .
chmod -R 755 .

# 4. Instalar dependencias Python
echo "🐍 Instalando dependencias Python..."
pip3 install -r requirements.txt

# 5. Configurar supervisor
echo "⚙️ Configurando supervisor..."
cp vigoleonrocks.conf /etc/supervisor/conf.d/
supervisorctl reread
supervisorctl update
supervisorctl start vigoleonrocks

# 6. Configurar Apache
echo "🌐 Configurando Apache..."
a2enmod proxy
a2enmod proxy_http
a2enmod rewrite
systemctl restart apache2

# 7. Verificar deployment
echo "🔍 Verificando deployment..."
sleep 5
supervisorctl status vigoleonrocks
curl -s http://localhost:5000/api/status
netstat -tlnp | grep :5000

echo "🎉 DEPLOYMENT COMPLETADO!"
echo "🌐 URLs:"
echo "   https://vigoleonrocks.com/"
echo "   https://vigoleonrocks.com/api/status"
