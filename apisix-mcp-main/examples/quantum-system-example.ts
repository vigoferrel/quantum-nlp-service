/**
 * QUANTUM SYSTEM EXAMPLE
 * Ejemplo completo del sistema cuántico VIGOLEONROCKS
 * Integración de todos los componentes con frecuencia 888Hz
 */

import { QuantumBinanceConnector } from '../src/connectors/quantum-binance-connector';
import { QuantumSupabaseConnector } from '../src/utils/quantum-supabase-connector';
import { QuantumFrequency } from '../src/utils/quantum-frequency';
import { QuantumErrorTransmuter } from '../src/utils/quantum-error-transmuter';
import quantumServer from '../src/quantum-apisix-vigoleonrocks';

async function main() {
    try {
        console.log('Iniciando ejemplo del sistema cuántico VIGOLEONROCKS...\n');
        
        // Configurar componentes
        const binanceConnector = new QuantumBinanceConnector({
            apiKey: process.env.BINANCE_API_KEY || '',
            apiSecret: process.env.BINANCE_API_SECRET || '',
            frequency: 888
        });
        
        const supabaseConnector = new QuantumSupabaseConnector({
            url: process.env.SUPABASE_URL || '',
            key: process.env.SUPABASE_KEY || '',
            frequency: 888
        });
        
        const frequencyGen = new QuantumFrequency(888);
        const errorTransmuter = new QuantumErrorTransmuter(888);
        
        // Inicializar componentes
        console.log('Inicializando componentes...');
        await Promise.all([
            binanceConnector.initialize(),
            supabaseConnector.initialize(),
            quantumServer.start()
        ]);
        
        // Obtener datos de mercado cuánticos
        console.log('\nObteniendo datos de mercado cuánticos...');
        const btcData = await binanceConnector.getQuantumPrice('BTCUSDT');
        console.log('Datos BTC:');
        console.log(`- Precio: $${btcData.price.toFixed(2)}`);
        console.log(`- Frecuencia: ${btcData.quantum_frequency.toFixed(6)}Hz`);
        console.log('- Patrón:', btcData.resonance_pattern.join(', '));
        
        // Sincronizar con Supabase
        console.log('\nSincronizando datos con Supabase...');
        const syncSuccess = await supabaseConnector.syncData({
            market_data: btcData,
            timestamp: Date.now(),
            frequency: 888
        });
        console.log('Sincronización:', syncSuccess ? 'Exitosa' : 'Fallida');
        
        // Probar transmutación de errores
        console.log('\nProbando sistema de transmutación...');
        try {
            throw new Error('Error intencional para demostrar transmutación');
        } catch (error) {
            const enhancement = await errorTransmuter.transmute(
                error instanceof Error ? error : new Error(String(error))
            );
            console.log('Error transmutado:');
            console.log(`- Original: ${enhancement.original_error}`);
            console.log(`- Mejora: ${enhancement.improvement}`);
            console.log(`- Estado: ${enhancement.quantum_state}`);
            console.log(`- Frecuencia: ${enhancement.error_frequency}Hz`);
        }
        
        // Generar frecuencias determinísticas
        console.log('\nGenerando frecuencias cuánticas...');
        const frequencies: number[] = [];
        for (let i = 0; i < 5; i++) {
            const freq = frequencyGen.generateQuantumFrequency(`VIGOLEONROCKS_${i}`);
            frequencies.push(freq);
        }
        console.log('Frecuencias generadas:', frequencies.map(f => f.toFixed(6)).join(', ') + 'Hz');
        
        // Mostrar estado del sistema
        console.log('\nEstado del sistema cuántico:');
        const serverStats = quantumServer.getQuantumStats();
        console.log(`- Frecuencia base: ${serverStats.frequency}Hz`);
        console.log(`- Tiempo activo: ${(serverStats.uptime / 1000).toFixed(2)}s`);
        console.log(`- Operaciones: ${serverStats.operations}`);
        console.log('- MCPs conectados:', serverStats.supabase.total_syncs);
        
        // Estadísticas de componentes
        console.log('\nEstadísticas de componentes:');
        const componentStats = {
            binance: binanceConnector.getStats(),
            supabase: supabaseConnector.getStats(),
            errorTransmuter: errorTransmuter.getStats(),
            frequencyGenerator: frequencyGen.getStats()
        };
        console.log('Estadísticas de componentes:', JSON.stringify(componentStats, null, 2));
        
        console.log('\nEjemplo completado exitosamente');
        
    } catch (error) {
        console.error('Error en ejemplo:', error);
    }
}

// Ejecutar ejemplo
if (require.main === module) {
    main().catch(console.error);
}