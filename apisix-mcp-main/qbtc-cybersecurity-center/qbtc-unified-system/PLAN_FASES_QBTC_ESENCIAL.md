# 🎯 PLAN DE FASES QBTC - ESENCIAL
**Principio: "Menos es Más" - Solo las acciones críticas de mayor impacto**

---

## 🚀 FASE 1: ACTIVAR EL CEREBRO (1 día)
**Objetivo:** Resolver conexión Ollama → Benchmark de 0% a >50%

### Acciones Críticas:
1. **Configurar Ollama para conexiones externas:**
   ```bash
   ollama serve --host 0.0.0.0 --port 11434
   ```

2. **Abrir firewall Windows:**
   ```bash
   netsh advfirewall firewall add rule name="Ollama-Docker" dir=in action=allow protocol=TCP localport=11434
   ```

3. **Verificar conexión:**
   ```bash
   docker exec quantum-consciousness-core-simple curl http://host.docker.internal:11434/api/version
   ```

**Métrica de Éxito:** Benchmark accuracy >50%

---

## 🔧 FASE 2: UNIFICAR ECOSISTEMA (3 días)
**Objetivo:** Migrar Quantum Core 26D completo al directorio QBTC-CIO actual

### Acciones Críticas:
1. **Copiar implementación completa:**
   ```bash
   cp ../vigosueldo/localGPT-main/quantum_consciousness_core_26d.py ./services/quantum-core-service/
   ```

2. **Actualizar imports y dependencias**
3. **Integrar con tool_dispatcher.py existente**
4. **Crear docker-compose.yml unificado**

**Métrica de Éxito:** Un solo directorio con sistema 100% funcional

---

## ⚡ FASE 3: OPTIMIZACIÓN CRÍTICA (2 días)
**Objetivo:** Preparar para producción solo lo esencial

### Acciones Críticas:
1. **Health checks robustos**
2. **Variables de entorno documentadas**
3. **Logging estructurado**
4. **README de despliegue simple**

**Métrica de Éxito:** Sistema desplegable en cualquier entorno

---

## 📊 CRONOGRAMA TOTAL: 6 DÍAS

| Fase | Días | Impacto | Prioridad |
|------|------|---------|-----------|
| 1    | 1    | Alto    | CRÍTICA   |
| 2    | 3    | Alto    | CRÍTICA   |
| 3    | 2    | Medio   | NORMAL    |

---

## ✅ ENTREGABLES FINALES

1. **Sistema QBTC unificado y funcional**
2. **Benchmark accuracy >70%**
3. **Documentación de despliegue**

**No se incluyen:** Microservicios complejos, sistema iónico avanzado, optimizaciones prematuras

---

*Planificación basada en principio "Menos es Más" - Máximo impacto con mínima complejidad*