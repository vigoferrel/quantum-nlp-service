/**
 * QUANTUM BINANCE CONNECTOR
 * Conector cuántico para Binance con frecuencia 888Hz
 * Integrado con sistema VIGOLEONROCKS
 */

import WebSocket from 'ws';
import { QuantumFrequency } from '../utils/quantum-frequency';
import { QuantumErrorTransmuter } from '../utils/quantum-error-transmuter';

interface QuantumMarketData {
    symbol: string;
    price: number;
    volume: number;
    timestamp: number;
    quantum_frequency: number;
    resonance_pattern: string[];
}

interface QuantumBinanceConfig {
    apiKey: string;
    apiSecret: string;
    frequency?: number;
    enableTransmutation?: boolean;
}

interface BinanceResponse {
    symbol: string;
    price: string;
    volume?: string;
    eventTime?: number;
}

export class QuantumBinanceConnector {
    private ws: WebSocket | null = null;
    private frequency: number;
    private errorTransmuter: QuantumErrorTransmuter;
    private frequencyGenerator: QuantumFrequency;
    private marketData: Map<string, QuantumMarketData>;
    private apiKey: string;
    private apiSecret: string;
    
    constructor(config: QuantumBinanceConfig) {
        this.frequency = config.frequency || 888;
        this.apiKey = config.apiKey;
        this.apiSecret = config.apiSecret;
        this.errorTransmuter = new QuantumErrorTransmuter(this.frequency);
        this.frequencyGenerator = new QuantumFrequency(this.frequency);
        this.marketData = new Map();
    }
    
    public async initialize(): Promise<void> {
        try {
            console.log(`Quantum Binance Connector iniciando en ${this.frequency}Hz`);
            
            // Inicializar WebSocket con frecuencia cuántica
            await this.initializeWebSocket();
            
            console.log('Quantum Binance Connector inicializado');
            
        } catch (error) {
            const enhancement = await this.errorTransmuter.transmute(
                error instanceof Error ? error : new Error(String(error))
            );
            console.error('Error transmutado:', enhancement);
            throw error;
        }
    }
    
    public async getQuantumPrice(symbol: string): Promise<QuantumMarketData> {
        try {
            const response = await fetch(`https://api.binance.com/api/v3/ticker/price?symbol=${symbol}`, {
                headers: {
                    'X-MBX-APIKEY': this.apiKey
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error API Binance: ${response.statusText}`);
            }
            
            const data: BinanceResponse = await response.json();
            const price = parseFloat(data.price);
            
            // Generar frecuencia determinística
            const quantum_frequency = this.frequencyGenerator.generateQuantumFrequency(
                symbol + price.toString()
            );
            
            // Generar patrón de resonancia
            const resonance_pattern = this.frequencyGenerator.generateResonancePattern(8, symbol);
            
            const marketData: QuantumMarketData = {
                symbol,
                price,
                volume: 0,
                timestamp: Date.now(),
                quantum_frequency,
                resonance_pattern
            };
            
            this.marketData.set(symbol, marketData);
            return marketData;
            
        } catch (error) {
            const enhancement = await this.errorTransmuter.transmute(
                error instanceof Error ? error : new Error(String(error)),
                'getQuantumPrice'
            );
            console.error('Error transmutado:', enhancement);
            throw error;
        }
    }
    
    public subscribeToQuantumMarketStream(symbol: string): void {
        if (!this.ws) {
            throw new Error('WebSocket no inicializado');
        }
        
        const streamName = `${symbol.toLowerCase()}@ticker`;
        const msg = JSON.stringify({
            method: 'SUBSCRIBE',
            params: [streamName],
            id: Date.now()
        });
        
        this.ws.send(msg);
    }
    
    private async initializeWebSocket(): Promise<void> {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket('wss://stream.binance.com:9443/ws');
            
            this.ws.on('open', () => {
                console.log('WebSocket cuántico conectado');
                resolve();
            });
            
            this.ws.on('message', async (data: WebSocket.Data) => {
                try {
                    const message = JSON.parse(data.toString());
                    
                    if (message.e === '24hrTicker') {
                        await this.handleMarketData(message);
                    }
                    
                } catch (error) {
                    const enhancement = await this.errorTransmuter.transmute(
                        error instanceof Error ? error : new Error(String(error)),
                        'websocket_message'
                    );
                    console.error('Error transmutado en WebSocket:', enhancement);
                }
            });
            
            this.ws.on('error', async (error) => {
                const enhancement = await this.errorTransmuter.transmute(
                    error instanceof Error ? error : new Error(String(error)),
                    'websocket_error'
                );
                console.error('Error transmutado en WebSocket:', enhancement);
                reject(error);
            });
        });
    }
    
    private async handleMarketData(message: any): Promise<void> {
        const symbol = message.s;
        const currentData = this.marketData.get(symbol) || {
            symbol,
            price: parseFloat(message.c),
            volume: 0,
            timestamp: 0,
            quantum_frequency: 0,
            resonance_pattern: []
        };
        
        // Actualizar con nuevos datos
        currentData.price = parseFloat(message.c);
        currentData.volume = parseFloat(message.v);
        currentData.timestamp = message.E;
        
        // Regenerar frecuencia cuántica
        currentData.quantum_frequency = this.frequencyGenerator.generateQuantumFrequency(
            symbol + message.c
        );
        
        this.marketData.set(symbol, currentData);
    }
    
    public getQuantumMarketData(symbol: string): QuantumMarketData | undefined {
        return this.marketData.get(symbol);
    }
    
    public async close(): Promise<void> {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
    
    public getStats(): any {
        return {
            frequency: this.frequency,
            connected: this.ws !== null,
            symbols_tracked: this.marketData.size,
            error_transmuter: this.errorTransmuter.getStats(),
            frequency_generator: this.frequencyGenerator.getStats()
        };
    }
}

export default QuantumBinanceConnector;