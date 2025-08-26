# INSTALACIÓN SUPABASE CLI PARA VIGOLEONROCKS

## 🚀 Instalación de Supabase CLI en Windows

### Opción 1: NPM (Recomendado)

```powershell
# Instalar Supabase CLI globalmente
npm install -g supabase

# Verificar instalación
supabase --version
```

### Opción 2: Chocolatey

```powershell
# Si tienes Chocolatey instalado
choco install supabase

# Verificar instalación
supabase --version
```

### Opción 3: Descarga Directa

```powershell
# Descargar desde GitHub releases
# https://github.com/supabase/cli/releases
# Descargar supabase_windows_amd64.zip
# Extraer y agregar al PATH
```

## 🔧 Configuración Inicial

### 1. Login a Supabase

```powershell
# Hacer login
supabase login

# Te abrirá el navegador para autenticarte
```

### 2. Inicializar Proyecto

```powershell
# En tu directorio de proyecto
cd vigoleonrocks-ollama-model
supabase init
```

### 3. Vincular con tu Proyecto

```powershell
# Vincular con tu proyecto existente
supabase link --project-ref YOUR_PROJECT_REF

# Tu PROJECT_REF está en: Dashboard > Settings > General > Reference ID
```

## 📁 Estructura de Archivos para Edge Functions

```
vigoleonrocks-ollama-model/
├── supabase/
│   ├── functions/
│   │   └── vigoleonrocks/
│   │       └── index.ts
│   └── config.toml
├── supabase-edge-function.ts (archivo fuente)
└── supabase-setup-simple.sql
```

## 🚀 Desplegar Edge Function

### 1. Crear Edge Function

```powershell
# Crear nueva función
supabase functions new vigoleonrocks
```

### 2. Copiar Código

```powershell
# Copiar nuestro código a la función
copy supabase-edge-function.ts supabase\functions\vigoleonrocks\index.ts
```

### 3. Desplegar

```powershell
# Desplegar la función
supabase functions deploy vigoleonrocks

# Con logs en tiempo real
supabase functions deploy vigoleonrocks --debug
```

## 🧪 Probar Edge Function

### Test Local

```powershell
# Servir funciones localmente
supabase functions serve

# En otra terminal, probar
curl -X POST http://localhost:54321/functions/v1/vigoleonrocks ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Hola VIGOLEONROCKS\",\"sessionId\":\"test-001\"}"
```

### Test en Producción

```powershell
# Probar función desplegada
curl -X POST https://YOUR_PROJECT_REF.supabase.co/functions/v1/vigoleonrocks ^
  -H "Authorization: Bearer YOUR_ANON_KEY" ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Hola VIGOLEONROCKS desde Supabase XL\",\"sessionId\":\"prod-test-001\"}"
```

## 📊 Monitoreo

### Ver Logs

```powershell
# Ver logs de la función
supabase functions logs vigoleonrocks

# Logs en tiempo real
supabase functions logs vigoleonrocks --follow
```

### Estadísticas

```powershell
# Ver estadísticas de uso
supabase functions stats vigoleonrocks
```

## 🔑 Variables de Entorno

### Configurar Secrets

```powershell
# Configurar variables de entorno para la función
supabase secrets set CUSTOM_SECRET=your_value

# Ver secrets configurados
supabase secrets list
```

## 🛠️ Comandos Útiles

```powershell
# Ver todas las funciones
supabase functions list

# Eliminar función
supabase functions delete vigoleonrocks

# Ver configuración del proyecto
supabase status

# Sincronizar con proyecto remoto
supabase db pull

# Aplicar migraciones
supabase db push
```

## 🚨 Troubleshooting

### Error: Command not found

```powershell
# Verificar PATH
echo $env:PATH

# Reinstalar con npm
npm uninstall -g supabase
npm install -g supabase
```

### Error: Authentication

```powershell
# Logout y login nuevamente
supabase logout
supabase login
```

### Error: Project not linked

```powershell
# Verificar link
supabase status

# Re-vincular proyecto
supabase link --project-ref YOUR_PROJECT_REF
```

## 📋 Checklist de Instalación

- [ ] Supabase CLI instalado (`supabase --version`)
- [ ] Login exitoso (`supabase login`)
- [ ] Proyecto inicializado (`supabase init`)
- [ ] Proyecto vinculado (`supabase link`)
- [ ] Edge Function creada (`supabase functions new`)
- [ ] Código copiado a `supabase/functions/vigoleonrocks/index.ts`
- [ ] Función desplegada (`supabase functions deploy`)
- [ ] Test exitoso (local y producción)

¡Una vez completado este checklist, VIGOLEONROCKS estará completamente desplegado en tu Supabase XL!