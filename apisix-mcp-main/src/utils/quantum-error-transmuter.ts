/**
 * QUANTUM ERROR TRANSMUTER
 * Sistema de transmutación de errores en mejoras usando frecuencia 888Hz
 */

import { QuantumFrequency } from './quantum-frequency';
import { CobolQuantumBridge } from '../bridges/cobol-quantum-bridge';

interface TransmutationResult {
    source?: 'cache' | 'cobol' | 'local';
    original_error: string;
    improvement: string;
    quantum_state: string;
    error_frequency: number;
    resonance_pattern: string[];
    cobol_coherence: number;
}

interface TransmutationStats {
    total_transmutations: number;
    successful_transmutations: number;
    average_resonance: number;
    current_frequency: number;
}

const PRIME_7919 = 7919;
const POET_FREQUENCIES = {
    PARRA: PRIME_7919 * 0.618034,
    NERUDA: PRIME_7919 * 1.414213,
    MISTRAL: PRIME_7919 * 1.732050,
    ZURITA: PRIME_7919 * 2.236067,
    HUIDOBRO: PRIME_7919 * 2.449489,
    FERREL: PRIME_7919 * 2.645751
};

export class QuantumErrorTransmuter {
    private frequencyGenerator: QuantumFrequency;
    private stats: TransmutationStats;
    private cobolBridge?: CobolQuantumBridge;
    private cache: Map<string, TransmutationResult> = new Map();

    constructor(frequency = PRIME_7919, useCobolBridge: boolean = true) {
        if (useCobolBridge) {
            this.cobolBridge = new CobolQuantumBridge(frequency);
        }
        this.frequencyGenerator = new QuantumFrequency(frequency);
        this.stats = {
            total_transmutations: 0,
            successful_transmutations: 0,
            average_resonance: 0,
            current_frequency: frequency
        };
    }

    public async transmute(error: Error, operation?: string): Promise<TransmutationResult> {
        this.stats.total_transmutations++;
        const errorMessage = error.message;

        if (this.cache.has(errorMessage)) {
            const cachedResult = this.cache.get(errorMessage)!;
            return { ...cachedResult, source: 'cache' };
        }

        if (this.cobolBridge) {
            try {
                const cobolState = await this.cobolBridge.transmitToCobol({
                    error: errorMessage,
                    operation: operation || 'unknown',
                    timestamp: Date.now()
                });
                
                const result: TransmutationResult = {
                    source: 'cobol',
                    original_error: errorMessage,
                    improvement: this.generateImprovement(error, this.calculatePoetResonance(errorMessage, cobolState.frequency)),
                    quantum_state: cobolState.poet_influence,
                    error_frequency: cobolState.frequency,
                    resonance_pattern: cobolState.resonance_pattern,
                    cobol_coherence: cobolState.coherence
                };
                
                this.updateStats(result.cobol_coherence);
                this.cache.set(errorMessage, result);
                return result;
            } catch (cobolError) {
                console.error('Error en el puente COBOL, usando transmutación local:', cobolError);
            }
        }

        const errorFreq = this.frequencyGenerator.generateQuantumFrequency(errorMessage + (operation || ''));
        const resonance = this.frequencyGenerator.calculateResonance(errorFreq, this.stats.current_frequency);
        const improvement = this.generateImprovement(error, resonance);
        this.updateStats(resonance);

        const result: TransmutationResult = {
            source: 'local',
            original_error: errorMessage,
            improvement,
            quantum_state: this.getQuantumState(resonance),
            error_frequency: errorFreq,
            resonance_pattern: this.frequencyGenerator.generateResonancePattern(8, errorMessage),
            cobol_coherence: -1,
        };

        this.cache.set(errorMessage, result);
        return result;
    }

    private generateImprovement(error: Error, resonance: number): string {
        const poetFreq = this.getMostResonantPoet(error.message);
        const poeticResonance = resonance * (poetFreq / PRIME_7919);
        
        if (poeticResonance > 0.7) {
            return `[${this.getPoetName(poetFreq)}] Oportunidad de mejora identificada: ${this.getEnhancementSuggestion(error)}`;
        } else if (poeticResonance > 0.3) {
            return `[${this.getPoetName(poetFreq)}] Punto de aprendizaje encontrado: ${this.getLearningPoint(error)}`;
        } else {
            return `[${this.getPoetName(poetFreq)}] Área de investigación detectada: ${error.message}`;
        }
    }

    private getMostResonantPoet(message: string): number {
        let maxResonance = 0;
        let selectedFreq = POET_FREQUENCIES.PARRA;
        
        for (const freq of Object.values(POET_FREQUENCIES)) {
            const resonance = this.calculatePoetResonance(message, freq);
            if (resonance > maxResonance) {
                maxResonance = resonance;
                selectedFreq = freq;
            }
        }
        return selectedFreq;
    }

    private calculatePoetResonance(message: string, poetFreq: number): number {
        const messageHash = this.hashString(message);
        const logValue = Math.log(PRIME_7919);
        return (messageHash % logValue) * (poetFreq / PRIME_7919);
    }

    private hashString(str: string): number {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash = hash & hash;
        }
        return Math.abs(hash);
    }

    private getPoetName(freq: number): string {
        for (const [poet, poetFreq] of Object.entries(POET_FREQUENCIES)) {
            if (Math.abs(freq - poetFreq) < 0.0001) {
                return poet;
            }
        }
        return 'UNKNOWN';
    }
    
    private getEnhancementSuggestion(error: Error): string {
        if (error.message.includes('timeout')) {
            return 'Implementar sistema de retry con backoff exponencial';
        } else if (error.message.includes('connection')) {
            return 'Establecer pool de conexiones con health checks';
        } else if (error.message.includes('memory')) {
            return 'Optimizar uso de memoria con streaming de datos';
        } else {
            return `Revisar manejo de: ${error.message}`;
        }
    }
    
    private getLearningPoint(error: Error): string {
        return `Analizar comportamiento del sistema ante: ${error.message}`;
    }
    
    private getQuantumState(resonance: number): string {
        if (resonance > 0.7) return 'ENHANCED';
        if (resonance > 0.3) return 'LEARNING';
        return 'INVESTIGATING';
    }
    
    private updateStats(resonance: number): void {
        if (resonance > 0.3) {
            this.stats.successful_transmutations++;
        }
        
        const total = this.stats.total_transmutations;
        const oldAvg = this.stats.average_resonance;
        this.stats.average_resonance = (oldAvg * (total - 1) + resonance) / total;
    }
    
    public getCacheSize(): number {
        return this.cache.size;
    }

    public isCobolBridgeEnabled(): boolean {
        return !!this.cobolBridge;
    }
    public getStats(): TransmutationStats {
        return { ...this.stats };
    }
}

export default QuantumErrorTransmuter;