import { EventEmitter } from 'events';
import { QuantumMetrics } from '../monitoring/QuantumCoherenceMonitor';
import { QUANTUM_LOGGING_CONFIG } from '../config/QuantumLoggingConfig';

export interface QuantumLogEntry {
    timestamp: number;
    level: keyof typeof QUANTUM_LOGGING_CONFIG.LEVELS;
    message: string;
    coherenceMetrics?: QuantumMetrics;
    context?: Record<string, unknown>;
    source?: string;
}

class QuantumLogger extends EventEmitter {
    private static instance: QuantumLogger;
    private logBuffer: QuantumLogEntry[] = [];
    private readonly config: typeof QUANTUM_LOGGING_CONFIG;
    private flushTimer?: NodeJS.Timeout;

    private constructor() {
        super();
        this.config = QUANTUM_LOGGING_CONFIG;
        this.startFlushTimer();
    }

    public static getInstance(): QuantumLogger {
        if (!QuantumLogger.instance) {
            QuantumLogger.instance = new QuantumLogger();
        }
        return QuantumLogger.instance;
    }

    private startFlushTimer(): void {
        if (this.flushTimer) {
            clearInterval(this.flushTimer);
        }
        this.flushTimer = setInterval(() => this.flush(), this.config.BUFFER.FLUSH_INTERVAL);
    }

    private createLogEntry(
        level: keyof typeof QUANTUM_LOGGING_CONFIG.LEVELS,
        message: string,
        coherenceMetrics?: QuantumMetrics,
        context?: Record<string, unknown>,
        source?: string
    ): QuantumLogEntry {
        return {
            timestamp: Date.now(),
            level,
            message,
            coherenceMetrics,
            context,
            source
        };
    }

    private async flush(): Promise<void> {
        if (this.logBuffer.length === 0) return;

        const entries = [...this.logBuffer];
        this.logBuffer = [];

        try {
            // Emitir evento para que los consumidores procesen las entradas
            this.emit('flush', entries);

            // Guardar en almacenamiento persistente si está configurado
            if (this.config.PERSISTENCE.ENABLED) {
                await this.persistLogs(entries);
            }
        } catch (error) {
            console.error('Error al procesar logs cuánticos:', error);
            // Reintentar con backoff exponencial
            this.logBuffer = [...entries, ...this.logBuffer];
        }
    }

    private async persistLogs(entries: QuantumLogEntry[]): Promise<void> {
        // Implementar persistencia según configuración
        // Por ejemplo: archivo, base de datos, servicio externo
        this.emit('persist', entries);
    }

    public log(
        level: keyof typeof QUANTUM_LOGGING_CONFIG.LEVELS,
        message: string,
        coherenceMetrics?: QuantumMetrics,
        context?: Record<string, unknown>,
        source?: string
    ): void {
        const entry = this.createLogEntry(level, message, coherenceMetrics, context, source);
        
        // Verificar nivel de coherencia si está habilitado
        if (this.config.FORMAT.INCLUDE_COHERENCE && coherenceMetrics) {
            if (coherenceMetrics.level < this.config.COHERENCE.MIN_LEVEL && this.config.COHERENCE.ALERT_ON_LOW) {
                this.emit('coherence:low', {
                    timestamp: Date.now(),
                    level: coherenceMetrics.level,
                    threshold: this.config.COHERENCE.MIN_LEVEL
                });
            }
        }

        this.logBuffer.push(entry);

        // Emitir evento para procesamiento en tiempo real
        this.emit('log', entry);

        // Forzar flush si el buffer está lleno
        if (this.logBuffer.length >= this.config.BUFFER.SIZE) {
            this.flush();
        }
    }

    public quantum(
        message: string,
        coherenceMetrics: QuantumMetrics,
        context?: Record<string, unknown>,
        source?: string
    ): void {
        this.log('QUANTUM', message, coherenceMetrics, context, source);
    }

    public debug(message: string, context?: Record<string, unknown>, source?: string): void {
        this.log('DEBUG', message, undefined, context, source);
    }

    public info(message: string, context?: Record<string, unknown>, source?: string): void {
        this.log('INFO', message, undefined, context, source);
    }

    public warn(message: string, context?: Record<string, unknown>, source?: string): void {
        this.log('WARN', message, undefined, context, source);
    }

    public error(message: string, error?: Error, context?: Record<string, unknown>, source?: string): void {
        const errorContext = error ? {
            ...context,
            error: {
                name: error.name,
                message: error.message,
                stack: error.stack
            }
        } : context;

        this.log('ERROR', message, undefined, errorContext, source);
    }

    public async destroy(): Promise<void> {
        if (this.flushTimer) {
            clearInterval(this.flushTimer);
        }
        await this.flush();
        this.removeAllListeners();
    }
}

export const quantumLogger = QuantumLogger.getInstance();