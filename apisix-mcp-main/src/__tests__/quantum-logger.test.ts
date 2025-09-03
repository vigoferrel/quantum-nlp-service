import { quantumLogger } from '../logging/QuantumLogger';
import { QUANTUM_LOGGING_CONFIG } from '../config/QuantumLoggingConfig';
import { QuantumLogEntry } from '../logging/QuantumLogger';

interface QuantumLoggerPrivate {
    flush: () => Promise<void>;
    persistLogs: (entries: QuantumLogEntry[]) => Promise<void>;
}

describe('QuantumLogger', () => {
    const mockTimestamp = 1689555555555;
    const mockMetrics = {
        level: 0.98,
        frequency: 1000,
        state: 'COHERENT',
        timestamp: mockTimestamp
    };

    beforeEach(() => {
        jest.useFakeTimers();
        jest.setSystemTime(mockTimestamp);
    });

    afterEach(async () => {
        await quantumLogger.destroy();
        jest.useRealTimers();
    });

    describe('Operaciones básicas de logging', () => {
        it('debe registrar mensajes con diferentes niveles', () => {
            const logSpy = jest.spyOn(quantumLogger, 'log');

            quantumLogger.debug('Mensaje debug');
            quantumLogger.info('Mensaje info');
            quantumLogger.warn('Mensaje warning');
            quantumLogger.error('Mensaje error');
            quantumLogger.quantum('Mensaje quantum', mockMetrics);

            expect(logSpy).toHaveBeenCalledTimes(5);
            expect(logSpy).toHaveBeenCalledWith('DEBUG', 'Mensaje debug', undefined, undefined, undefined);
            expect(logSpy).toHaveBeenCalledWith('INFO', 'Mensaje info', undefined, undefined, undefined);
            expect(logSpy).toHaveBeenCalledWith('WARN', 'Mensaje warning', undefined, undefined, undefined);
            expect(logSpy).toHaveBeenCalledWith('ERROR', 'Mensaje error', undefined, undefined, undefined);
            expect(logSpy).toHaveBeenCalledWith('QUANTUM', 'Mensaje quantum', mockMetrics, undefined, undefined);

            logSpy.mockRestore();
        });

        it('debe incluir contexto y origen en los logs', () => {
            const context = { operation: 'test' };
            const source = 'test-module';
            const logSpy = jest.spyOn(quantumLogger, 'log');

            quantumLogger.info('Mensaje con contexto', context, source);

            expect(logSpy).toHaveBeenCalledWith('INFO', 'Mensaje con contexto', undefined, context, source);
            logSpy.mockRestore();
        });
    });

    describe('Buffer y Flush', () => {
        it('debe hacer flush automático cuando el buffer está lleno', () => {
            const flushSpy = jest.spyOn(quantumLogger as unknown as QuantumLoggerPrivate, 'flush');
            const bufferSize = QUANTUM_LOGGING_CONFIG.BUFFER.SIZE;

            // Llenar el buffer
            for (let i = 0; i < bufferSize + 1; i++) {
                quantumLogger.info(`Mensaje ${i}`);
            }

            expect(flushSpy).toHaveBeenCalled();
            flushSpy.mockRestore();
        });

        it('debe hacer flush periódico basado en el intervalo', () => {
            const flushSpy = jest.spyOn(quantumLogger as unknown as QuantumLoggerPrivate, 'flush');
            const flushInterval = QUANTUM_LOGGING_CONFIG.BUFFER.FLUSH_INTERVAL;

            quantumLogger.info('Mensaje de prueba');
            jest.advanceTimersByTime(flushInterval + 100);

            expect(flushSpy).toHaveBeenCalled();
            flushSpy.mockRestore();
        });
    });

    describe('Eventos', () => {
        it('debe emitir eventos de log', (done) => {
            const testMessage = 'Mensaje de prueba';

            quantumLogger.once('log', (entry) => {
                expect(entry.level).toBe('INFO');
                expect(entry.message).toBe(testMessage);
                expect(entry.timestamp).toBe(mockTimestamp);
                done();
            });

            quantumLogger.info(testMessage);
        });

        it('debe emitir eventos de flush', (done) => {
            const testMessage = 'Mensaje para flush';

            quantumLogger.once('flush', (entries) => {
                expect(entries).toHaveLength(1);
                expect(entries[0].message).toBe(testMessage);
                done();
            });

            quantumLogger.info(testMessage);
            jest.advanceTimersByTime(QUANTUM_LOGGING_CONFIG.BUFFER.FLUSH_INTERVAL);
        });

        it('debe emitir alertas de coherencia baja', (done) => {
            const lowCoherenceMetrics = {
                ...mockMetrics,
                level: QUANTUM_LOGGING_CONFIG.COHERENCE.MIN_LEVEL - 0.1
            };

            quantumLogger.once('coherence:low', (alert) => {
                expect(alert.level).toBe(lowCoherenceMetrics.level);
                expect(alert.threshold).toBe(QUANTUM_LOGGING_CONFIG.COHERENCE.MIN_LEVEL);
                expect(alert.timestamp).toBe(mockTimestamp);
                done();
            });

            quantumLogger.quantum('Coherencia baja detectada', lowCoherenceMetrics);
        });
    });

    describe('Manejo de errores', () => {
        it('debe incluir detalles del error en el contexto', () => {
            const testError = new Error('Error de prueba');
            const logSpy = jest.spyOn(quantumLogger, 'log');

            quantumLogger.error('Error en operación', testError);

            expect(logSpy).toHaveBeenCalledWith(
                'ERROR',
                'Error en operación',
                undefined,
                expect.objectContaining({
                    error: {
                        name: testError.name,
                        message: testError.message,
                        stack: testError.stack
                    }
                }),
                undefined
            );

            logSpy.mockRestore();
        });

        it('debe reintentar el flush en caso de error', async () => {
            const mockError = new Error('Error de persistencia');
            const persistSpy = jest.spyOn(quantumLogger as unknown as QuantumLoggerPrivate, 'persistLogs')
                .mockRejectedValueOnce(mockError)
                .mockResolvedValueOnce(undefined);

            quantumLogger.info('Mensaje para retry');
            await jest.advanceTimersByTimeAsync(QUANTUM_LOGGING_CONFIG.BUFFER.FLUSH_INTERVAL);

            expect(persistSpy).toHaveBeenCalledTimes(1);
            await jest.advanceTimersByTimeAsync(QUANTUM_LOGGING_CONFIG.BUFFER.FLUSH_INTERVAL);
            expect(persistSpy).toHaveBeenCalledTimes(2);

            persistSpy.mockRestore();
        });
    });
});