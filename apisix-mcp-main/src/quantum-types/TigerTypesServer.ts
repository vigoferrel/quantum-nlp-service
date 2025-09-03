import { QUANTUM_MAINFRAME } from '@quantum/config/QuantumMainframeConstants';
import { QuantumEither } from './QuantumEither';
import { QuantumTry } from './QuantumTry';
import {
    QuantumData,
    QuantumOperation,
    QuantumResult,
    CallToolResult,
    QuantumError,
    QuantumUtils
} from './QuantumTypes';

/**
 * Servidor Tiger Types para operaciones cuánticas seguras
 */
export class TigerTypesServer {
    private static instance: TigerTypesServer;
    private coherenceLevel: number;

    private constructor() {
        this.coherenceLevel = QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD;
    }

    public static getInstance(): TigerTypesServer {
        if (!TigerTypesServer.instance) {
            TigerTypesServer.instance = new TigerTypesServer();
        }
        return TigerTypesServer.instance;
    }

    /**
     * Ejecuta una operación usando Either
     */
    public executeWithEither(value: QuantumData): QuantumEither<string, QuantumResult<QuantumData>> {
        try {
            if (QuantumUtils.validateCoherence(this.coherenceLevel)) {
                return QuantumEither.Right(QuantumUtils.createResult(value));
            }
            return QuantumEither.Left('Coherencia insuficiente');
        } catch (error) {
            return QuantumEither.Left(error instanceof Error ? error.message : String(error));
        }
    }

    /**
     * Ejecuta una operación usando Try
     */
    public executeWithTry(operation: QuantumOperation): QuantumTry<QuantumError, QuantumResult<QuantumData>> {
        return QuantumTry.From(() => {
            if (!QuantumUtils.validateCoherence(this.coherenceLevel)) {
                throw QuantumUtils.createError(
                    'COHERENCE_LOSS',
                    'Nivel de coherencia insuficiente'
                );
            }

            switch (operation.name) {
                case 'CALCULATE': {
                    const [a, b] = operation.args as number[];
                    if (typeof a !== 'number' || typeof b !== 'number') {
                        throw QuantumUtils.createError(
                            'VALIDATION_ERROR',
                            'Argumentos inválidos para cálculo'
                        );
                    }
                    return QuantumUtils.createResult(a / b);
                }
                case 'TRANSFORM': {
                    const [value] = operation.args;
                    return QuantumUtils.createResult(value);
                }
                default:
                    throw QuantumUtils.createError(
                        'OPERATION_FAILED',
                        'Operación no soportada'
                    );
            }
        });
    }

    /**
     * Ejecuta una operación cuántica
     */
    public async executeQuantumOperation(operation: QuantumOperation): Promise<CallToolResult> {
        try {
            const tryResult = this.executeWithTry(operation);
            
            if (tryResult.isFailure()) {
                throw tryResult.getErrorOrNull() || new Error('Error desconocido');
            }

            const result = tryResult.getOrNull();
            if (!result) {
                throw QuantumUtils.createError(
                    'OPERATION_FAILED',
                    'Resultado nulo'
                );
            }

            return {
                success: true,
                data: result
            };
        } catch (error) {
            if (error instanceof QuantumError) {
                throw error;
            }
            throw QuantumUtils.createError(
                'SYSTEM_ERROR',
                error instanceof Error ? error.message : String(error)
            );
        }
    }

    /**
     * Obtiene el nivel de coherencia actual
     */
    public getCoherenceLevel(): number {
        return this.coherenceLevel;
    }

    /**
     * Actualiza el nivel de coherencia
     */
    public setCoherenceLevel(level: number): void {
        this.coherenceLevel = level;
    }
}

// Exportar una instancia singleton
export const tigerTypesServer = TigerTypesServer.getInstance();