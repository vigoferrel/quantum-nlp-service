# 🚀 **VIGOLEONROCKS - Guía de Despliegue en Dokploy**

## 📋 **Información General**

- **Proyecto**: VIGOLEONROCKS - Quantum NLP Service
- **Versión**: 2.1.0-supreme
- **Fecha**: Septiembre 2025
- **Repositorio**: https://github.com/vigoferrel/quantum-nlp-service

---

## 🔧 **Preparativos Previos**

### **1. Verificar Archivos de Configuración**
Asegúrate de que estos archivos estén actualizados en el repositorio:
- ✅ `docker-compose.yml` - Configuración completa de servicios
- ✅ `Dockerfile` - Imagen optimizada para producción
- ✅ `.env.docker` - Variables de entorno de ejemplo
- ✅ `deploy-dokploy.sh` - Script de preparación de despliegue

### **2. Preparar Variables de Entorno Seguras**
Genera credenciales seguras para los siguientes servicios:

```bash
# Variables obligatorias
POSTGRES_PASSWORD=tu_password_postgres_muy_seguro_aqui
SECRET_KEY=tu_clave_secreta_32_caracteres_minimo
GRAFANA_PASSWORD=tu_password_grafana_seguro_aqui

# Variables opcionales
OPENROUTER_API_KEY=tu_api_key_openrouter_opcional
```

---

## 🌐 **Configuración en Dokploy**

### **Paso 1: Crear Nuevo Proyecto**

1. **Acceder al Dashboard de Dokploy**
   - Ir a: `https://tu-dokploy-instance.com`
   - Iniciar sesión con tus credenciales

2. **Crear Proyecto**
   - Click en "**New Project**"
   - Nombre: `vigoleonrocks`
   - Descripción: `VIGOLEONROCKS - Quantum NLP Service`

### **Paso 2: Configurar Repositorio Git**

1. **Conectar Repositorio**
   - Repository URL: `https://github.com/vigoferrel/quantum-nlp-service.git`
   - Branch: `main`
   - Deployment type: **Docker Compose**

2. **Configurar Build Settings**
   - Build Command: `docker-compose build`
   - Compose File: `docker-compose.yml`
   - Environment: `production`

### **Paso 3: Configurar Variables de Entorno**

En la sección **Environment Variables**, agregar:

#### **Variables de Seguridad (Obligatorias)**
```bash
NODE_ENV=production
FLASK_ENV=production
POSTGRES_PASSWORD=[TU_PASSWORD_POSTGRES]
SECRET_KEY=[TU_SECRET_KEY_32_CHARS]
GRAFANA_PASSWORD=[TU_PASSWORD_GRAFANA]
```

#### **Políticas VIGOLEONROCKS (Obligatorias)**
```bash
BACKGROUND_EXECUTION=true
PROMETHEUS_ENABLED=true
METRICS_RNG_ENABLED=true
SYSTEM_ENTROPY_ENABLED=true
MATH_RANDOM_DISABLED=true
QUANTUM_PROCESSOR_ENABLED=true
```

#### **Base de Datos**
```bash
POSTGRES_DB=vigoleonrocks_db
POSTGRES_USER=vigoleonrocks
DATABASE_URL=postgresql://vigoleonrocks:${POSTGRES_PASSWORD}@postgres:5432/vigoleonrocks_db
REDIS_URL=redis://redis:6379/0
```

#### **Configuración de Performance**
```bash
GUNICORN_WORKERS=4
GUNICORN_THREADS=2
MAX_CONTEXT_LENGTH=500000
QUANTUM_DIMENSIONS=26
```

#### **API Keys (Opcional)**
```bash
OPENROUTER_API_KEY=[TU_OPENROUTER_KEY_OPCIONAL]
```

### **Paso 4: Configurar Dominio y SSL**

1. **Configurar Dominio**
   - Domain: `vigoleonrocks.com`
   - Enable SSL: ✅ **Activado**
   - SSL Provider: Let's Encrypt

2. **Configurar Puertos**
   - **Puerto Principal**: 5000 (API)
   - **Puerto Métricas**: 8000 (Monitoring)
   - **Puerto Prometheus**: 9090 (Metrics Collection)
   - **Puerto Grafana**: 3000 (Dashboard)

### **Paso 5: Configurar Health Checks**

```yaml
Health Check:
  Path: /api/status
  Port: 5000
  Interval: 30s
  Timeout: 10s
  Retries: 3
```

---

## 🚀 **Proceso de Despliegue**

### **1. Despliegue Inicial**

1. **Deploy**
   - Click en "**Deploy**" en el dashboard de Dokploy
   - Esperar a que se complete el build (5-10 minutos aproximadamente)

2. **Verificar Logs**
   - Monitorear logs durante el despliegue
   - Verificar que todos los servicios se inicien correctamente

### **2. Verificación Post-Despliegue**

