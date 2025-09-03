import { QUANTUM_MAINFRAME } from '@quantum/config/QuantumMainframeConstants';
import { QuantumError } from '../quantum-types';
import { coherenceMonitor, CoherenceAlert } from '../monitoring/QuantumCoherenceMonitor';

describe('QuantumCoherenceMonitor', () => {
    const mockTimestamp = 1689555555555;

    beforeEach(() => {
        // Detener el monitoreo y restablecer el estado
        coherenceMonitor.stopMonitoring();
        jest.useFakeTimers();
        jest.setSystemTime(mockTimestamp);
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    describe('Inicialización', () => {
        it('debe iniciar con valores por defecto correctos', () => {
            const metrics = coherenceMonitor.getMetrics();
            const thresholds = coherenceMonitor.getThresholds();

            expect(metrics.level).toBe(QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD);
            expect(metrics.frequency).toBe(QUANTUM_MAINFRAME.FREQUENCY);
            expect(metrics.state).toBe(QUANTUM_MAINFRAME.STATES.COHERENT);
            expect(typeof metrics.timestamp).toBe('number');
            expect(metrics.timestamp).toBeGreaterThan(0);

            expect(thresholds.warning).toBe(QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.95);
            expect(thresholds.critical).toBe(QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.90);
        });
    });

    describe('Control de monitoreo', () => {
        it('debe iniciar y detener el monitoreo correctamente', () => {
            expect(coherenceMonitor.isActive()).toBe(false);

            coherenceMonitor.startMonitoring();
            expect(coherenceMonitor.isActive()).toBe(true);

            coherenceMonitor.stopMonitoring();
            expect(coherenceMonitor.isActive()).toBe(false);
        });

        it('debe ejecutar verificaciones periódicas', () => {
            // Accedemos al método privado de manera segura para testing
            const checkSpy = jest.spyOn(coherenceMonitor as unknown as { checkCoherence: () => void }, 'checkCoherence');
            coherenceMonitor.startMonitoring(1000);

            jest.advanceTimersByTime(3500);
            expect(checkSpy).toHaveBeenCalledTimes(3);

            coherenceMonitor.stopMonitoring();
            jest.advanceTimersByTime(1000);
            expect(checkSpy).toHaveBeenCalledTimes(3);

            checkSpy.mockRestore();
        });
    });

    describe('Manejo de métricas', () => {
        it('debe actualizar métricas correctamente', () => {
            const newLevel = QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.98;
            coherenceMonitor.updateMetrics({ level: newLevel });

            const metrics = coherenceMonitor.getMetrics();
            expect(metrics.level).toBe(newLevel);
            expect(metrics.timestamp).toBe(mockTimestamp);
        });

        it('debe mantener valores no actualizados', () => {
            const originalMetrics = coherenceMonitor.getMetrics();
            coherenceMonitor.updateMetrics({ level: 0.98 });

            const newMetrics = coherenceMonitor.getMetrics();
            expect(newMetrics.frequency).toBe(originalMetrics.frequency);
            expect(newMetrics.state).toBe(originalMetrics.state);
        });
    });

    describe('Sistema de alertas', () => {
        it('debe emitir alerta de advertencia', (done) => {
            const warningLevel = QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.94;

            coherenceMonitor.once('alert:warning', (alert: CoherenceAlert) => {
                expect(alert.type).toBe('WARNING');
                expect(alert.metrics.level).toBe(warningLevel);
                expect(alert.metrics.timestamp).toBe(mockTimestamp);
                expect(alert.threshold).toBe(coherenceMonitor.getThresholds().warning);
                done();
            });

            coherenceMonitor.updateMetrics({ level: warningLevel });
        });

        it('debe lanzar error en nivel crítico', () => {
            const criticalLevel = QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.89;

            expect(() => {
                coherenceMonitor.updateMetrics({ level: criticalLevel });
            }).toThrow(QuantumError);
        });

        it('debe emitir alerta crítica antes de lanzar error', (done) => {
            const criticalLevel = QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.89;

            coherenceMonitor.once('alert:critical', (alert: CoherenceAlert) => {
                expect(alert.type).toBe('CRITICAL');
                expect(alert.metrics.level).toBe(criticalLevel);
                expect(alert.threshold).toBe(coherenceMonitor.getThresholds().critical);
                done();
            });

            try {
                coherenceMonitor.updateMetrics({ level: criticalLevel });
            } catch (error: unknown) {
                expect(error).toBeInstanceOf(QuantumError);
            }
        });
    });

    describe('Eventos del sistema', () => {
        it('debe emitir eventos de inicio/fin de monitoreo', (done) => {
            let eventsReceived = 0;

            coherenceMonitor.once('monitoring:started', (data) => {
                expect(data.timestamp).toBe(mockTimestamp);
                expect(data.metrics).toEqual(coherenceMonitor.getMetrics());
                eventsReceived++;
            });

            coherenceMonitor.once('monitoring:stopped', (data) => {
                expect(data.timestamp).toBe(mockTimestamp);
                expect(data.metrics).toEqual(coherenceMonitor.getMetrics());
                eventsReceived++;
                expect(eventsReceived).toBe(2);
                done();
            });

            coherenceMonitor.startMonitoring();
            coherenceMonitor.stopMonitoring();
        });

        it('debe emitir eventos de actualización de métricas', (done) => {
            const newLevel = 0.98;

            coherenceMonitor.once('metrics:updated', (metrics) => {
                expect(metrics.level).toBe(newLevel);
                expect(metrics.timestamp).toBe(mockTimestamp);
                done();
            });

            coherenceMonitor.updateMetrics({ level: newLevel });
        });
    });
});