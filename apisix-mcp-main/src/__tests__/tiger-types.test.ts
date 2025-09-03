import { QUANTUM_MAINFRAME } from '@quantum/config/QuantumMainframeConstants';
import { QuantumData, QuantumError } from '../quantum-types';
import { tigerTypesProcessor, TigerTypesOperation } from '../quantum-apisix-tiger-types-ultimate-fixed';

describe('TigerTypesProcessor', () => {
    beforeEach(() => {
        // Restablecer el estado del procesador antes de cada prueba
        tigerTypesProcessor.setConfig({
            coherenceThreshold: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD,
            maxRetries: 3,
            timeout: 5000
        });
    });

    describe('Operaciones de cálculo', () => {
        it('debe realizar una división correctamente', async () => {
            const result = await tigerTypesProcessor.processOperation({
                type: 'CALCULATE',
                args: [10, 2]
            });

            expect(result.value).toBe(5);
            expect(result.state).toBe(QUANTUM_MAINFRAME.STATES.COHERENT);
            expect(result.coherenceLevel).toBe(QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD);
            expect(result.frequency).toBe(QUANTUM_MAINFRAME.FREQUENCY);
            expect(result.signature).toContain('7919');
        });

        it('debe manejar división por cero', async () => {
            await expect(
                tigerTypesProcessor.processOperation({
                    type: 'CALCULATE',
                    args: [10, 0]
                })
            ).rejects.toThrow('División por cero');
        });
    });

    describe('Operaciones de transformación', () => {
        it('debe transformar datos válidos', async () => {
            const testData: QuantumData = { test: 'data' };
            const result = await tigerTypesProcessor.processOperation({
                type: 'TRANSFORM',
                value: testData
            });

            expect(result.value).toEqual(testData);
            expect(result.state).toBe(QUANTUM_MAINFRAME.STATES.COHERENT);
            expect(result.signature).toContain(JSON.stringify(testData));
        });

        it('debe rechazar datos inválidos', async () => {
            // Simular un objeto vacío que será tratado como inválido
            const emptyData: QuantumData = {};
            
            await expect(
                tigerTypesProcessor.processOperation({
                    type: 'TRANSFORM',
                    value: emptyData
                })
            ).rejects.toThrow('Valor inválido');
        });
    });

    describe('Manejo de errores', () => {
        it('debe manejar operaciones no soportadas', async () => {
            // Crear un tipo de operación inválida usando type assertion
            const invalidOperation = {
                type: 'INVALID',
                args: [1, 1]
            } as unknown as TigerTypesOperation;

            await expect(
                tigerTypesProcessor.processOperation(invalidOperation)
            ).rejects.toThrow('Operación no soportada');
        });

        it('debe generar errores cuánticos apropiados', async () => {
            let caughtError: Error | null = null;

            try {
                await tigerTypesProcessor.processOperation({
                    type: 'CALCULATE',
                    args: [1, 0]
                });
                fail('Debería haber lanzado un error');
            } catch (error) {
                caughtError = error instanceof Error ? error : new Error('Error desconocido');
            }

            expect(caughtError).toBeInstanceOf(QuantumError);
            expect(caughtError?.message).toContain('División por cero');
        });
    });

    describe('Configuración', () => {
        it('debe permitir actualizar la configuración', () => {
            const newConfig = {
                maxRetries: 5,
                timeout: 10000
            };

            tigerTypesProcessor.setConfig(newConfig);
            const config = tigerTypesProcessor.getConfig();

            expect(config.maxRetries).toBe(5);
            expect(config.timeout).toBe(10000);
            expect(config.coherenceThreshold).toBe(QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD);
        });

        it('debe mantener valores por defecto al actualizar parcialmente', () => {
            const originalConfig = tigerTypesProcessor.getConfig();
            tigerTypesProcessor.setConfig({ maxRetries: 5 });
            const newConfig = tigerTypesProcessor.getConfig();

            expect(newConfig.maxRetries).toBe(5);
            expect(newConfig.timeout).toBe(originalConfig.timeout);
            expect(newConfig.coherenceThreshold).toBe(originalConfig.coherenceThreshold);
        });
    });

    describe('Generación de firmas', () => {
        it('debe generar firmas únicas para diferentes datos', async () => {
            const result1 = await tigerTypesProcessor.processOperation({
                type: 'TRANSFORM',
                value: { id: 1 }
            });

            const result2 = await tigerTypesProcessor.processOperation({
                type: 'TRANSFORM',
                value: { id: 2 }
            });

            expect(result1.signature).not.toBe(result2.signature);
            expect(result1.signature).toContain('7919');
            expect(result2.signature).toContain('7919');
        });
    });
});