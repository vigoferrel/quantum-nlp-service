import { QUANTUM_MAINFRAME } from '@quantum/config/QuantumMainframeConstants';

/**
 * Tipos base para el sistema cuántico
 */

// Tipos de datos cuánticos
export type QuantumData = number | string | boolean | Record<string, unknown>;

// Resultado cuántico base
export interface QuantumResult<T> {
    value: T;
    state: typeof QUANTUM_MAINFRAME.STATES[keyof typeof QUANTUM_MAINFRAME.STATES];
    coherenceLevel: number;
    frequency: number;
    processingTime: number;
}

// Configuración de operaciones
export interface QuantumOperationConfig {
    coherenceThreshold?: number;
    maxRetries?: number;
    timeout?: number;
}

// Operación cuántica
export interface QuantumOperation {
    name: string;
    args: QuantumData[];
    config?: QuantumOperationConfig;
}

// Resultado de herramienta
export interface CallToolResult {
    success: boolean;
    data: QuantumResult<QuantumData>;
    error?: Error;
}

// Error cuántico personalizado
export class QuantumError extends Error {
    constructor(
        message: string,
        public readonly code: string,
        public readonly details?: Record<string, unknown>,
        public readonly quantum?: {
            state: string;
            coherenceLevel: number;
        }
    ) {
        super(message);
        this.name = 'QuantumError';
    }
}

// Constantes de error
export const QUANTUM_ERROR_CODES = {
    COHERENCE_LOSS: 'COHERENCE_LOSS',
    FREQUENCY_MISMATCH: 'FREQUENCY_MISMATCH',
    OPERATION_FAILED: 'OPERATION_FAILED',
    VALIDATION_ERROR: 'VALIDATION_ERROR',
    SYSTEM_ERROR: 'SYSTEM_ERROR'
} as const;

// Funciones auxiliares
export const QuantumUtils = {
    createResult<T>(
        value: T,
        state = QUANTUM_MAINFRAME.STATES.COHERENT,
        coherenceLevel = QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD
    ): QuantumResult<T> {
        return {
            value,
            state,
            coherenceLevel,
            frequency: QUANTUM_MAINFRAME.FREQUENCY,
            processingTime: QUANTUM_MAINFRAME.CONFIG.PROCESSING_TIME_PICOSECONDS
        };
    },

    createError(
        code: keyof typeof QUANTUM_ERROR_CODES,
        message: string,
        details?: Record<string, unknown>
    ): QuantumError {
        return new QuantumError(
            message,
            QUANTUM_ERROR_CODES[code],
            details,
            {
                state: QUANTUM_MAINFRAME.STATES.COHERENT,
                coherenceLevel: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD
            }
        );
    },

    validateCoherence(level: number): boolean {
        return level >= QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD;
    },

    validateFrequency(frequency: number): boolean {
        return frequency === QUANTUM_MAINFRAME.FREQUENCY;
    }
};