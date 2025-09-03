// Re-exportar todo desde los módulos
export * from './QuantumTypes';
export * from './QuantumEither';
export * from './QuantumTry';
export * from './TigerTypesServer';

// Exportar la instancia singleton del servidor
export { tigerTypesServer } from './TigerTypesServer';