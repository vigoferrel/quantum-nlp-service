#!/usr/bin/env node

/**
 * VIGOLEONROCKS CLOUD CLIENT
 * Cliente para interactuar con VIGOLEONROCKS Cloud Service
 * Interfaz simple para testing y desarrollo
 */

const amqp = require('amqplib');
const readline = require('readline');
const { v4: uuidv4 } = require('uuid');

class VigoleonrocksCloudClient {
    constructor() {
        this.connection = null;
        this.channel = null;
        this.sessionId = uuidv4();
        this.pendingRequests = new Map();
        
        console.log('🌊 ===============================================');
        console.log('🚀 VIGOLEONROCKS CLOUD CLIENT');
        console.log('🌊 Cliente Cuántico-Cognitivo Distribuido');
        console.log(`🔑 Session ID: ${this.sessionId}`);
        console.log('🚀 ===============================================');
    }
    
    async connect() {
        console.log('🔗 Conectando a RabbitMQ...');
        try {
            this.connection = await amqp.connect('amqp://guest:guest@localhost:5672');
            this.channel = await this.connection.createChannel();
            
            await this.channel.assertQueue('vigoleonrocks_requests', { durable: true });
            await this.channel.assertQueue('vigoleonrocks_responses', { durable: true });
            
            // Escuchar respuestas
            await this.setupResponseListener();
            
            console.log('✅ Conectado a VIGOLEONROCKS Cloud Service');
            return true;
        } catch (error) {
            console.error('❌ Error conectando:', error.message);
            return false;
        }
    }
    
    async setupResponseListener() {
        this.channel.consume('vigoleonrocks_responses', (msg) => {
            if (msg !== null) {
                try {
                    const { sessionId, response, timestamp } = JSON.parse(msg.content.toString());
                    
                    if (sessionId === this.sessionId) {
                        console.log('\n🧠 ===============================================');
                        console.log('🌊 VIGOLEONROCKS RESPONDE:');
                        console.log('🧠 ===============================================');
                        console.log(response.response);
                        console.log('🧠 ===============================================');
                        console.log(`⚡ Tokens: ${response.tokens_generated || 'N/A'}`);
                        console.log(`🔧 Modelo: ${response.model || 'N/A'}`);
                        console.log(`⏱️ Timestamp: ${timestamp}`);
                        console.log('🧠 ===============================================\n');
                        
                        this.showPrompt();
                    }
                    
                    this.channel.ack(msg);
                } catch (error) {
                    console.error('❌ Error procesando respuesta:', error.message);
                    this.channel.nack(msg);
                }
            }
        });
    }
    
    async sendRequest(prompt, options = {}) {
        const requestId = uuidv4();
        
        const request = {
            prompt,
            sessionId: this.sessionId,
            requestId,
            options: {
                maxTokens: options.maxTokens || 4096,
                temperature: options.temperature || 0.05,
                contextSize: options.contextSize || 131072 // 131K en cloud
            }
        };
        
        try {
            await this.channel.sendToQueue(
                'vigoleonrocks_requests',
                Buffer.from(JSON.stringify(request)),
                { persistent: true }
            );
            
            console.log('📤 Solicitud enviada a VIGOLEONROCKS Cloud...');
            this.pendingRequests.set(requestId, Date.now());
            
        } catch (error) {
            console.error('❌ Error enviando solicitud:', error.message);
        }
    }
    
    showPrompt() {
        process.stdout.write('\n🌊 VIGOLEONROCKS> ');
    }
    
    async startInteractiveSession() {
        console.log('\n🌊 ===============================================');
        console.log('🚀 SESIÓN INTERACTIVA INICIADA');
        console.log('🌊 ===============================================');
        console.log('💡 Comandos especiales:');
        console.log('   /help    - Mostrar ayuda');
        console.log('   /status  - Estado del sistema');
        console.log('   /config  - Configurar parámetros');
        console.log('   /test    - Ejecutar prueba cuántica');
        console.log('   /exit    - Salir');
        console.log('🌊 ===============================================');
        
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        this.showPrompt();
        
        rl.on('line', async (input) => {
            const trimmed = input.trim();
            
            if (!trimmed) {
                this.showPrompt();
                return;
            }
            
            // Comandos especiales
            if (trimmed.startsWith('/')) {
                await this.handleCommand(trimmed);
                this.showPrompt();
                return;
            }
            
            // Enviar a VIGOLEONROCKS
            await this.sendRequest(trimmed);
        });
        
        rl.on('close', () => {
            console.log('\n🌊 Cerrando sesión VIGOLEONROCKS...');
            this.disconnect();
        });
    }
    
