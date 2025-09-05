# 🌐 **Configuración DNS para vigoleonrocks.com**

## 📋 **Información del Dominio**

- **Dominio**: vigoleonrocks.com
- **Proveedor**: Hostinger
- **Panel**: https://hpanel.hostinger.com/domain/vigoleonrocks.com/dns
- **Proyecto**: VIGOLEONROCKS - Quantum NLP Service

---

## 🔧 **Configuración DNS Requerida**

### **Registros A - Servicios Principales**

```dns
# Servicio Principal (API)
A    @                vigoleonrocks.com    [IP_SERVIDOR_DOKPLOY]
A    api              api.vigoleonrocks.com    [IP_SERVIDOR_DOKPLOY]

# Subdominios para servicios específicos
A    app              app.vigoleonrocks.com    [IP_SERVIDOR_DOKPLOY]
A    admin            admin.vigoleonrocks.com  [IP_SERVIDOR_DOKPLOY]
```

### **Registros CNAME - Servicios de Monitoreo**

```dns
# Servicios de Monitoreo
CNAME metrics          vigoleonrocks.com
CNAME prometheus       vigoleonrocks.com  
CNAME grafana          vigoleonrocks.com
CNAME monitor          vigoleonrocks.com

# Servicios de Desarrollo
CNAME docs             vigoleonrocks.com
CNAME dev              vigoleonrocks.com
CNAME staging          vigoleonrocks.com
```

### **Registros TXT - Verificación y Seguridad**

```dns
# Verificación de dominio
TXT  @    "v=spf1 include:_spf.hostinger.com ~all"

# Verificación de propiedad (si es requerida por Dokploy)
TXT  _dokploy    "dokploy-verification=[TOKEN_VERIFICACION]"

# Configuración DMARC (opcional)
TXT  _dmarc    "v=DMARC1; p=none; rua=mailto:vigoferrel@gmail.com"
```

---

## 🚀 **Configuración Específica para Dokploy**

### **1. Configuración Principal**

