/**
 * JEST CONFIGURATION - QUANTUM TESTING VIGOLEONROCKS
 * Configuración simplificada para testing del sistema cuántico
 */

const config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  
  // Configuración de archivos
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: [
    '**/__tests__/**/*.ts',
    '**/?(*.)+(spec|test).ts'
  ],
  
  // Configuración de transformación
  transform: {
    '^.+\\.ts$': 'ts-jest'
  },
  
  // Configuración de cobertura
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts'
  ],
  
  // Configuración de cobertura detallada
  coverageDirectory: 'coverage',
  coverageReporters: [
    'text',
    'lcov',
    'html'
  ],
  
  // Configuración de paths
  moduleNameMapper: {
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@tools/(.*)$': '<rootDir>/src/tools/$1',
    // Mapear importaciones .js a .ts para Jest
    '^(.+)\\.js$': '$1'
  },
  
  // Configuración de timeout
  testTimeout: 10000,
  
  // Configuración de verbose
  verbose: true,
  
  // Display name cuántico
  displayName: {
    name: 'QUANTUM-TESTS-888Hz',
    color: 'magenta'
  },
  
  // Configuración específica para ts-jest
  globals: {
    'ts-jest': {
      useESM: false,
      tsconfig: {
        module: 'commonjs'
      }
    }
  }
};

module.exports = config;