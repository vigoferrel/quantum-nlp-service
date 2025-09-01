# 🚀 DEPLOYMENT MANUAL AL VPS - VIGOLEONROCKS.COM

## 📊 **DETALLES DEL VPS:**

- **🌍 Ubicación:** Brazil - São Paulo
- **🖥️ Sistema:** Ubuntu 24.04 with Dokploy
- **🏠 Hostname:** srv984842.hstgr.cloud
- **🌐 IP:** 72.60.61.49
- **👤 Usuario:** root
- **⏱️ Uptime:** 2 horas

## 🔧 **PASOS DE DEPLOYMENT:**

### 1. **Conectar al VPS via SSH:**
```bash
ssh root@srv984842.hstgr.cloud
```

### 2. **Preparar el servidor:**
```bash
# Actualizar sistema
apt-get update && apt-get upgrade -y

# Instalar dependencias
apt-get install -y python3 python3-pip python3-venv apache2 supervisor curl

# Crear directorio de deployment
mkdir -p /var/www/vigoleonrocks.com
cd /var/www/vigoleonrocks.com
```

### 3. **Subir archivos al VPS:**

**Opción A: Usar SCP desde tu máquina local:**
```bash
# Desde tu máquina local
scp vigoleonrocks_server.py root@srv984842.hstgr.cloud:/var/www/vigoleonrocks.com/
scp requirements.txt root@srv984842.hstgr.cloud:/var/www/vigoleonrocks.com/
scp .htaccess root@srv984842.hstgr.cloud:/var/www/vigoleonrocks.com/
scp start_vigoleonrocks.sh root@srv984842.hstgr.cloud:/var/www/vigoleonrocks.com/
scp vigoleonrocks.conf root@srv984842.hstgr.cloud:/var/www/vigoleonrocks.com/
scp index.html root@srv984842.hstgr.cloud:/var/www/vigoleonrocks.com/
```

**Opción B: Crear archivos directamente en el VPS:**
```bash
# Conectar al VPS y crear los archivos manualmente
nano vigoleonrocks_server.py
# Pegar el contenido del archivo
```

### 4. **Configurar permisos:**
```bash
chmod +x start_vigoleonrocks.sh
chown -R www-data:www-data /var/www/vigoleonrocks.com
chmod -R 755 /var/www/vigoleonrocks.com
```

### 5. **Instalar dependencias Python:**
```bash
cd /var/www/vigoleonrocks.com
pip3 install -r requirements.txt
```

### 6. **Configurar Supervisor:**
```bash
# Copiar configuración de supervisor
cp vigoleonrocks.conf /etc/supervisor/conf.d/

# Recargar supervisor
supervisorctl reread
supervisorctl update
supervisorctl start vigoleonrocks
```

### 7. **Configurar Apache:**
```bash
# Habilitar módulos necesarios
a2enmod proxy
a2enmod proxy_http
a2enmod rewrite

# Crear configuración de virtual host
nano /etc/apache2/sites-available/vigoleonrocks.com.conf
```

**Contenido del virtual host:**
```apache
<VirtualHost *:80>
    ServerName vigoleonrocks.com
    ServerAlias www.vigoleonrocks.com
    
    DocumentRoot /var/www/vigoleonrocks.com
    
    ProxyPreserveHost On
    ProxyPass / http://localhost:5000/
    ProxyPassReverse / http://localhost:5000/
    
    <Directory /var/www/vigoleonrocks.com>
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/vigoleonrocks_error.log
    CustomLog ${APACHE_LOG_DIR}/vigoleonrocks_access.log combined
</VirtualHost>
```

```bash
# Habilitar sitio
a2ensite vigoleonrocks.com.conf

# Reiniciar Apache
systemctl restart apache2
```

### 8. **Verificar el deployment:**
```bash
# Verificar estado del supervisor
supervisorctl status vigoleonrocks

# Verificar que el servidor Python esté corriendo
curl http://localhost:5000/api/status

# Verificar puerto
netstat -tlnp | grep :5000

# Verificar Apache
systemctl status apache2
```

## 🌐 **URLs DE VERIFICACIÓN:**

- **Página principal:** https://vigoleonrocks.com/
- **API Status:** https://vigoleonrocks.com/api/status
- **API Principal:** https://vigoleonrocks.com/api/vigoleonrocks
- **Detección de idiomas:** https://vigoleonrocks.com/api/detect-language

## 🔍 **TROUBLESHOOTING:**

### Si el servidor Python no inicia:
```bash
# Verificar logs
tail -f /var/log/supervisor/supervisord.log
tail -f /var/log/vigoleonrocks.log

# Reiniciar supervisor
supervisorctl restart vigoleonrocks
```

### Si Apache no funciona:
```bash
# Verificar configuración
apache2ctl configtest

# Verificar logs
tail -f /var/log/apache2/error.log
```

### Si el dominio no resuelve:
```bash
# Verificar DNS
nslookup vigoleonrocks.com

# Verificar firewall
ufw status
```

## 📋 **COMANDOS ÚTILES:**

```bash
# Ver estado del sistema
supervisorctl status
systemctl status apache2

# Ver logs en tiempo real
tail -f /var/log/vigoleonrocks.log
tail -f /var/log/apache2/vigoleonrocks_access.log

# Reiniciar servicios
supervisorctl restart vigoleonrocks
systemctl restart apache2

# Verificar puertos
netstat -tlnp | grep :5000
netstat -tlnp | grep :80
```

## 🎉 **RESULTADO FINAL:**

Una vez completado el deployment, tendrás:
- ✅ **Sistema Python Flask** corriendo en puerto 5000
- ✅ **Apache** como proxy reverso
- ✅ **Supervisor** para auto-inicio
- ✅ **12 idiomas** soportados
- ✅ **APIs multilingües** operativas
- ✅ **Dominio vigoleonrocks.com** funcionando

¡El sistema VIGOLEONROCKS estará completamente operativo en producción! 🚀
