# 🌐 CONFIGURACIÓN DNS PARA VIGOLEONROCKS.COM

## 📍 **INFORMACIÓN DEL VPS**
- **IP Address**: `72.60.61.49`
- **Hostname**: `srv984842.hstgr.cloud`
- **Dokploy URL**: `http://72.60.61.49:3000`

---

## 🔧 **CONFIGURACIÓN DNS EN HOSTINGER**

### **Acceder al Panel DNS**
1. **Ir a**: https://hpanel.hostinger.com/domain/vigoleonrocks.com/dns?tab=dns_records
2. **Seleccionar** el dominio `vigoleonrocks.com`
3. **Ir a la pestaña** "DNS Records"

### **Registros DNS Necesarios**

#### **1. Registro A (Principal)**
```
Type: A
Name: @
Value: 72.60.61.49
TTL: 14400 (4 horas)
```

#### **2. Registro A (www)**
```
Type: A
Name: www
Value: 72.60.61.49
TTL: 14400 (4 horas)
```

#### **3. Registro CNAME (Opcional - para subdominios)**
```
Type: CNAME
Name: api
Value: vigoleonrocks.com
TTL: 14400 (4 horas)
```

---

## ⚙️ **CONFIGURACIÓN EN DOKPLOY**

### **Después de configurar DNS**
1. **Ir al Dashboard Dokploy**: http://72.60.61.49:3000
2. **Seleccionar** el proyecto `vigoleonrocks`
3. **Ir a** Project Settings → Domain
4. **Configurar**:
   ```
   Domain: vigoleonrocks.com
   SSL: ✅ Enabled
   Redirect HTTPS: ✅ Enabled
   ```

### **URLs después de la configuración**
- **Sitio web**: `https://vigoleonrocks.com`
- **API**: `https://vigoleonrocks.com/api/status`
- **Dashboard Dokploy**: `http://72.60.61.49:3000`

---

## ⏱️ **TIEMPO DE PROPAGACIÓN**

### **Tiempo estimado**
- **DNS Propagation**: 24-48 horas
- **SSL Certificate**: 5-10 minutos (automático con Let's Encrypt)
- **Cache Clearing**: Inmediato

### **Verificar propagación**
```bash
# Verificar registro A
nslookup vigoleonrocks.com

# Verificar SSL
curl -I https://vigoleonrocks.com

# Verificar aplicación
curl https://vigoleonrocks.com/api/status
```

---

## 🚨 **TROUBLESHOOTING DNS**

### **Si el dominio no funciona**
1. **Verificar registros DNS**:
   ```bash
   dig vigoleonrocks.com
   ```

2. **Limpiar cache DNS**:
   ```bash
   # Windows
   ipconfig /flushdns

   # Linux/Mac
   sudo dscacheutil -flushcache
   ```

3. **Verificar en diferentes ubicaciones**:
   - https://dnschecker.org
   - https://whatismyipaddress.com/dns-lookup

### **Errores comunes**
- ❌ **Registro A apunta a IP incorrecta**
- ❌ **TTL muy alto** (demora en propagación)
- ❌ **Falta registro www**
- ❌ **DNS cache no actualizado**

---

## 🔒 **CONFIGURACIÓN SSL/TLS**

### **Certificado Automático**
Dokploy configura automáticamente SSL con Let's Encrypt:

1. **Después de configurar DNS** → Esperar 24 horas
2. **Dokploy detecta** el dominio válido
3. **Genera certificado** SSL automáticamente
4. **Configura renovación** automática

### **Verificar SSL**
```bash
# Verificar certificado
openssl s_client -connect vigoleonrocks.com:443 -servername vigoleonrocks.com

# Verificar en navegador
# https://vigoleonrocks.com (debe mostrar candado verde)
```

---

## 📊 **MONITOREO POST-DNS**

### **URLs a verificar**
```bash
# HTTP (redirige a HTTPS)
curl -I http://vigoleonrocks.com

# HTTPS (certificado válido)
curl -I https://vigoleonrocks.com

# API endpoints
curl https://vigoleonrocks.com/api/status
curl https://vigoleonrocks.com/api/quantum-metrics

# Web interface
curl https://vigoleonrocks.com/
```

### **Herramientas de monitoreo**
- **SSL Labs**: https://www.ssllabs.com/ssltest/
- **DNS Checker**: https://dnschecker.org
- **HTTP Status**: https://httpstatus.io

---

## 🎯 **PASOS FINALES**

### **Después de configurar DNS**
1. ✅ **Esperar 24-48 horas** para propagación
2. ✅ **Verificar SSL** automático
3. ✅ **Probar todos los endpoints**
4. ✅ **Configurar monitoreo** continuo
5. ✅ **Actualizar documentación** con URLs finales

### **URLs finales esperadas**
```
🌐 Sitio web: https://vigoleonrocks.com
🔗 API Base: https://vigoleonrocks.com/api/
📊 Dashboard: https://vigoleonrocks.com/dashboard/
📱 Admin: https://vigoleonrocks.com/admin/
```

---

## 📞 **SOPORTE**

Si tienes problemas con la configuración DNS:

1. **Verificar** que los registros estén correctos en Hostinger
2. **Esperar** el tiempo de propagación (24-48 horas)
3. **Limpiar cache** DNS local
4. **Contactar soporte** de Hostinger si es necesario

**¡Tu dominio vigoleonrocks.com estará listo para conquistar el mundo! 🚀**