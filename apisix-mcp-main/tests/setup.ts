/**
 * QUANTUM TESTS SETUP - VIGOLEONROCKS
 * Configuración inicial para tests cuánticos
 */

// Mock de console.error para tests silenciosos
const originalConsoleError = console.error;
console.error = (...args: any[]) => {
  // Solo mostrar errores que no sean de logging cuántico
  if (!args[0]?.toString().includes('🌌') && !args[0]?.toString().includes('⚡')) {
    originalConsoleError(...args);
  }
};

// Variables de entorno para testing
process.env.NODE_ENV = 'test';
process.env.QUANTUM_FREQUENCY = '888';
process.env.VIGOLEONROCKS_MODE = 'testing';

// Mock de fetch para tests
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    status: 200,
    json: () => Promise.resolve({ success: true, timestamp: Date.now() }),
  })
) as jest.Mock;

// Setup global para frecuencia cuántica
(global as any).QUANTUM_BASE_FREQUENCY = 888;

// Cleanup después de cada test
afterEach(() => {
  jest.clearAllMocks();
});

console.log('🌌 Quantum Test Environment Initialized - VIGOLEONROCKS 888Hz');