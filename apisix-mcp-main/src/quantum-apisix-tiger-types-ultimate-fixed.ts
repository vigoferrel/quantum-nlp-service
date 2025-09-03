import { QUANTUM_MAINFRAME } from '@quantum/config/QuantumMainframeConstants';
import { QuantumData, QuantumError, QuantumUtils } from './quantum-types';

export type TigerTypesOperation = 
    | { type: 'CALCULATE'; args: [number, number] }
    | { type: 'TRANSFORM'; value: QuantumData };

interface TigerTypesResult<T> {
    value: T;
    state: typeof QUANTUM_MAINFRAME.STATES[keyof typeof QUANTUM_MAINFRAME.STATES];
    coherenceLevel: number;
    frequency: number;
    processingTime: number;
    signature: string;
    timestamp: number;
}

interface TigerTypesConfig {
    coherenceThreshold: number;
    maxRetries: number;
    timeout: number;
}

/**
 * Implementación mejorada de Tiger Types
 */
export class TigerTypesProcessor {
    private static instance: TigerTypesProcessor;
    private coherenceLevel: number;
    private config: TigerTypesConfig;

    private constructor() {
        this.coherenceLevel = QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD;
        this.config = {
            coherenceThreshold: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD,
            maxRetries: 3,
            timeout: 5000
        };
    }

    public static getInstance(): TigerTypesProcessor {
        if (!TigerTypesProcessor.instance) {
            TigerTypesProcessor.instance = new TigerTypesProcessor();
        }
        return TigerTypesProcessor.instance;
    }

    /**
     * Procesa una operación Tiger Types
     */
    public async processOperation(operation: TigerTypesOperation): Promise<TigerTypesResult<QuantumData>> {
        if (!QuantumUtils.validateCoherence(this.coherenceLevel)) {
            throw QuantumUtils.createError(
                'COHERENCE_LOSS',
                'Nivel de coherencia insuficiente'
            );
        }

        try {
            const result = await this.executeOperation(operation);
            return this.createTigerResult(result);
        } catch (error) {
            throw this.handleError(error);
        }
    }

    private async executeOperation(operation: TigerTypesOperation): Promise<QuantumData> {
        switch (operation.type) {
            case 'CALCULATE': {
                const result = this.executeCalculation(...operation.args);
                return result;
            }
            case 'TRANSFORM':
                return this.executeTransformation(operation.value);
            default:
                throw QuantumUtils.createError(
                    'OPERATION_FAILED',
                    'Operación no soportada'
                );
        }
    }

    private executeCalculation(a: number, b: number): number {
        if (b === 0) {
            throw QuantumUtils.createError(
                'VALIDATION_ERROR',
                'División por cero'
            );
        }
        return a / b;
    }

    private executeTransformation(value: QuantumData): QuantumData {
        if (value === null || value === undefined) {
            throw QuantumUtils.createError(
                'VALIDATION_ERROR',
                'Valor inválido para transformación'
            );
        }
        return value;
    }

    private createTigerResult(value: QuantumData): TigerTypesResult<QuantumData> {
        return {
            value,
            state: QUANTUM_MAINFRAME.STATES.COHERENT,
            coherenceLevel: this.coherenceLevel,
            frequency: QUANTUM_MAINFRAME.FREQUENCY,
            processingTime: QUANTUM_MAINFRAME.CONFIG.PROCESSING_TIME_PICOSECONDS,
            signature: this.generateSignature(value),
            timestamp: Date.now()
        };
    }

    private generateSignature(value: QuantumData): string {
        return `${QUANTUM_MAINFRAME.FREQUENCY}-${this.coherenceLevel}-${JSON.stringify(value)}`;
    }

    private handleError(error: unknown): QuantumError {
        if (error instanceof QuantumError) {
            return error;
        }
        return QuantumUtils.createError(
            'SYSTEM_ERROR',
            error instanceof Error ? error.message : String(error)
        );
    }

    public getConfig(): TigerTypesConfig {
        return { ...this.config };
    }

    public setConfig(config: Partial<TigerTypesConfig>): void {
        this.config = {
            ...this.config,
            ...config
        };
    }
}

// Exportar una instancia singleton
export const tigerTypesProcessor = TigerTypesProcessor.getInstance();