En el panel de Hostinger (https://hpanel.hostinger.com/domain/vigoleonrocks.com/dns):

#### **Registro A Principal**
```
Tipo: A
Nombre: @ (o dejar vacío)
Valor: [IP_SERVIDOR_DOKPLOY]
TTL: 3600
```

#### **Registro A para API**
```
Tipo: A  
Nombre: api
Valor: [IP_SERVIDOR_DOKPLOY]
TTL: 3600
```

### **2. Subdominios de Servicios**

#### **Grafana Dashboard**
```
Tipo: CNAME
Nombre: grafana
Valor: vigoleonrocks.com
TTL: 3600
```

#### **Prometheus Metrics**
```
Tipo: CNAME
Nombre: prometheus  
Valor: vigoleonrocks.com
TTL: 3600
```

#### **Monitoring Dashboard**
```
Tipo: CNAME
Nombre: metrics
Valor: vigoleonrocks.com
TTL: 3600
```

---

## 📊 **URLs de Servicios Configurados**

Después de la configuración DNS y despliegue:

### **Servicios Principales**
- **API Principal**: https://vigoleonrocks.com
- **API Endpoint**: https://api.vigoleonrocks.com  
- **Health Check**: https://vigoleonrocks.com/api/status
- **Documentación**: https://docs.vigoleonrocks.com

### **Monitoreo y Métricas**  
- **Grafana**: https://grafana.vigoleonrocks.com:3000
- **Prometheus**: https://prometheus.vigoleonrocks.com:9090
- **Métricas**: https://metrics.vigoleonrocks.com:8000
- **Monitor General**: https://monitor.vigoleonrocks.com

### **Desarrollo y Testing**
- **Staging**: https://staging.vigoleonrocks.com
- **Development**: https://dev.vigoleonrocks.com
- **Admin Panel**: https://admin.vigoleonrocks.com

---

## 🔐 **Configuración SSL/TLS**

### **Let's Encrypt en Dokploy**

1. **Habilitar SSL en Dokploy**:
   ```yaml
   SSL Configuration:
     Provider: Let's Encrypt
     Domain: vigoleonrocks.com
     Subdomains: 
       - api.vigoleonrocks.com
       - grafana.vigoleonrocks.com
       - prometheus.vigoleonrocks.com
   ```

2. **Certificados Wildcard** (recomendado):
   ```bash
   # Configurar certificado wildcard para todos los subdominios
   Domain: *.vigoleonrocks.com
   Include Root: true (vigoleonrocks.com)
   ```

### **Configuración de Redirección HTTP → HTTPS**

```yaml
# En docker-compose.yml o configuración Dokploy
SSL_REDIRECT: true
FORCE_HTTPS: true
HSTS_ENABLED: true
```

---

## ⚙️ **Configuración en Dokploy**

### **1. Configuración del Proyecto**

```yaml
Project Settings:
  Name: vigoleonrocks
  Domain: vigoleonrocks.com
  SSL: Enabled (Let's Encrypt)
  Environment: production
```

### **2. Variables de Entorno DNS**

```bash
# Configuración de dominio
DOMAIN_NAME=vigoleonrocks.com
SUBDOMAIN_API=api.vigoleonrocks.com
SUBDOMAIN_GRAFANA=grafana.vigoleonrocks.com
SUBDOMAIN_PROMETHEUS=prometheus.vigoleonrocks.com

# URLs completas para servicios
BASE_URL=https://vigoleonrocks.com
API_URL=https://api.vigoleonrocks.com
GRAFANA_URL=https://grafana.vigoleonrocks.com:3000
PROMETHEUS_URL=https://prometheus.vigoleonrocks.com:9090
```

### **3. Configuración de Puertos y Proxy**

```yaml
Port Mapping:
  80: 5000     # HTTP → API Principal
  443: 5000    # HTTPS → API Principal  
  3000: 3000   # Grafana Dashboard
  8000: 8000   # Métricas
  9090: 9090   # Prometheus

Reverse Proxy:
  grafana.vigoleonrocks.com → localhost:3000
  prometheus.vigoleonrocks.com → localhost:9090
  metrics.vigoleonrocks.com → localhost:8000
```

---

## 🧪 **Testing y Verificación**

### **1. Verificar Propagación DNS**

```bash
# Verificar registros A
nslookup vigoleonrocks.com
nslookup api.vigoleonrocks.com

# Verificar CNAME
nslookup grafana.vigoleonrocks.com
nslookup prometheus.vigoleonrocks.com

# Test desde diferentes servidores DNS
dig @8.8.8.8 vigoleonrocks.com
dig @1.1.1.1 vigoleonrocks.com
```

### **2. Test de Conectividad**

```bash
# Health check
curl -I https://vigoleonrocks.com/api/status

# SSL Certificate check  
curl -vI https://vigoleonrocks.com

# Métricas
curl https://vigoleonrocks.com:8000/metrics

# Servicios específicos
curl -I https://api.vigoleonrocks.com
```

### **3. Herramientas Online**

- **DNS Checker**: https://www.whatsmydns.net/#A/vigoleonrocks.com
- **SSL Test**: https://www.ssllabs.com/ssltest/analyze.html?d=vigoleonrocks.com
- **Website Test**: https://tools.pingdom.com/

---

## 🚨 **Troubleshooting DNS**

### **Problemas Comunes**

#### **1. DNS No Propaga**
```bash
# Verificar TTL y esperar tiempo necesario
# Limpiar cache DNS local
ipconfig /flushdns  # Windows
sudo dscacheutil -flushcache  # macOS
sudo systemctl restart systemd-resolved  # Linux
```

#### **2. SSL Certificate Issues**
```bash
# Verificar que el dominio resuelve correctamente antes de generar SSL
# Esperar propagación DNS completa (hasta 48 horas)
# Verificar que puerto 80 y 443 están abiertos
```

#### **3. Subdomain Not Working**
```bash
# Verificar registros CNAME en Hostinger panel
# Confirmar configuración de proxy reverso en Dokploy
# Verificar que servicios estén corriendo en puertos correctos
```

### **Comandos de Diagnóstico**

```bash
# Verificar resolución DNS completa
nslookup vigoleonrocks.com 8.8.8.8

# Test de conectividad TCP  
telnet vigoleonrocks.com 80
telnet vigoleonrocks.com 443

# Verificar certificado SSL
echo | openssl s_client -connect vigoleonrocks.com:443 -servername vigoleonrocks.com
```

---

## 📞 **Información de Soporte**

### **Contactos**
- **Dominio**: Hostinger Support
- **DNS**: Panel Hostinger (https://hpanel.hostinger.com)
- **Despliegue**: Configuración Dokploy
- **Proyecto**: vigoferrel@gmail.com

### **Recursos Útiles**
- **Hostinger DNS Docs**: https://support.hostinger.com/en/articles/1583227-how-to-manage-dns-records
- **Let's Encrypt**: https://letsencrypt.org/
- **DNS Propagation**: https://www.whatsmydns.net/

---

## ✅ **Checklist de Configuración DNS**

### **Pre-Configuración**
- [ ] Acceso al panel Hostinger confirmado
- [ ] IP del servidor Dokploy disponible
- [ ] Proyecto Dokploy configurado

### **Configuración DNS**
- [ ] Registro A principal (@) configurado
- [ ] Registro A para API configurado
- [ ] Registros CNAME para servicios configurados
- [ ] Registros TXT de verificación agregados

### **Post-Configuración**
- [ ] Propagación DNS verificada
- [ ] SSL/TLS certificados generados
- [ ] Health checks pasando
- [ ] Todos los servicios accesibles
- [ ] Redirección HTTPS funcionando

---

**🌐 "Conectando VIGOLEONROCKS al mundo con infraestructura DNS robusta y segura"**

*Configuración DNS VIGOLEONROCKS • Dominio: vigoleonrocks.com • Actualizada: Septiembre 2025*
