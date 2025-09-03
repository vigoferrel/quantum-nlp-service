/**
 * Port Configuration for QBTC Quantum Unified Security System
 * Configuración centralizada de puertos para el sistema
 */

const PORTS = {
    // Core Services (7000-7099)
    QUANTUM_CORE: {
        MAIN: 7000,           // Servicio principal cuántico
        STATE_MANAGER: 7001,  // Gestor de estados cuánticos
        PROCESSOR: 7002,      // Procesador cuántico
        MONITOR: 7003         // Monitor cuántico
    },

    // Security Services (7100-7199)
    SECURITY: {
        MAIN: 7100,           // Servicio principal de seguridad
        QUANTUM_FIREWALL: 7101, // Firewall cuántico
        IDS: 7102,            // Sistema de detección de intrusiones
        AUDIT: 7103          // Sistema de auditoría
    },

    // APIs (7200-7299)
    API: {
        GATEWAY: 7200,        // API Gateway principal
        QUANTUM: 7201,        // API de servicios cuánticos
        SECURITY: 7202,       // API de seguridad
        METRICS: 7203         // API de métricas
    },

    // Monitoring & Health (7300-7399)
    MONITORING: {
        HEALTH: 7300,         // Healthcheck endpoints
        METRICS: 7301,        // Métricas del sistema
        ALERTS: 7302,         // Sistema de alertas
        LOGS: 7303           // Sistema de logs
    },

    // Web Interfaces (7400-7499)
    WEB: {
        DASHBOARD: 7400,      // Dashboard principal
        ADMIN: 7401,         // Panel de administración
        REPORTS: 7402        // Sistema de reportes
    },

    // Utility Functions
    isPortAvailable: async (port) => {
        try {
            const net = require('net');
            return new Promise((resolve) => {
                const server = net.createServer();
                server.once('error', () => resolve(false));
                server.once('listening', () => {
                    server.close();
                    resolve(true);
                });
                server.listen(port);
            });
        } catch (error) {
            return false;
        }
    },

    // Validar puerto específico
    validatePort: async (port) => {
        if (port < 1024 || port > 65535) {
            throw new Error(`Puerto ${port} fuera del rango válido (1024-65535)`);
        }
        const available = await PORTS.isPortAvailable(port);
        if (!available) {
            throw new Error(`Puerto ${port} no disponible`);
        }
        return true;
    },

    // Validar todos los puertos del sistema
    validateAllPorts: async () => {
        const usedPorts = new Set();
        const errors = [];

        // Función recursiva para validar puertos en objeto anidado
        const validatePortsRecursive = async (obj) => {
            for (const key in obj) {
                if (typeof obj[key] === 'number') {
                    // Es un puerto
                    const port = obj[key];
                    
                    // Verificar rango válido
                    if (port < 1024 || port > 65535) {
                        errors.push(`Puerto ${port} (${key}) fuera del rango válido (1024-65535)`);
                        continue;
                    }

                    // Verificar duplicados
                    if (usedPorts.has(port)) {
                        errors.push(`Puerto ${port} (${key}) duplicado`);
                        continue;
                    }

                    // Verificar disponibilidad
                    const available = await PORTS.isPortAvailable(port);
                    if (!available) {
                        errors.push(`Puerto ${port} (${key}) no disponible`);
                        continue;
                    }

                    usedPorts.add(port);
                } else if (typeof obj[key] === 'object' && !Array.isArray(obj[key]) && obj[key] !== null) {
                    // Es un objeto anidado, validar recursivamente
                    await validatePortsRecursive(obj[key]);
                }
            }
        };

        await validatePortsRecursive(PORTS);

        if (errors.length > 0) {
            throw new Error('Errores en la validación de puertos:\n' + errors.join('\n'));
        }

        return true;
    },

    // Obtener siguiente puerto disponible en un rango
    getNextAvailablePort: async (startPort, endPort) => {
        for (let port = startPort; port <= endPort; port++) {
            if (await PORTS.isPortAvailable(port)) {
                return port;
            }
        }
        throw new Error(`No hay puertos disponibles en el rango ${startPort}-${endPort}`);
    },

    // Obtener todos los puertos en uso
    getUsedPorts: () => {
        const usedPorts = new Set();
        
        const getPortsRecursive = (obj) => {
            for (const key in obj) {
                if (typeof obj[key] === 'number') {
                    usedPorts.add(obj[key]);
                } else if (typeof obj[key] === 'object' && !Array.isArray(obj[key]) && obj[key] !== null) {
                    getPortsRecursive(obj[key]);
                }
            }
        };

        getPortsRecursive(PORTS);
        return Array.from(usedPorts).sort((a, b) => a - b);
    }
};

module.exports = PORTS;
