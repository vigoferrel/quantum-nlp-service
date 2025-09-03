import { coherenceMonitor } from '../src/monitoring/QuantumCoherenceMonitor';
import { quantumLogger } from '../src/logging/QuantumLogger';
import { QUANTUM_MAINFRAME } from '../src/config/QuantumMainframeConstants';

interface CoherenceContext extends Record<string, unknown> {
    currentLevel: number;
    threshold: number;
    state: string;
}

interface OperationContext extends Record<string, unknown> {
    operation: string;
    timestamp: number;
}

interface RecoveryContext extends Record<string, unknown> {
    attempts: number;
    finalLevel: number;
}

interface OperationResultContext extends Record<string, unknown> {
    duration: number;
    coherenceLevel: number;
}

class QuantumIntegrationExample {
    private static readonly RECOVERY_ATTEMPTS = 3;
    private static readonly RECOVERY_DELAY = 1000;
    private isRunning = false;

    constructor() {
        this.setupEventHandlers();
    }

    private setupEventHandlers(): void {
        coherenceMonitor.on('alert:warning', (alert) => {
            const context: CoherenceContext = {
                currentLevel: alert.metrics.level,
                threshold: alert.threshold,
                state: alert.metrics.state
            };
            quantumLogger.warn('Nivel de coherencia bajo detectado', context);
            void this.attemptCoherenceRecovery(alert.metrics.level);
        });

        coherenceMonitor.on('alert:critical', (alert) => {
            const context: CoherenceContext = {
                currentLevel: alert.metrics.level,
                threshold: alert.threshold,
                state: alert.metrics.state
            };
            quantumLogger.error('Nivel de coherencia crítico', undefined, context);
            void this.emergencyShutdown();
        });

        quantumLogger.on('flush', (entries) => {
            console.log(`Procesados ${entries.length} registros cuánticos`);
        });

        quantumLogger.on('coherence:low', (data) => {
            console.warn('Alerta de coherencia baja:', data);
        });
    }

    public async start(): Promise<void> {
        try {
            this.isRunning = true;
            quantumLogger.info('Iniciando sistema cuántico integrado');

            coherenceMonitor.startMonitoring(1000);
            quantumLogger.info('Monitor de coherencia iniciado', {
                thresholds: coherenceMonitor.getThresholds()
            });

            await this.runQuantumOperations();

        } catch (error) {
            quantumLogger.error('Error durante el inicio del sistema', error as Error);
            await this.shutdown();
        }
    }

    private async runQuantumOperations(): Promise<void> {
        while (this.isRunning) {
            try {
                const metrics = coherenceMonitor.getMetrics();
                
                if (metrics.level > QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD) {
                    await this.performQuantumOperation();
                } else {
                    quantumLogger.warn('Esperando mejora en nivel de coherencia', {
                        currentLevel: metrics.level,
                        required: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD
                    });
                    await this.delay(1000);
                }

            } catch (error) {
                quantumLogger.error('Error en operación cuántica', error as Error);
                await this.delay(500);
            }
        }
    }

    private async performQuantumOperation(): Promise<void> {
        const metrics = coherenceMonitor.getMetrics();
        
        const opContext: OperationContext = {
            operation: 'quantum_transform',
            timestamp: Date.now()
        };
        quantumLogger.quantum('Iniciando operación cuántica', metrics, opContext);

        await this.delay(100);

        const resultContext: OperationResultContext = {
            duration: 100,
            coherenceLevel: metrics.level
        };
        quantumLogger.info('Operación cuántica completada exitosamente', resultContext);
    }

    private async attemptCoherenceRecovery(currentLevel: number): Promise<void> {
        for (let attempt = 1; attempt <= QuantumIntegrationExample.RECOVERY_ATTEMPTS; attempt++) {
            quantumLogger.info('Intentando recuperar coherencia', {
                attempt,
                currentLevel
            });

            await this.delay(QuantumIntegrationExample.RECOVERY_DELAY);

            const newMetrics = coherenceMonitor.getMetrics();
            if (newMetrics.level > QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD) {
                quantumLogger.info('Coherencia recuperada exitosamente', {
                    previousLevel: currentLevel,
                    newLevel: newMetrics.level
                });
                return;
            }
        }

        const errorContext: RecoveryContext = {
            attempts: QuantumIntegrationExample.RECOVERY_ATTEMPTS,
            finalLevel: coherenceMonitor.getMetrics().level
        };
        quantumLogger.error('No se pudo recuperar la coherencia', undefined, errorContext);
    }

    private async emergencyShutdown(): Promise<void> {
        quantumLogger.warn('Iniciando apagado de emergencia');
        await this.shutdown();
    }

    public async shutdown(): Promise<void> {
        this.isRunning = false;

        try {
            coherenceMonitor.stopMonitoring();
            quantumLogger.info('Monitor de coherencia detenido');

            await quantumLogger.destroy();
            console.log('Sistema apagado correctamente');

        } catch (error) {
            console.error('Error durante el apagado:', error);
        }
    }

    private delay(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

async function main(): Promise<void> {
    const integration = new QuantumIntegrationExample();
    
    process.on('SIGINT', async () => {
        console.log('\nRecibida señal de terminación');
        await integration.shutdown();
        process.exit(0);
    });

    await integration.start();
}

if (require.main === module) {
    void main().catch(console.error);
}

export { QuantumIntegrationExample };