# APISIX MCP - Sistema de Integración Cuántica

## Descripción

APISIX MCP es un sistema de integración que conecta APISIX con el sistema cuántico QBTC, proporcionando monitoreo de coherencia, logging avanzado y gestión de estados cuánticos.

## Características Principales

- Monitor de coherencia cuántica en tiempo real
- Sistema de logs con soporte para métricas cuánticas
- Integración con QBTC Mainframe
- Recuperación automática de estados incoherentes
- Tipos TypeScript completos
- Pruebas unitarias exhaustivas

## Requisitos

- Node.js >= 16.x
- TypeScript >= 4.x
- QBTC Mainframe >= 3.x

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/your-org/apisix-mcp.git

# Instalar dependencias
cd apisix-mcp
npm install
```

## Configuración

### Monitor de Coherencia

El monitor de coherencia se configura a través de `QuantumMainframeConstants.ts`:

```typescript
const QUANTUM_MAINFRAME = {
    CONFIG: {
        COHERENCE_THRESHOLD: 0.9997,
        PRECISION: 0.999,
        PROCESSING_TIME_PICOSECONDS: 10
    }
};
```

### Sistema de Logs

La configuración del sistema de logs se encuentra en `QuantumLoggingConfig.ts`:

```typescript
const QUANTUM_LOGGING_CONFIG = {
    BUFFER: {
        SIZE: 100,
        FLUSH_INTERVAL: 5000
    },
    PERSISTENCE: {
        ENABLED: true,
        TYPE: 'file',
        PATH: './logs/quantum'
    }
};
```

## Uso

### Inicialización Básica

```typescript
import { coherenceMonitor } from './monitoring/QuantumCoherenceMonitor';
import { quantumLogger } from './logging/QuantumLogger';

// Iniciar monitoreo
coherenceMonitor.startMonitoring(1000);

// Configurar handlers
coherenceMonitor.on('alert:warning', (alert) => {
    quantumLogger.warn('Nivel de coherencia bajo', {
        level: alert.metrics.level,
        threshold: alert.threshold
    });
});
```

### Integración Completa

Ver el ejemplo completo en `examples/quantum-integration.ts`:

```typescript
const integration = new QuantumIntegrationExample();
await integration.start();
```

## Monitoreo y Alertas

### Niveles de Coherencia

- **Normal**: > 0.9997
- **Advertencia**: > 0.95 y <= 0.9997
- **Crítico**: <= 0.95

### Tipos de Alertas

- `alert:warning`: Nivel de coherencia bajo
- `alert:critical`: Nivel de coherencia crítico
- `coherence:low`: Alerta general de coherencia baja

## Logging

### Niveles de Log

- `DEBUG`: Información de desarrollo
- `INFO`: Información general
- `WARN`: Advertencias
- `ERROR`: Errores
- `QUANTUM`: Eventos cuánticos específicos

### Ejemplo de Uso

```typescript
quantumLogger.quantum('Operación cuántica iniciada', metrics, {
    operation: 'quantum_transform',
    timestamp: Date.now()
});
```

## Manejo de Errores

El sistema implementa un manejo robusto de errores:

1. **Recuperación Automática**
   - Intentos configurables
   - Backoff exponencial
   - Logging de intentos

2. **Apagado Seguro**
   - Detención ordenada del monitoreo
   - Flush de logs pendientes
   - Limpieza de recursos

## Pruebas

```bash
# Ejecutar todas las pruebas
npm test

# Ejecutar pruebas específicas
npm test -- --grep "QuantumCoherenceMonitor"
```

## Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## Licencia

MIT - Ver [LICENSE](LICENSE) para más detalles.

## Soporte

Para soporte y consultas:

- Documentación: [docs/API.md](docs/API.md)
- Issues: [GitHub Issues](https://github.com/your-org/apisix-mcp/issues)
- Email: support@your-org.com

## Estado del Proyecto

- [x] Monitor de Coherencia
- [x] Sistema de Logs
- [x] Integración QBTC
- [x] Documentación
- [ ] Dashboard de Monitoreo
- [ ] Integración CI/CD
