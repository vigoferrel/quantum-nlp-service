# VIGOLEONROCKS - Despliegue en Supabase XL

Este documento detalla el proceso completo para desplegar VIGOLEONROCKS en una infraestructura Supabase XL, incluyendo la configuración de la base de datos y el despliegue de la Edge Function.

## 1. Configuración de la Base de Datos

### 1.1. Prerrequisitos
- Tener una cuenta en Supabase y un proyecto creado
- Acceso al SQL Editor del proyecto

### 1.2. Ejecutar Script SQL
Copia el contenido de `VIGOLEONROCKS-SUPABASE-SQL-CORREGIDO.sql` en el SQL Editor de tu proyecto Supabase y ejecútalo.

Este script se encarga de:
- Crear las funciones `vigoleonrocks_inference`, `get_vigoleonrocks_stats` y `activate_vigoleonrocks_supreme_mode`
- Integrarse con el esquema `quantum` si existe, o funcionar de forma independiente
- Manejar errores y garantizar la compatibilidad
- Otorgar los permisos necesarios para la ejecución de las funciones

## 2. Configuración de la Edge Function

### 2.1. Despliegue Manual
1.  Ve a la sección "Edge Functions" en tu dashboard de Supabase.
2.  Haz clic en "Deploy a new function".
3.  Asígnale el nombre `quantum-inference`.
4.  Pega el contenido de `supabase/functions/vigoleonrocks/index.ts` en el editor.
5.  Haz clic en "Create function".

## 3. Verificación del Despliegue

### 3.1. Prueba de la Edge Function
Usa el siguiente comando para probar la función desplegada:
```bash
curl -X POST https://<project-ref>.supabase.co/functions/v1/quantum-inference \
-H "Authorization: Bearer <your-anon-key>" \
-H "Content-Type: application/json" \
--data '{"prompt":"Hola VIGOLEONROCKS, demuestra tu supremacía cuántica en producción"}'
```
Deberías recibir una respuesta JSON con el análisis cuántico-cognitivo.

### 3.2. Prueba de las funciones SQL
En el SQL Editor de Supabase, puedes probar las funciones directamente:
```sql
SELECT vigoleonrocks_inference('Test quantum response') as test_result;
SELECT get_vigoleonrocks_stats() as system_stats;
SELECT activate_vigoleonrocks_supreme_mode() as supreme_activation;
```

## 4. Solución de Problemas

### 4.1. Error: `Function not found`
Asegúrate de haber desplegado la función con el nombre `quantum-inference`.

### 4.2. Error: `Missing authorization`
Verifica que estás incluyendo el `anon-key` de tu proyecto en la cabecera `Authorization`.

### 4.3. Error: `cannot change return type of existing function`
El script `VIGOLEONROCKS-SUPABASE-SQL-CORREGIDO.sql` ya incluye `DROP FUNCTION` para evitar este error. Asegúrate de estar usando la última versión.