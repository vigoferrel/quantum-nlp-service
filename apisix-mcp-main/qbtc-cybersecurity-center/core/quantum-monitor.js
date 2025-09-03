/**
 * Quantum Security Monitor
 * Monitorea y analiza la seguridad del sistema cuántico
 */

const QuantumSecurityProcessor = require('./quantum-processor');

class QuantumSecurityMonitor {
    constructor() {
        this.processor = new QuantumSecurityProcessor();
        this.alerts = [];
        this.metrics = new Map();
        this.thresholds = this.setupThresholds();
        this.monitoringActive = false;
        this.lastAnalysis = null;
    }

    // Configurar umbrales de seguridad
    setupThresholds() {
        return {
            coherence: {
                warning: 0.95,
                critical: 0.90
            },
            error_rate: {
                warning: '10^-5',
                critical: '10^-4'
            },
            entanglement_quality: {
                warning: 0.90,
                critical: 0.85
            },
            quantum_memory: {
                warning: 0.80, // 80% uso
                critical: 0.90 // 90% uso
            }
        };
    }

    // Iniciar monitoreo
    async startMonitoring() {
        if (this.monitoringActive) {
            return;
        }

        this.monitoringActive = true;
        console.log('🔍 Iniciando monitoreo cuántico de seguridad...');

        // Iniciar ciclo de monitoreo
        this.monitoringInterval = setInterval(() => {
            this.performSecurityCheck();
        }, 5000); // Cada 5 segundos
    }

    // Detener monitoreo
    stopMonitoring() {
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
        }
        this.monitoringActive = false;
        console.log('⏹️ Monitoreo cuántico detenido');
    }

    // Realizar verificación de seguridad
    async performSecurityCheck() {
        const metrics = this.processor.getProcessorMetrics();
        const quantumState = metrics.quantum_state;

        // Analizar coherencia
        if (quantumState.average_coherence < this.thresholds.coherence.critical) {
            this.raiseAlert('CRITICAL', 'Pérdida crítica de coherencia cuántica');
        } else if (quantumState.average_coherence < this.thresholds.coherence.warning) {
            this.raiseAlert('WARNING', 'Degradación de coherencia cuántica');
        }

        // Analizar tasa de errores
        const currentErrorRate = parseFloat(quantumState.error_rate.split('^')[1]);
        if (currentErrorRate > parseFloat(this.thresholds.error_rate.critical.split('^')[1])) {
            this.raiseAlert('CRITICAL', 'Tasa de errores cuánticos crítica');
        }

        // Verificar calidad de entrelazamiento
        const entanglements = Array.from(this.processor.stateManager.entanglements.values());
        const avgQuality = entanglements.reduce((acc, curr) => acc + curr.quality, 0) / entanglements.length;
        if (avgQuality < this.thresholds.entanglement_quality.critical) {
            this.raiseAlert('CRITICAL', 'Calidad de entrelazamiento crítica');
        }

        // Actualizar métricas
        this.updateMetrics({
            timestamp: Date.now(),
            coherence: quantumState.average_coherence,
            error_rate: quantumState.error_rate,
            entanglement_quality: avgQuality,
            alerts: this.alerts.length
        });

        this.lastAnalysis = Date.now();
    }

    // Levantar alerta
    raiseAlert(level, message) {
        const alert = {
            level,
            message,
            timestamp: Date.now(),
            quantum_state: this.processor.stateManager.getQuantumMetrics()
        };

        this.alerts.push(alert);
        console.log(`🚨 [${level}] ${message}`);

        // Limitar número de alertas almacenadas
        if (this.alerts.length > 1000) {
            this.alerts = this.alerts.slice(-1000);
        }

        return alert;
    }

    // Actualizar métricas
    updateMetrics(newMetrics) {
        const timeKey = Math.floor(Date.now() / 60000); // Por minuto
        this.metrics.set(timeKey, newMetrics);

        // Mantener solo última hora de métricas
        const cutoff = timeKey - 60;
        for (const [key] of this.metrics) {
            if (key < cutoff) {
                this.metrics.delete(key);
            }
        }
    }

    // Analizar patrones de amenazas
    async analyzeThreats() {
        const recentMetrics = Array.from(this.metrics.values());
        if (recentMetrics.length < 2) {
            return null;
        }

        // Detectar patrones usando quantum walk
        const patterns = await this.processor.runQuantumAlgorithm('quantum_walk', recentMetrics);

        return {
            timestamp: Date.now(),
            patterns: patterns.result.patterns,
            confidence: patterns.result.confidence,
            recommendations: this.generateRecommendations(patterns.result)
        };
    }

    // Generar recomendaciones basadas en análisis
    generateRecommendations(analysis) {
        const recommendations = [];

        if (analysis.periodic) {
            recommendations.push({
                type: 'PATTERN',
                message: 'Detectado patrón periódico en degradación de coherencia',
                action: 'Ajustar frecuencia de corrección de errores'
            });
        }

        if (analysis.symmetric) {
            recommendations.push({
                type: 'OPTIMIZATION',
                message: 'Patrón simétrico en uso de recursos cuánticos',
                action: 'Optimizar distribución de carga cuántica'
            });
        }

        return recommendations;
    }

    // Obtener estado actual del monitor
    getMonitorStatus() {
        return {
            active: this.monitoringActive,
            last_analysis: this.lastAnalysis,
            metrics: {
                current: Array.from(this.metrics.values()).pop(),
                historical: {
                    count: this.metrics.size,
                    timespan: `${this.metrics.size} minutos`
                }
            },
            alerts: {
                total: this.alerts.length,
                critical: this.alerts.filter(a => a.level === 'CRITICAL').length,
                warning: this.alerts.filter(a => a.level === 'WARNING').length,
                recent: this.alerts.slice(-5)
            },
            quantum_health: {
                coherence: this.processor.stateManager.getQuantumMetrics().average_coherence,
                error_rate: this.processor.stateManager.getQuantumMetrics().error_rate,
                entanglement_quality: Array.from(this.processor.stateManager.entanglements.values())
                    .reduce((acc, curr) => acc + curr.quality, 0) / 
                    Math.max(1, this.processor.stateManager.entanglements.size)
            }
        };
    }
}

module.exports = QuantumSecurityMonitor;
