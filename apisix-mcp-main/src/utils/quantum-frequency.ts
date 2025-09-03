/**
 * QUANTUM FREQUENCY GENERATOR
 * Sistema de generación de frecuencias cuánticas determinísticas
 * Frecuencia Base: 888Hz - VIGOLEONROCKS
 */

interface QuantumStats {
    base_frequency: number;
    golden_ratio: number;
    phi_sequence_length: number;
    current_resonance: number;
}

type ResonanceType = 'HIGH_RESONANCE' | 'MEDIUM_RESONANCE' | 'LOW_RESONANCE';

export class QuantumFrequency {
    private readonly BASE_FREQUENCY = 888;
    private readonly GOLDEN_RATIO = 1.618033988749;
    private readonly PHI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987];
    
    constructor(private frequency = 888) {}
    
    public generateQuantumFrequency(seed: string): number {
        const baseHash = this.hashString(seed);
        const frequency = (baseHash % 1000) + this.frequency;
        const phi = this.PHI_SEQUENCE[baseHash % this.PHI_SEQUENCE.length];
        return (frequency * this.GOLDEN_RATIO * phi) % 1;
    }
    
    public generateResonancePattern(length: number, seed: string): ResonanceType[] {
        const pattern: ResonanceType[] = [];
        
        for (let i = 0; i < length; i++) {
            const freq = this.generateQuantumFrequency(seed + i.toString());
            const resonance = this.calculateResonance(freq, this.frequency);
            pattern.push(this.getResonanceType(resonance));
        }
        
        return pattern;
    }
    
    public calculateResonance(freq1: number, freq2: number): number {
        const ratio = Math.min(freq1, freq2) / Math.max(freq1, freq2);
        return (ratio * this.GOLDEN_RATIO) % 1;
    }
    
    public synchronizeWith(targetFreq: number): number {
        const resonance = this.calculateResonance(targetFreq, this.frequency);
        return (targetFreq * resonance * this.GOLDEN_RATIO) % this.frequency;
    }

    public generateHarmonics(count: number): number[] {
        const harmonics: number[] = [];
        for (let i = 1; i <= count; i++) {
            const harmonic = this.frequency * (this.PHI_SEQUENCE[i % this.PHI_SEQUENCE.length] / this.GOLDEN_RATIO);
            harmonics.push(harmonic);
        }
        return harmonics;
    }
    
    private hashString(str: string): number {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash);
    }
    
    private getResonanceType(resonance: number): ResonanceType {
        if (resonance > 0.7) return 'HIGH_RESONANCE';
        if (resonance > 0.3) return 'MEDIUM_RESONANCE';
        return 'LOW_RESONANCE';
    }
    
    public getStats(): QuantumStats {
        return {
            base_frequency: this.frequency,
            golden_ratio: this.GOLDEN_RATIO,
            phi_sequence_length: this.PHI_SEQUENCE.length,
            current_resonance: this.calculateResonance(this.frequency, this.BASE_FREQUENCY)
        };
    }
}

export default QuantumFrequency;