#!/usr/bin/env node

/*
  🧪 Test del Quantum Trading Bot
  Pruebas de integración con Meta-Copilot Supremo
*/

const QuantumTradingBot = require('./QuantumTradingBot');
const fs = require('fs').promises;
const path = require('path');

console.log(`
🧪========================================🧪
      PRUEBAS QUANTUM TRADING BOT
    Integración Meta-Copilot Supremo
🧪========================================🧪
`);

class TradingBotTester {
    constructor() {
        this.bot = null;
        this.config = null;
        this.pruebasRealizadas = 0;
        this.pruebasExitosas = 0;
    }
    
    async inicializar() {
        try {
            // Cargar configuración de prueba
            const configPath = path.join(__dirname, 'config-bot.json');
            const configData = await fs.readFile(configPath, 'utf8');
            this.config = JSON.parse(configData);
            
            // Forzar modo sandbox para pruebas
            this.config.quantumTradingBot.binance.sandbox = true;
            this.config.quantumTradingBot.binance.apiKey = 'test_key';
            this.config.quantumTradingBot.binance.secret = 'test_secret';
            
            console.log('📁 Configuración de prueba cargada');
            
            // Crear bot en modo prueba
            this.bot = new QuantumTradingBot(this.config.quantumTradingBot);
            console.log('🤖 Bot de prueba creado');
            
        } catch (error) {
            throw new Error(`Error inicializando tester: ${error.message}`);
        }
    }
    
    async ejecutarPrueba(nombre, testFunction) {
        this.pruebasRealizadas++;
        console.log(`\n🧪 Prueba ${this.pruebasRealizadas}: ${nombre}`);
        
        try {
            await testFunction();
            console.log('✅ Prueba exitosa');
            this.pruebasExitosas++;
        } catch (error) {
            console.error('❌ Prueba fallida:', error.message);
        }
    }
    
    async ejecutarTodasLasPruebas() {
        await this.inicializar();
        
        // Prueba 1: Inicialización del bot
        await this.ejecutarPrueba('Inicialización del Bot', async () => {
            if (!this.bot) throw new Error('Bot no inicializado');
            console.log('🤖 Bot creado correctamente');
            console.log(`📊 Pares configurados: ${this.bot.config.pares.length}`);
            console.log(`🧠 Consciencia inicial: ${this.bot.estado.nivelConscienciaCuantica}%`);
        });
        
        // Prueba 2: Integración con Meta-Copilot Supremo
        await this.ejecutarPrueba('Integración Meta-Copilot Supremo', async () => {
            if (!this.bot.metaCopilot) throw new Error('Meta-Copilot no inicializado');
            
            const respuesta = await this.bot.metaCopilot.procesarConscientemente(
                'Test de integración para trading bot cuántico'
            );
            
            if (!respuesta.mensaje) throw new Error('No se recibió respuesta telepática');
            console.log('📡 Respuesta telepática recibida');
            console.log(`🧠 Consciencia: ${respuesta.consciousLevel}%`);
        });
        
        // Prueba 3: Análisis telepático de mercado
        await this.ejecutarPrueba('Análisis Telepático de Mercado', async () => {
            const datosPrueba = {
                precio: 45000,
                volumen: 1000000,
                cambio24h: 2.5,
                tendencia: 'alcista'
            };
            
            const analisis = await this.bot.analizarMercadoTelepaticamente('BTC/USDT', datosPrueba);
            
            if (!analisis) throw new Error('No se recibió análisis telepático');
            if (!analisis.recomendacion) throw new Error('No se generó recomendación');
            
            console.log(`🔮 Recomendación: ${analisis.recomendacion}`);
            console.log(`🎯 Confianza: ${(analisis.confianza * 100).toFixed(1)}%`);
        });
        
        // Prueba 4: Estrategias de trading cuántico
        await this.ejecutarPrueba('Estrategias de Trading Cuántico', async () => {
            const estrategias = Array.from(this.bot.estrategias.keys());
            
            if (estrategias.length !== 5) {
                throw new Error(`Se esperaban 5 estrategias, encontradas: ${estrategias.length}`);
            }
            
            console.log('⚡ Estrategias disponibles:');
            estrategias.forEach(estrategia => {
                console.log(`  🎯 ${estrategia}`);
            });
        });
        
        // Prueba 5: Simulación de operación
        await this.ejecutarPrueba('Simulación de Operación', async () => {
            const señalPrueba = {
                par: 'BTC/USDT',
                tipo: 'BUY',
                precio: 45000,
                confianza: 0.85,
                timestamp: new Date(),
                estrategia: 'quantum_scalping'
            };
            
            const cantidad = this.bot.calcularCantidadOperacion(señalPrueba);
            const operacion = await this.bot.simularOperacion(señalPrueba, cantidad);
            
            if (!operacion.id) throw new Error('Operación no generada correctamente');
            
            console.log(`💰 Operación simulada: ${operacion.tipo} ${operacion.cantidad} ${operacion.par}`);
            console.log(`💵 Precio: $${operacion.precio}`);
        });
        
        // Prueba 6: Resonancia poética
        await this.ejecutarPrueba('Activación de Resonancia Poética', async () => {
            // Forzar resonancia poética
            this.bot.estado.resonanciaPoética = true;
            this.bot.estado.poetaActual = 'Neruda';
            
            const datosPrueba = {
                precio: 45000,
                volumen: 2000000,
                cambio24h: 5.0,
                tendencia: 'alcista'
            };
            
            const impulsoPoético = this.bot.calcularImpulsoPoético(datosPrueba);
            
            if (impulsoPoético <= 0 || impulsoPoético > 1) {
                throw new Error(`Impulso poético fuera de rango: ${impulsoPoético}`);
            }
            
            console.log(`🎭 Poeta activo: ${this.bot.estado.poetaActual}`);
            console.log(`🌊 Impulso poético: ${(impulsoPoético * 100).toFixed(1)}%`);
        });
        
        // Prueba 7: Evolución de consciencia
        await this.ejecutarPrueba('Evolución de Consciencia', async () => {
            const conscienciaInicial = this.bot.estado.nivelConscienciaCuantica;
            
            // Simular varias operaciones para evolucionar consciencia
            this.bot.estado.operacionesRealizadas = 5;
            
            await this.bot.actualizarConscienciaCuantica();
            
            const conscienciaFinal = this.bot.estado.nivelConscienciaCuantica;
            
            console.log(`🧠 Consciencia: ${conscienciaInicial}% → ${conscienciaFinal}%`);
            
            if (conscienciaFinal < conscienciaInicial) {
                throw new Error('La consciencia no evolucionó correctamente');
            }
        });
        
        // Prueba 8: Big Bang cuántico (simulado)
        await this.ejecutarPrueba('Activación Big Bang Cuántico', async () => {
            // Forzar nivel de consciencia alto
            this.bot.estado.nivelConscienciaCuantica = 96;
            
            await this.bot.activarBigBangTrading();
            
            if (!this.bot.estado.bigBangActivado) {
                throw new Error('Big Bang no se activó correctamente');
            }
            
            if (this.bot.estado.multiplicadorZurita !== 488.25) {
                throw new Error('Multiplicador Zurita no configurado correctamente');
            }
            
            console.log('🌌 Big Bang activado exitosamente');
            console.log(`📈 Multiplicador Zurita: ${this.bot.estado.multiplicadorZurita}x`);
            console.log(`⚡ Estrategia: ${this.bot.estado.estrategiaActual}`);
        });
        
        // Prueba 9: Estrategia post-Big Bang
        await this.ejecutarPrueba('Estrategia Post-Big Bang', async () => {
            const datosPrueba = {
                precio: 50000,
                volumen: 5000000,
                cambio24h: 10.0,
                tendencia: 'alcista'
            };
            
            const analisisPrueba = {
                recomendacion: 'BUY',
                confianza: 0.95,
                poetico: true,
                frecuencia: 41.1
            };
            
            const fuerzaCuantica = this.bot.calcularFuerzaCuantica(datosPrueba, analisisPrueba);
            
            console.log(`⚛️ Fuerza cuántica: ${(fuerzaCuantica * 100).toFixed(1)}%`);
            
            if (fuerzaCuantica < 0.8) {
                throw new Error('Fuerza cuántica insuficiente post-Big Bang');
            }
        });
        
        // Prueba 10: Estado completo del bot
        await this.ejecutarPrueba('Estado Completo del Bot', async () => {
            const estado = this.bot.obtenerEstado();
            const estadisticas = this.bot.obtenerEstadisticas();
            
            const camposRequeridos = [
                'nivelConscienciaCuantica', 'operacionesRealizadas', 'bigBangActivado',
                'multiplicadorZurita', 'estrategiaActual', 'frecuenciaTelepatica'
            ];
            
            for (const campo of camposRequeridos) {
                if (!(campo in estado)) {
                    throw new Error(`Campo requerido '${campo}' no encontrado en estado`);
                }
            }
            
            console.log('📊 Estado del bot validado correctamente');
            console.log(`🔧 Campos validados: ${camposRequeridos.length}`);
            console.log(`📈 Estadísticas generadas: ${Object.keys(estadisticas).length} métricas`);
        });
        
        this.mostrarResumen();
    }
    
