# 🌐 CONFIGURACIÓN DNS PARA MIGRACIÓN COMPLETA

## 📋 INSTRUCCIONES PARA CONFIGURAR DNS

### 🎯 **OBJETIVO:**
Configurar el dominio `vigoleonrocks.com` para que apunte al VPS y completar la migración.

### 🔧 **CONFIGURACIÓN DNS REQUERIDA:**

#### **En tu panel de control del dominio (vigoleonrocks.com):**

```
Tipo    Nombre              Valor                    TTL
A       @                  72.60.61.49             3600
A       www                72.60.61.49             3600
A       api                72.60.61.49             3600
CNAME   *.vigoleonrocks.com vigoleonrocks.com       3600
```

#### **Explicación:**
- **A Record (@)**: Apunta el dominio principal al VPS
- **A Record (www)**: Apunta www.vigoleonrocks.com al VPS
- **A Record (api)**: Apunta api.vigoleonrocks.com al VPS
- **CNAME (*)**: Redirige todos los subdominios al dominio principal

### 📍 **PASOS EN EL PANEL DE CONTROL:**

1. **Acceder al panel de control** del dominio vigoleonrocks.com
2. **Buscar la sección DNS** o "Zone Editor"
3. **Eliminar registros existentes** que apunten al Cloud Hosting
4. **Agregar los nuevos registros** mostrados arriba
5. **Guardar los cambios**
6. **Esperar propagación** (5-30 minutos)

### ⏱️ **TIEMPO DE PROPAGACIÓN:**
- **Propagación local**: 5-15 minutos
- **Propagación global**: 30-60 minutos
- **Verificación**: Usar `nslookup vigoleonrocks.com`

### 🧪 **COMANDOS DE VERIFICACIÓN:**

```bash
# Verificar DNS local
nslookup vigoleonrocks.com

# Verificar desde diferentes ubicaciones
dig vigoleonrocks.com @8.8.8.8
dig vigoleonrocks.com @1.1.1.1

# Verificar conectividad
ping vigoleonrocks.com
curl -I https://vigoleonrocks.com
```

### 🚀 **EJECUTAR MIGRACIÓN EN EL VPS:**

Una vez configurado el DNS, ejecutar en el VPS:

```bash
# Hacer ejecutable el script
chmod +x /root/migracion_completa_vps.sh

# Ejecutar migración completa
/root/migracion_completa_vps.sh
```

### 📊 **VERIFICACIÓN POST-MIGRACIÓN:**

```bash
# Verificar sitio web
curl -I https://vigoleonrocks.com

# Verificar API
curl -s https://vigoleonrocks.com/api/status

# Verificar SSL
openssl s_client -connect vigoleonrocks.com:443

# Monitorear sistema
/var/www/vigoleonrocks.com/monitor_migration.sh
```

### 🎯 **RESULTADO ESPERADO:**

Después de la migración completa:
- ✅ **vigoleonrocks.com** → VPS (72.60.61.49)
- ✅ **SSL funcionando** (Let's Encrypt)
- ✅ **API Python** funcionando
- ✅ **Contenido migrado** del Cloud Hosting
- ✅ **Monitoreo configurado**
- ✅ **Costos optimizados** (eliminar Cloud Hosting)

### 💰 **BENEFICIOS:**

- **Reducción de costos**: Eliminar Cloud Hosting
- **Arquitectura simplificada**: Un solo servidor
- **Mejor rendimiento**: Python Flask optimizado
- **Control total**: Gestión completa del entorno
- **Escalabilidad**: Fácil expansión futura

### ⚠️ **IMPORTANTE:**

1. **Hacer backup** del Cloud Hosting antes de cancelar
2. **Verificar funcionamiento** completo antes de cancelar
3. **Monitorear** durante las primeras 24 horas
4. **Documentar** la nueva arquitectura

### 🔧 **SOPORTE:**

Si hay problemas durante la migración:
- Verificar logs: `/var/log/apache2/error.log`
- Verificar Python: `/var/www/vigoleonrocks.com/logs/`
- Ejecutar monitoreo: `./monitor_migration.sh`
- Reiniciar servicios: `systemctl restart apache2`
