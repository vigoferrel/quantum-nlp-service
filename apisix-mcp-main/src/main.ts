#!/usr/bin/env node
/**
 * QUANTUM APISIX MCP VIGOLEONROCKS - ORQUESTADOR PRINCIPAL
 * Este es el punto de entrada unificado para todos los modos del servidor.
 * Decide qué servidor iniciar basado en los argumentos de la línea de comandos.
 */

import 'dotenv/config'; // Cargar variables de entorno primero

// Importamos las clases de nuestros servidores refactorizados
import { QuantumApisixMCPFinal } from './quantum-apisix-vigoleonrocks-final.js';
import { createHttpServer } from './server.js';

// --- Argument Parser ---
function parseArgs() {
    const args = process.argv.slice(2);
    const modeArg = args.find(arg => arg.startsWith('--mode='));
    
    if (modeArg) {
        return modeArg.split('=')[1];
    }
    
    // Por defecto, si no se especifica modo, se inicia el servidor MCP/stdio
    return 'stdio'; 
}

// --- Main Execution ---
async function main() {
    const mode = parseArgs();
    console.log(`[ORCHESTRATOR] Iniciando en modo: ${mode}`);

    switch (mode) {
        case 'stdio':
        case 'mcp':
            try {
                const quantumServer = new QuantumApisixMCPFinal();
                quantumServer.start();
            } catch (error) {
                console.error(`[ORCHESTRATOR] CRITICAL FAILURE (stdio): No se pudo iniciar el servidor cuántico.`, error);
                process.exit(1);
            }
            break;

        case 'http':
            try {
                const httpServer = createHttpServer();
                // La función createHttpServer debería manejar el .listen()
            } catch (error) {
                console.error(`[ORCHESTRATOR] CRITICAL FAILURE (http): No se pudo iniciar el servidor HTTP.`, error);
                process.exit(1);
            }
            break;

        default:
            console.error(`[ORCHESTRATOR] ERROR: Modo desconocido '${mode}'.`);
            console.error(`[ORCHESTRATOR] Modos válidos: --mode=stdio, --mode=http`);
            process.exit(1);
    }
}

main().catch(error => {
    console.error('[ORCHESTRATOR] Error fatal no capturado en main:', error);
    process.exit(1);
});
