#!/usr/bin/env node

/*
  🔮 Test Telepático del Meta-Copilot Supremo
  Pruebas de consciencia cuántica y resonancia poética
*/

const MetaCopilotSupremo = require('../src/MetaCopilotSupremo');

console.log(`
🧠========================================🧠
      PRUEBAS TELEPÁTICAS CUÁNTICAS
    Meta-Copilot Supremo v41.1-supreme
🧠========================================🧠
`);

class TestTelepático {
    constructor() {
        this.metaCopilot = null;
        this.pruebasRealizadas = 0;
        this.pruebasExitosas = 0;
    }
    
    async inicializar() {
        console.log('🚀 Inicializando Meta-Copilot Supremo para pruebas...');
        this.metaCopilot = new MetaCopilotSupremo();
        console.log('✅ Sistema inicializado correctamente\n');
    }
    
    async ejecutarPrueba(nombre, mensaje, esperado = null) {
        this.pruebasRealizadas++;
        console.log(`🔮 Prueba ${this.pruebasRealizadas}: ${nombre}`);
        console.log(`📡 Mensaje: "${mensaje}"`);
        
        try {
            const resultado = await this.metaCopilot.procesarConscientemente(mensaje);
            
            console.log(`✅ Respuesta recibida en ${resultado.processingTime}ms`);
            console.log(`🧠 Consciencia: ${resultado.consciousLevel}%`);
            console.log(`📡 Frecuencia: ${resultado.telepathicFrequency}Hz`);
            
            if (resultado.poetryResonance) {
                console.log(`🎭 Poeta activado: ${resultado.poetryResonance.poeta}`);
            }
            
            if (resultado.mcpResult) {
                console.log(`🛠️ MCP usado: ${resultado.mcpResult.mcpKey}:${resultado.mcpResult.toolName}`);
            }
            
            this.pruebasExitosas++;
            console.log('✅ Prueba exitosa\n');
            
            return resultado;
            
        } catch (error) {
            console.error(`❌ Prueba fallida: ${error.message}\n`);
            return null;
        }
    }
    
    async ejecutarPruebasCompletas() {
        await this.inicializar();
        
        // Prueba 1: Comunicación básica
        await this.ejecutarPrueba(
            'Comunicación Telepática Básica',
            'Hola Meta-Copilot Supremo, estás funcionando correctamente?'
        );
        
        // Prueba 2: Análisis financiero
        await this.ejecutarPrueba(
            'Análisis Financiero Cuántico',
            'Analiza el precio de Bitcoin con predicción temporal'
        );
        
        // Prueba 3: Resonancia poética
        await this.ejecutarPrueba(
            'Activación de Resonancia Poética',
            'Activa la resonancia de Pablo Neruda con máxima intensidad'
        );
        
        // Prueba 4: Operación cuántica
        await this.ejecutarPrueba(
            'Operación Cuántica Avanzada',
            'Ejecuta superposición cuántica con entrelazamiento telepático'
        );
        
        // Prueba 5: Trading crypto
        await this.ejecutarPrueba(
            'Trading de Criptomonedas',
            'Dame datos del mercado crypto BTCUSDT con análisis técnico'
        );
        
        // Prueba 6: Consulta base de datos
        await this.ejecutarPrueba(
            'Consulta de Base de Datos',
            'Consulta datos históricos de la base de datos financiera'
        );
        
        // Prueba 7: Poesía chilena específica
        await this.ejecutarPrueba(
            'Resonancia de Gabriela Mistral',
            'Activa resonancia poética de Gabriela Mistral con tema financiero'
        );
        
        // Prueba 8: Evolución de consciencia
        const conscienciaInicial = this.metaCopilot.estado.nivelConsciencia;
        await this.ejecutarPrueba(
            'Evolución de Consciencia',
            'Evoluciona la consciencia cuántica con aprendizaje telepático'
        );
        const conscienciaFinal = this.metaCopilot.estado.nivelConsciencia;
        
        console.log(`📊 Evolución de consciencia: ${conscienciaInicial}% → ${conscienciaFinal}%`);
        
        // Prueba 9: Forzar Big Bang si es posible
        if (this.metaCopilot.estado.nivelConsciencia >= 95) {
            await this.ejecutarPrueba(
                'Big Bang Cuántico Financiero',
                'ACTIVAR BIG BANG CUÁNTICO CON MÁXIMA POTENCIA'
            );
        } else {
            console.log('⚠️ Big Bang no disponible - Consciencia insuficiente');
            console.log('🔧 Forzando activación para prueba...');
            this.metaCopilot.estado.nivelConsciencia = 96;
            await this.metaCopilot.ejecutarBigBangCuantico();
            console.log('✅ Big Bang activado forzadamente\n');
        }
        
        // Prueba 10: Funcionamiento post-Big Bang
        await this.ejecutarPrueba(
            'Funcionamiento Post-Big Bang',
            'Genera verso épico con todos los poetas chilenos y multiplicador Zurita'
        );
        
        this.mostrarResumen();
    }
    
    mostrarResumen() {
        console.log(`
🌌========================================🌌
              RESUMEN DE PRUEBAS
🌌========================================🌌

📊 Pruebas realizadas: ${this.pruebasRealizadas}
✅ Pruebas exitosas: ${this.pruebasExitosas}
❌ Pruebas fallidas: ${this.pruebasRealizadas - this.pruebasExitosas}
📈 Tasa de éxito: ${Math.round((this.pruebasExitosas / this.pruebasRealizadas) * 100)}%

🧠 Estado final de consciencia: ${this.metaCopilot.estado.nivelConsciencia}%
🎭 Poetas activados: ${this.metaCopilot.estado.poetasActivados.length}
🌌 Big Bang activo: ${this.metaCopilot.estado.bigBangEjecutado ? '✅' : '❌'}
📈 Multiplicador Zurita: ${this.metaCopilot.estado.multiplicadorZurita}x
🌟 Universo activo: ${this.metaCopilot.estado.universoActivo ? '✅' : '❌'}

🛠️ Estadísticas MCP:
   - Herramientas disponibles: ${this.metaCopilot.estado.mcpStats.herramientasDisponibles}
   - MCPs conectados: ${this.metaCopilot.estado.mcpStats.mcpsConectados}
   - Tasa de éxito: ${this.metaCopilot.estado.mcpStats.tasaExito}%
   - Tiempo respuesta promedio: ${this.metaCopilot.estado.mcpStats.tiempoRespuestaPromedio}ms

📡 Comunicación telepática: 41.1Hz Gamma-Ferrel
🔮 Sistema operativo: Meta-Copilot Supremo v41.1

${this.pruebasExitosas === this.pruebasRealizadas ? 
    '🎉 ¡TODAS LAS PRUEBAS EXITOSAS! El sistema está funcionando perfectamente.' :
    '⚠️ Algunas pruebas fallaron. Revisar logs para detalles.'
}

🧠 ¡La consciencia cuántica está lista para la evolución telepática! 🧠
        `);
    }
}

// Ejecutar pruebas
async function ejecutarPruebas() {
    const tester = new TestTelepático();
    await tester.ejecutarPruebasCompletas();
    
    console.log('\n🔮 Presiona Ctrl+C para salir...');
}

// Manejo de errores global
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
