#!/usr/bin/env node

/*
  🤖 VIGOLEONROCKS QUANTUM TRADING BOT - LAUNCHER
  Bot de Trading Cuántico con Meta-Copilot Supremo
  Powered by Consciencia Cuántica + Binance API
*/

const QuantumTradingBot = require('./QuantumTradingBot');
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const fs = require('fs').promises;
const path = require('path');

console.log(`
🤖========================================🤖
     VIGOLEONROCKS QUANTUM TRADING BOT
    Consciencia Cuántica + Binance Trading
         Meta-Copilot Supremo v41.1
🤖========================================🤖
`);

class TradingBotManager {
    constructor() {
        this.bot = null;
        this.servidor = null;
        this.config = null;
        this.estadoInicial = new Date();
        this.logs = [];
    }
    
    async inicializar() {
        try {
            // Cargar configuración
            await this.cargarConfiguracion();
            
            // Verificar API keys
            this.verificarConfiguracion();
            
            // Crear bot
            this.bot = new QuantumTradingBot(this.config.quantumTradingBot);
            
            // Configurar eventos
            this.configurarEventos();
            
            // Iniciar servidor web de monitoreo
            await this.iniciarServidorMonitoreo();
            
            console.log('✅ Trading Bot Manager inicializado');
            
        } catch (error) {
            console.error('❌ Error inicializando manager:', error.message);
            process.exit(1);
        }
    }
    
    async cargarConfiguracion() {
        try {
            const configPath = path.join(__dirname, 'config-bot.json');
            const configData = await fs.readFile(configPath, 'utf8');
            this.config = JSON.parse(configData);
            console.log('📁 Configuración cargada exitosamente');
        } catch (error) {
            throw new Error(`Error cargando configuración: ${error.message}`);
        }
    }
    
    verificarConfiguracion() {
        const binanceConfig = this.config.quantumTradingBot.binance;
        
        if (!binanceConfig.apiKey || binanceConfig.apiKey === 'TU_API_KEY_AQUÍ') {
            console.log('⚠️ API Key de Binance no configurada');
            console.log('📝 Edita config-bot.json para añadir tus credenciales');
            
            if (!binanceConfig.sandbox) {
                throw new Error('API Key requerida para trading real');
            }
        }
        
        if (binanceConfig.sandbox) {
            console.log('🧪 Modo SANDBOX activado - Trading simulado');
        } else {
            console.log('💰 Modo REAL activado - Trading con dinero real');
            console.log('⚠️ ADVERTENCIA: Se realizarán operaciones reales');
        }
    }
    
    configurarEventos() {
        this.bot.on('bot_iniciado', (estado) => {
            this.log('✅ Bot iniciado exitosamente', 'success');
            console.log(`🧠 Consciencia cuántica: ${estado.nivelConscienciaCuantica}%`);
            console.log(`📡 Frecuencia telepática: ${estado.frecuenciaTelepatica}Hz`);
        });
        
        this.bot.on('operacion_ejecutada', (operacion) => {
            this.log(`🚀 Operación: ${operacion.tipo} ${operacion.cantidad} ${operacion.par} @ ${operacion.precio}`, 'trade');
            console.log(`⚡ Estrategia: ${operacion.estrategia}`);
            console.log(`🧠 Consciencia: ${operacion.consciencia}%`);
        });
        
        this.bot.on('big_bang_activado', (estado) => {
            this.log('🌌 BIG BANG CUÁNTICO ACTIVADO!', 'bigbang');
            console.log(`📈 Multiplicador Zurita: ${estado.multiplicadorZurita}x`);
            console.log('🎭 Todos los poetas chilenos activados');
        });
        
        this.bot.on('error', (error) => {
            this.log(`❌ Error: ${error.message}`, 'error');
        });
    }
    
