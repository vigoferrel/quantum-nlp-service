# 🚀 DEPLOYMENT VIGOLEONROCKS EN TU VPS

## 📍 **DETALLES DE TU VPS**
- **Nombre de host**: `srv984842.hstgr.cloud`
- **IP Address**: `72.60.61.49`
- **IPv6**: `2a02:4780:66:bfe::1`
- **Dokploy URL**: `http://72.60.61.49:3000`

---

## 🎯 **MÉTODO 1: DEPLOYMENT AUTOMÁTICO (Recomendado)**

### **Paso 1: Preparar Variables de Entorno**
```bash
# Configurar variables de entorno en tu sistema local
export DOKPLOY_API_TOKEN="tu-token-de-dokploy"
export POSTGRES_PASSWORD="tu-password-seguro"
export SECRET_KEY="tu-secret-key-unica"
export OPENROUTER_API_KEY="tu-api-key-openrouter"
```

### **Paso 2: Ejecutar Deployment Automático**
```bash
# Ejecutar el script personalizado para tu VPS
python deploy_vps.py
```

### **Paso 3: Verificar Deployment**
```bash
# Verificar que la aplicación esté funcionando
curl http://72.60.61.49/api/status

# Acceder a la aplicación
# http://72.60.61.49
```

---

## 🎯 **MÉTODO 2: DEPLOYMENT MANUAL CON DASHBOARD**

### **Paso 1: Acceder al Dashboard de Dokploy**
```bash
# Abrir en tu navegador
http://72.60.61.49:3000
```

### **Paso 2: Crear Proyecto**
1. **Ir a "Projects"** → **"Create Project"**
2. **Seleccionar "Connect Git Repository"**
3. **Configurar**:
   - **Repository URL**: `https://github.com/vigoferrel/quantum-nlp-service`
   - **Branch**: `main`
   - **Auto Deploy**: ✅ Enabled

### **Paso 3: Configurar Servicios**
Dokploy detectará automáticamente la configuración de `.dokploy/config.json`

### **Paso 4: Configurar Variables de Entorno**
En **Project Settings** → **Environment Variables**:

```bash
# Base de datos
POSTGRES_PASSWORD=tu-password-seguro

# Seguridad
SECRET_KEY=tu-secret-key-unica

# APIs externas
OPENROUTER_API_KEY=tu-api-key-openrouter

# URLs de servicios
DATABASE_URL=postgresql://vigoleonrocks:${POSTGRES_PASSWORD}@postgres:5432/vigoleonrocks
REDIS_URL=redis://redis:6379
```

### **Paso 5: Deploy**
1. **Hacer clic en "Deploy"**
2. **Esperar a que termine el deployment**
3. **Verificar health checks**

---

## 🎯 **MÉTODO 3: DEPLOYMENT CON GITHUB ACTIONS**

### **Paso 1: Configurar Secrets en GitHub**
Ir a tu repositorio → **Settings** → **Secrets and variables** → **Actions**

Agregar estos secrets:
```bash
DOKPLOY_SERVER_URL=http://72.60.61.49:3000
DOKPLOY_API_TOKEN=tu-token-de-dokploy
DATABASE_URL=postgresql://vigoleonrocks:tu-password-seguro@postgres:5432/vigoleonrocks
REDIS_URL=redis://redis:6379
SECRET_KEY=tu-secret-key-unica
OPENROUTER_API_KEY=tu-api-key-openrouter
POSTGRES_PASSWORD=tu-password-seguro
```

### **Paso 2: Trigger Deployment**
```bash
# Hacer push a la rama main
git add .
git commit -m "Trigger deployment"
git push origin main
```

### **Paso 3: Monitorear**
El workflow `.github/workflows/dokploy-deploy.yml` se ejecutará automáticamente.

---

## 🔧 **CONFIGURACIÓN POST-DEPLOYMENT**

### **Verificar Servicios**
```bash
# Verificar estado de todos los servicios
curl http://72.60.61.49/api/status

# Verificar base de datos
curl http://72.60.61.49/api/health/db

# Verificar cache
curl http://72.60.61.49/api/health/redis
```

### **Configurar Dominio (Opcional)**
Si tienes un dominio personalizado:

1. **Ir a Project Settings** → **Domain**
2. **Configurar**:
   - **Domain**: `tu-dominio.com`
   - **SSL**: ✅ Enabled
   - **Redirect HTTPS**: ✅ Enabled

3. **Configurar DNS**:
   - **Tipo**: A
   - **Nombre**: `@` o `www`
   - **Valor**: `72.60.61.49`

### **Configurar Backups**
En **Project Settings** → **Backups**:
- **Database Backup**: ✅ Enabled (diario)
- **Volume Backup**: ✅ Enabled (semanal)

---

## 📊 **MONITOREO Y LOGS**

### **Dashboard de Dokploy**
- **URL**: `http://72.60.61.49:3000`
- **Ver logs**: Projects → vigoleonrocks → Logs
- **Ver métricas**: Projects → vigoleonrocks → Monitoring

### **Endpoints de Monitoreo**
```bash
# Estado general
GET http://72.60.61.49/api/status

# Métricas del sistema
GET http://72.60.61.49/api/quantum-metrics

# Historial de interacciones
GET http://72.60.61.49/api/interaction-history
```

---

## 🚨 **TROUBLESHOOTING**

### **Si el deployment falla**
1. **Verificar logs** en Dokploy dashboard
2. **Verificar variables de entorno**
3. **Verificar conectividad de red**
4. **Verificar límites de recursos del VPS**

### **Comandos Útiles**
```bash
# Ver logs de un servicio específico
docker logs <container-name>

# Reiniciar un servicio
docker restart <container-name>

# Ver estado de contenedores
docker ps

# Ver uso de recursos
docker stats
```

---

## 🎉 **DEPLOYMENT COMPLETADO**

### **URLs de Acceso**
- **Aplicación Principal**: `http://72.60.61.49`
- **API Status**: `http://72.60.61.49/api/status`
- **Dashboard Dokploy**: `http://72.60.61.49:3000`
- **Documentación API**: `http://72.60.61.49/`

### **Credenciales por Defecto**
- **Usuario Admin**: `admin@vigoleonrocks.com`
- **Password**: Cambiar después del primer login

### **Próximos Pasos Recomendados**
1. ✅ **Configurar dominio personalizado**
2. ✅ **Configurar SSL/TLS**
3. ✅ **Configurar backups automáticos**
4. ✅ **Configurar monitoreo avanzado**
5. ✅ **Optimizar recursos del VPS**

---

## 📞 **SOPORTE**

Si encuentras algún problema:

1. **Revisar logs** en Dokploy dashboard
2. **Verificar configuración** de variables de entorno
3. **Contactar soporte** si es necesario

**¡Tu VIGOLEONROCKS está listo para producción! 🚀**