#### **Verificar Servicios**
```bash
# API Principal
curl https://vigoleonrocks.com/api/status

# Métricas
curl https://vigoleonrocks.com:8000/metrics

# Prometheus
https://vigoleonrocks.com:9090

# Grafana
https://vigoleonrocks.com:3000
```

#### **Verificar Base de Datos**
- Verificar que PostgreSQL esté ejecutándose
- Confirmar que las tablas se crearon correctamente
- Verificar conexión de Redis

#### **Verificar Políticas**
- ✅ Procesos ejecutándose en segundo plano
- ✅ Métricas de performance habilitadas
- ✅ Sistema de entropía basado en métricas del sistema
- ✅ Prohibición de Math.random activa

---

## 📊 **Monitoreo y Mantenimiento**

### **Acceso a Dashboards**

1. **Grafana Dashboard**
   - URL: `https://vigoleonrocks.com:3000`
   - Usuario: `admin`
   - Password: `[TU_GRAFANA_PASSWORD]`

2. **Prometheus Metrics**
   - URL: `https://vigoleonrocks.com:9090`
   - Acceso directo a métricas del sistema

### **Logs y Debugging**

```bash
# Ver logs en tiempo real en Dokploy
- Acceder a la sección "Logs" del proyecto
- Filtrar por servicio específico
- Monitorear errores y performance
```

### **Backup y Recuperación**

- **Database Backup**: Configurado automáticamente cada 24 horas
- **Logs Retention**: 30 días
- **Metrics Retention**: 200 horas

---

## 🔄 **Actualizaciones y Re-despliegue**

### **Actualización de Código**

1. **Push al Repositorio**
   ```bash
   git add .
   git commit -m "feat: update deployment configuration"
   git push origin main
   ```

2. **Re-deploy en Dokploy**
   - El webhook automáticamente detectará cambios
   - O hacer click manual en "**Deploy**"

### **Actualización de Variables de Entorno**

1. Ir a configuración del proyecto en Dokploy
2. Actualizar variables en la sección "Environment Variables"
3. Hacer re-deploy para aplicar cambios

---

## 🚨 **Troubleshooting**

### **Problemas Comunes**

#### **1. Error de Build**
```bash
# Verificar Dockerfile y docker-compose.yml
# Revisar logs de build en Dokploy
# Asegurar que todas las dependencias estén en requirements.txt
```

#### **2. Error de Base de Datos**
```bash
# Verificar POSTGRES_PASSWORD
# Confirmar que el servicio PostgreSQL esté corriendo
# Revisar logs del contenedor postgres
```

#### **3. Error de Variables de Entorno**
```bash
# Verificar que todas las variables obligatorias estén configuradas
# Confirmar formato correcto de las variables
# Revisar logs de la aplicación para errores específicos
```

#### **4. Error de Health Check**
```bash
# Verificar que el endpoint /api/status responda
# Confirmar que el puerto 5000 esté disponible
# Revisar logs del servicio principal
```

### **Comandos de Diagnóstico**

```bash
# Health check manual
curl -f https://vigoleonrocks.com/api/status

# Verificar métricas
curl https://vigoleonrocks.com:8000/metrics

# Test de conectividad
nslookup vigoleonrocks.com
```

---

## 📞 **Soporte y Contacto**

### **Canales de Soporte**
- **GitHub Issues**: https://github.com/vigoferrel/quantum-nlp-service/issues
- **Email**: vigoferrel@gmail.com
- **Documentación**: Ver archivos README.md y ARCHITECTURE.md

### **Información para Reportar Problemas**
1. **Logs del sistema** (disponibles en Dokploy)
2. **Variables de entorno configuradas** (sin passwords)
3. **Versión desplegada** (2.1.0-supreme)
4. **Descripción detallada del problema**
5. **Pasos para reproducir el error**

---

## ✅ **Checklist de Despliegue**

### **Pre-Despliegue**
- [ ] Repositorio actualizado en GitHub
- [ ] Variables de entorno seguras generadas
- [ ] Dockerfile y docker-compose.yml validados
- [ ] Dominio configurado y DNS apuntando

### **Durante el Despliegue**
- [ ] Proyecto creado en Dokploy
- [ ] Repositorio Git conectado
- [ ] Variables de entorno configuradas
- [ ] SSL habilitado
- [ ] Health checks configurados
- [ ] Build completado sin errores

### **Post-Despliegue**
- [ ] API principal responde correctamente
- [ ] Base de datos inicializada
- [ ] Métricas disponibles en Prometheus
- [ ] Grafana dashboard accesible
- [ ] Health checks pasando
- [ ] Logs sin errores críticos
- [ ] Políticas VIGOLEONROCKS aplicadas

---

**🌌 "Desplegando el futuro de la IA cuántica con infraestructura robusta y monitoreo completo"**

*Guía de Despliegue VIGOLEONROCKS • Versión: 2.1.0-supreme • Actualizada: Septiembre 2025*

<citations>
<document>
    <document_type>RULE</document_type>
    <document_id>OOXRPDT0m0MVsz2xUFKDTQ</document_id>
</document>
</citations>