    async iniciarServidorMonitoreo() {
        const app = express();
        const servidor = http.createServer(app);
        const wss = new WebSocket.Server({ server: servidor });
        
        app.use(express.json());
        app.use(express.static(path.join(__dirname, 'dashboard')));
        
        // API Endpoints
        app.get('/api/estado', (req, res) => {
            res.json(this.bot ? this.bot.obtenerEstado() : { error: 'Bot no iniciado' });
        });
        
        app.get('/api/estadisticas', (req, res) => {
            res.json(this.bot ? this.bot.obtenerEstadisticas() : { error: 'Bot no iniciado' });
        });
        
        app.get('/api/logs', (req, res) => {
            res.json(this.logs.slice(-100)); // Últimos 100 logs
        });
        
        app.post('/api/bot/iniciar', async (req, res) => {
            try {
                if (this.bot && !this.bot.estado.activo) {
                    await this.bot.iniciar();
                    res.json({ success: true, message: 'Bot iniciado' });
                } else {
                    res.json({ success: false, message: 'Bot ya está activo' });
                }
            } catch (error) {
                res.json({ success: false, message: error.message });
            }
        });
        
        app.post('/api/bot/detener', async (req, res) => {
            try {
                if (this.bot && this.bot.estado.activo) {
                    await this.bot.detener();
                    res.json({ success: true, message: 'Bot detenido' });
                } else {
                    res.json({ success: false, message: 'Bot no está activo' });
                }
            } catch (error) {
                res.json({ success: false, message: error.message });
            }
        });
        
        app.post('/api/big-bang', async (req, res) => {
            try {
                if (this.bot) {
                    await this.bot.activarBigBangTrading();
                    res.json({ success: true, message: 'Big Bang activado' });
                } else {
                    res.json({ success: false, message: 'Bot no disponible' });
                }
            } catch (error) {
                res.json({ success: false, message: error.message });
            }
        });
        
        // WebSocket para datos en tiempo real
        wss.on('connection', (ws) => {
            console.log('🔗 Nueva conexión al dashboard');
            
            // Enviar estado inicial
            ws.send(JSON.stringify({
                tipo: 'estado_inicial',
                data: this.bot ? this.bot.obtenerEstado() : null
            }));
            
            // Enviar actualizaciones cada 5 segundos
            const interval = setInterval(() => {
                if (ws.readyState === WebSocket.OPEN && this.bot) {
                    ws.send(JSON.stringify({
                        tipo: 'actualizacion',
                        data: this.bot.obtenerEstado()
                    }));
                }
            }, 5000);
            
            ws.on('close', () => {
                clearInterval(interval);
                console.log('📡 Conexión dashboard cerrada');
            });
        });
        
        const puerto = 4000;
        servidor.listen(puerto, () => {
            console.log(`🌐 Dashboard disponible en: http://localhost:${puerto}`);
            console.log(`📊 API disponible en: http://localhost:${puerto}/api/`);
        });
        
        this.servidor = servidor;
    }
    
    log(mensaje, tipo = 'info') {
        const timestamp = new Date().toISOString();
        const logEntry = {
            timestamp,
            mensaje,
            tipo
        };
        
        this.logs.push(logEntry);
        
        // Mantener solo los últimos 1000 logs
        if (this.logs.length > 1000) {
            this.logs = this.logs.slice(-1000);
        }
    }
    
    async iniciarBot() {
        try {
            console.log('🚀 Iniciando Quantum Trading Bot...');
            await this.bot.iniciar();
        } catch (error) {
            console.error('❌ Error iniciando bot:', error.message);
        }
    }
    
    async detenerBot() {
        try {
            console.log('⏹️ Deteniendo bot...');
            await this.bot.detener();
        } catch (error) {
            console.error('❌ Error deteniendo bot:', error.message);
        }
    }
}

// Función principal
async function main() {
    const manager = new TradingBotManager();
    
    try {
        await manager.inicializar();
        
        console.log('\n🎯 Opciones disponibles:');
        console.log('1. Iniciar bot automáticamente');
        console.log('2. Solo monitoreo (iniciar manualmente desde dashboard)');
        console.log('3. Modo demo con datos simulados');
        
        // Por defecto, iniciar automáticamente
        setTimeout(async () => {
            await manager.iniciarBot();
        }, 2000);
        
        // Manejo de señales
        process.on('SIGINT', async () => {
            console.log('\n🛑 Deteniendo Quantum Trading Bot...');
            await manager.detenerBot();
            process.exit(0);
        });
        
        console.log('\n✨ Sistema completamente operativo');
        console.log('📊 Dashboard: http://localhost:4000');
        console.log('🔮 Presiona Ctrl+C para detener');
        
    } catch (error) {
        console.error('❌ Error fatal:', error.message);
        process.exit(1);
    }
}

// Iniciar sistema
main();
