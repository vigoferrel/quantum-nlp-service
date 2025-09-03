/**
 * QUANTUM BINANCE EXAMPLE
 * Ejemplo de uso del conector cuántico de Binance
 * Integrado con sistema VIGOLEONROCKS
 */

import { QuantumBinanceConnector } from '../src/connectors/quantum-binance-connector';
import { QuantumFrequency } from '../src/utils/quantum-frequency';
import { QuantumErrorTransmuter } from '../src/utils/quantum-error-transmuter';

async function main() {
    try {
        console.log('Iniciando ejemplo de Quantum Binance...');
        
        // Configurar conector
        const connector = new QuantumBinanceConnector({
            apiKey: process.env.BINANCE_API_KEY || '',
            apiSecret: process.env.BINANCE_API_SECRET || '',
            frequency: 888,
            enableTransmutation: true
        });
        
        // Inicializar conector
        await connector.initialize();
        console.log('\nEstado del conector:');
        console.log(connector.getStats());
        
        // Obtener precio cuántico de BTC
        const btcData = await connector.getQuantumPrice('BTCUSDT');
        console.log('\nDatos cuánticos de BTC:');
        console.log(`- Precio: $${btcData.price.toFixed(2)}`);
        console.log(`- Frecuencia cuántica: ${btcData.quantum_frequency.toFixed(6)}`);
        console.log('- Patrón de resonancia:', btcData.resonance_pattern.join(', '));
        
        // Suscribirse a stream de mercado
        console.log('\nSuscribiendo a stream de mercado...');
        connector.subscribeToQuantumMarketStream('BTCUSDT');
        
        // Esperar y mostrar actualizaciones
        await new Promise(resolve => setTimeout(resolve, 10000));
        
        const updatedData = connector.getQuantumMarketData('BTCUSDT');
        if (updatedData) {
            console.log('\nDatos actualizados de BTC:');
            console.log(`- Precio: $${updatedData.price.toFixed(2)}`);
            console.log(`- Volumen: ${updatedData.volume.toFixed(2)}`);
            console.log(`- Frecuencia cuántica: ${updatedData.quantum_frequency.toFixed(6)}`);
        }
        
        // Probar transmutación de errores
        console.log('\nProbando transmutación de errores...');
        try {
            throw new Error('Error de prueba para transmutación');
        } catch (error) {
            const transmuter = new QuantumErrorTransmuter(888);
            const enhancement = await transmuter.transmute(
                error instanceof Error ? error : new Error(String(error)),
                'quantum_binance_example'
            );
            console.log('Error transmutado:');
            console.log(`- Original: ${enhancement.original_error}`);
            console.log(`- Mejora: ${enhancement.improvement}`);
            console.log(`- Estado cuántico: ${enhancement.quantum_state}`);
            console.log(`- Frecuencia: ${enhancement.error_frequency}`);
            console.log('- Patrón:', enhancement.resonance_pattern.join(', '));
        }
        
        // Probar generación de frecuencias
        console.log('\nProbando generación de frecuencias...');
        const freqGen = new QuantumFrequency(888);
        const frequencies: number[] = [];
        for (let i = 0; i < 5; i++) {
            frequencies.push(freqGen.generateQuantumFrequency(`BTCUSDT_${i}`));
        }
        console.log('Frecuencias generadas:', frequencies.map(f => f.toFixed(6)).join(', ') + ' Hz');
        
        // Cerrar conexión
        console.log('\nCerrando conexión...');
        await connector.close();
        
        console.log('\nEjemplo completado exitosamente');
        
    } catch (error) {
        console.error('Error en ejemplo:', error);
    }
}

// Ejecutar ejemplo
if (require.main === module) {
    main().catch(console.error);
}