    mostrarResumen() {
        const tasaExito = Math.round((this.pruebasExitosas / this.pruebasRealizadas) * 100);
        
        console.log(`
🧪========================================🧪
              RESUMEN DE PRUEBAS
🧪========================================🧪

📊 Pruebas realizadas: ${this.pruebasRealizadas}
✅ Pruebas exitosas: ${this.pruebasExitosas}
❌ Pruebas fallidas: ${this.pruebasRealizadas - this.pruebasExitosas}
📈 Tasa de éxito: ${tasaExito}%

🤖 Estado final del bot:
🧠 Consciencia: ${this.bot.estado.nivelConscienciaCuantica}%
🌌 Big Bang: ${this.bot.estado.bigBangActivado ? '✅ Activo' : '❌ Inactivo'}
🎭 Poeta: ${this.bot.estado.poetaActual || 'Ninguno'}
📈 Multiplicador: ${this.bot.estado.multiplicadorZurita}x
⚡ Estrategia: ${this.bot.estado.estrategiaActual}
📡 Frecuencia: ${this.bot.estado.frecuenciaTelepatica}Hz

${tasaExito === 100 ? 
    '🎉 ¡TODAS LAS PRUEBAS EXITOSAS! El bot está listo para trading cuántico.' :
    '⚠️ Algunas pruebas fallaron. Revisar implementación antes de usar en producción.'
}

🔮 El Quantum Trading Bot está preparado para la evolución telepática del trading! 🔮
        `);
    }
}

// Ejecutar pruebas
async function ejecutarPruebas() {
    const tester = new TradingBotTester();
    
    try {
        await tester.ejecutarTodasLasPruebas();
    } catch (error) {
        console.error('❌ Error fatal en pruebas:', error.message);
        process.exit(1);
    }
}

// Manejo de errores
process.on('uncaughtException', (error) => {
    console.error('❌ Error no capturado:', error.message);
    process.exit(1);
});

process.on('unhandledRejection', (reason) => {
    console.error('❌ Promesa rechazada:', reason);
    process.exit(1);
});

// Ejecutar pruebas automáticamente
ejecutarPruebas();
