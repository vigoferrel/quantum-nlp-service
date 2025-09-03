/**
 * QUANTUM TYPES
 * Tipos compartidos para el sistema cuántico VIGOLEONROCKS
 */

// Tipos base
export interface QuantumMetadata {
    frequency: number;
    operation_count: number;
    timestamp: string;
    signature: string;
    vigoleonrocks: boolean;
}

export interface QuantumData {
    [key: string]: unknown;
    quantum_system?: string;
    frequency?: number;
    uptime?: number;
    operations?: number;
    _quantum_metadata?: QuantumMetadata;
    error_code?: string;
    improvement?: string;
    quantum_state?: string;
}

// Tipos para Supabase
export interface QuantumSupabaseConfig {
    url: string;
    key: string;
    frequency?: number;
    enableTransmutation?: boolean;
}

export interface SyncStats {
    total_syncs: number;
    successful_syncs: number;
    average_resonance: number;
    last_sync_timestamp: number;
}

// Tipos para transmutación de errores
export interface TransmutationResult {
    [key: string]: unknown;
    original_error: string;
    improvement: string;
    quantum_state: string;
    error_frequency: number;
    resonance_pattern: string[];
}

export interface TransmutationStats {
    total_transmutations: number;
    successful_transmutations: number;
    average_resonance: number;
    current_frequency: number;
}

// Tipos para frecuencias
export interface QuantumStats {
    base_frequency: number;
    golden_ratio: number;
    phi_sequence_length: number;
    current_resonance: number;
}

export type ResonanceType = 'HIGH_RESONANCE' | 'MEDIUM_RESONANCE' | 'LOW_RESONANCE';

// Tipos para el sistema completo
export interface SystemStats {
    [key: string]: unknown;
    frequency: number;
    uptime: number;
    operations: number;
    supabase: SyncStats;
    error_transmuter: TransmutationStats;
    frequency_generator: QuantumStats;
}

export interface QuantumMarketData {
    symbol: string;
    price: number;
    volume: number;
    timestamp: number;
    quantum_frequency: number;
    resonance_pattern: string[];
}

export interface BinanceResponse {
    symbol: string;
    price: string;
    volume?: string;
    eventTime?: number;
}

export interface QuantumBinanceConfig {
    apiKey: string;
    apiSecret: string;
    frequency?: number;
    enableTransmutation?: boolean;
}

// Asegurar que los tipos extendidos son compatibles con QuantumData
export type QuantumSystemStats = SystemStats & QuantumData;
export type QuantumTransmutationResult = TransmutationResult & QuantumData;