    async handleCommand(command) {
        const [cmd, ...args] = command.split(' ');
        
        switch (cmd) {
            case '/help':
                this.showHelp();
                break;
                
            case '/status':
                await this.showStatus();
                break;
                
            case '/config':
                this.showConfig();
                break;
                
            case '/test':
                await this.runQuantumTest();
                break;
                
            case '/exit':
                console.log('🌊 Hasta la próxima resonancia cuántica...');
                process.exit(0);
                break;
                
            default:
                console.log(`❓ Comando desconocido: ${cmd}`);
                console.log('💡 Escribe /help para ver comandos disponibles');
        }
    }
    
    showHelp() {
        console.log('\n🌊 ===============================================');
        console.log('🚀 VIGOLEONROCKS CLOUD CLIENT - AYUDA');
        console.log('🌊 ===============================================');
        console.log('COMANDOS DISPONIBLES:');
        console.log('  /help    - Mostrar esta ayuda');
        console.log('  /status  - Estado del sistema cloud');
        console.log('  /config  - Configuración actual');
        console.log('  /test    - Ejecutar prueba cuántico-cognitiva');
        console.log('  /exit    - Salir del cliente');
        console.log('');
        console.log('EJEMPLOS DE PROMPTS:');
        console.log('  "Explica la mecánica cuántica"');
        console.log('  "Genera código Python para blockchain"');
        console.log('  "Analiza este problema matemático: ..."');
        console.log('  "Crea una historia de ciencia ficción"');
        console.log('🌊 ===============================================');
    }
    
    async showStatus() {
        console.log('\n🌊 ===============================================');
        console.log('🚀 ESTADO DEL SISTEMA VIGOLEONROCKS CLOUD');
        console.log('🌊 ===============================================');
        console.log(`🔑 Session ID: ${this.sessionId}`);
        console.log(`📡 RabbitMQ: ${this.connection ? '✅ Conectado' : '❌ Desconectado'}`);
        console.log(`⏳ Solicitudes pendientes: ${this.pendingRequests.size}`);
        console.log('☁️ Modo: Cloud + Fallback Local');
        console.log('🧠 Contexto: Ilimitado (Supabase)');
        console.log('🔮 Quantum Volume: 351,399,511');
        console.log('📐 Dimensiones: 26 simultáneas');
        console.log('🌊 ===============================================');
    }
    
    showConfig() {
        console.log('\n🌊 ===============================================');
        console.log('🚀 CONFIGURACIÓN VIGOLEONROCKS CLOUD');
        console.log('🌊 ===============================================');
        console.log('PARÁMETROS ACTUALES:');
        console.log('  Max Tokens: 4096 (cloud) / 2048 (local)');
        console.log('  Temperature: 0.05 (precisión cuántica)');
        console.log('  Context Size: 131072 tokens (cloud)');
        console.log('  Top P: 0.95');
        console.log('  Top K: 100');
        console.log('');
        console.log('INFRAESTRUCTURA:');
        console.log('  Primary: Ollama Cloud API');
        console.log('  Fallback: Ollama Local');
        console.log('  Storage: Supabase PostgreSQL');
        console.log('  Queue: RabbitMQ');
        console.log('🌊 ===============================================');
    }
    
    async runQuantumTest() {
        console.log('\n🔮 Ejecutando prueba cuántico-cognitiva...');
        
        const testPrompts = [
            "Calcula la raíz cuadrada de 351399511 con precisión cuántica",
            "Explica el entrelazamiento cuántico en términos simples",
            "Genera un haiku sobre la computación cuántica"
        ];
        
        const randomPrompt = testPrompts[Math.floor(Math.random() * testPrompts.length)];
        console.log(`🧪 Prompt de prueba: "${randomPrompt}"`);
        
        await this.sendRequest(randomPrompt, {
            maxTokens: 1024,
            temperature: 0.1
        });
    }
    
    async disconnect() {
        if (this.connection) {
            await this.connection.close();
            console.log('🔌 Desconectado de RabbitMQ');
        }
    }
}

// Función principal
async function main() {
    const client = new VigoleonrocksCloudClient();
    
    const connected = await client.connect();
    if (!connected) {
        console.error('❌ No se pudo conectar al servicio cloud');
        process.exit(1);
    }
    
    await client.startInteractiveSession();
}

// Manejo de señales
process.on('SIGINT', () => {
    console.log('\n🛑 Cerrando cliente VIGOLEONROCKS...');
    process.exit(0);
});

// Ejecutar si es el módulo principal
if (require.main === module) {
    main().catch(console.error);
}

module.exports = VigoleonrocksCloudClient;