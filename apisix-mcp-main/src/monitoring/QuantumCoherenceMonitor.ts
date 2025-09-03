import { EventEmitter } from 'events';
import { QUANTUM_MAINFRAME } from '../config/QuantumMainframeConstants';
import { QuantumError } from '../quantum-types/QuantumTypes';

export interface QuantumMetrics {
    level: number;
    frequency: number;
    state: string;
    timestamp: number;
}

export interface CoherenceThresholds {
    warning: number;
    critical: number;
}

export interface CoherenceAlert {
    type: 'WARNING' | 'CRITICAL';
    metrics: QuantumMetrics;
    threshold: number;
    timestamp: number;
}

class QuantumCoherenceMonitor extends EventEmitter {
    private static instance: QuantumCoherenceMonitor;
    private metrics: QuantumMetrics;
    private thresholds: CoherenceThresholds;
    private monitoringInterval?: NodeJS.Timeout;
    private isMonitoring: boolean = false;

    private constructor() {
        super();
        this.metrics = {
            level: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD,
            frequency: QUANTUM_MAINFRAME.FREQUENCY,
            state: QUANTUM_MAINFRAME.STATES.COHERENT,
            timestamp: Date.now()
        };

        this.thresholds = {
            warning: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.95,
            critical: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.90
        };
    }

    public static getInstance(): QuantumCoherenceMonitor {
        if (!QuantumCoherenceMonitor.instance) {
            QuantumCoherenceMonitor.instance = new QuantumCoherenceMonitor();
        }
        return QuantumCoherenceMonitor.instance;
    }

    public startMonitoring(interval: number = 1000): void {
        if (this.isMonitoring) return;

        this.isMonitoring = true;
        this.monitoringInterval = setInterval(() => this.checkCoherence(), interval);

        this.emit('monitoring:started', {
            timestamp: Date.now(),
            metrics: this.metrics
        });
    }

    public stopMonitoring(): void {
        if (!this.isMonitoring) return;

        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = undefined;
        }

        this.isMonitoring = false;
        this.emit('monitoring:stopped', {
            timestamp: Date.now(),
            metrics: this.metrics
        });
    }

    public isActive(): boolean {
        return this.isMonitoring;
    }

    public getMetrics(): QuantumMetrics {
        return { ...this.metrics };
    }

    public getThresholds(): CoherenceThresholds {
        return { ...this.thresholds };
    }

    public updateMetrics(update: Partial<QuantumMetrics>): void {
        const newMetrics: QuantumMetrics = {
            ...this.metrics,
            ...update,
            timestamp: Date.now()
        };

        this.metrics = newMetrics;
        this.emit('metrics:updated', newMetrics);

        this.checkCoherenceLevel(newMetrics);
    }

    private checkCoherence(): void {
        const currentMetrics = this.getMetrics();
        this.checkCoherenceLevel(currentMetrics);
    }

    private checkCoherenceLevel(metrics: QuantumMetrics): void {
        if (metrics.level <= this.thresholds.critical) {
            const alert: CoherenceAlert = {
                type: 'CRITICAL',
                metrics,
                threshold: this.thresholds.critical,
                timestamp: Date.now()
            };

            this.emit('alert:critical', alert);
            throw new QuantumError(
                'Nivel de coherencia crítico detectado',
                'COHERENCE_CRITICAL',
                {
                    currentLevel: metrics.level,
                    threshold: this.thresholds.critical,
                    metrics
                }
            );
        }

        if (metrics.level <= this.thresholds.warning) {
            const alert: CoherenceAlert = {
                type: 'WARNING',
                metrics,
                threshold: this.thresholds.warning,
                timestamp: Date.now()
            };

            this.emit('alert:warning', alert);
        }
    }
}

export const coherenceMonitor = QuantumCoherenceMonitor.getInstance();