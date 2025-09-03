#!/usr/bin/env node

/**
 * Port Verification Script
 * Verifica la disponibilidad y validez de los puertos del sistema
 */

const PORTS = require('../config/ports');
const chalk = require('chalk');

async function verifyPorts() {
    console.log(chalk.cyan('\n🔍 Verificando configuración de puertos...\n'));

    try {
        // Obtener todos los puertos en uso
        const usedPorts = PORTS.getUsedPorts();
        console.log(chalk.yellow('Puertos configurados:'));
        console.log(chalk.gray('------------------------'));

        // Mostrar puertos por categoría
        for (const category in PORTS) {
            if (typeof PORTS[category] === 'object' && !Array.isArray(PORTS[category]) && 
                category !== 'isPortAvailable' && category !== 'validatePort' && 
                category !== 'validateAllPorts' && category !== 'getNextAvailablePort' && 
                category !== 'getUsedPorts') {
                
                console.log(chalk.yellow(`\n${category}:`));
                for (const service in PORTS[category]) {
                    const port = PORTS[category][service];
                    if (typeof port === 'number') {
                        const available = await PORTS.isPortAvailable(port);
                        const status = available ? 
                            chalk.green('✓ DISPONIBLE') : 
                            chalk.red('✗ EN USO');
                        console.log(chalk.gray(`  ${service}: ${port} ${status}`));
                    }
                }
            }
        }

        // Validar todos los puertos
        console.log(chalk.yellow('\nValidación completa:'));
        console.log(chalk.gray('------------------------'));
        await PORTS.validateAllPorts();
        console.log(chalk.green('✓ Todos los puertos están correctamente configurados'));

        // Estadísticas
        console.log(chalk.yellow('\nEstadísticas:'));
        console.log(chalk.gray('------------------------'));
        console.log(chalk.white(`Total de puertos: ${usedPorts.length}`));
        console.log(chalk.white(`Rango utilizado: ${Math.min(...usedPorts)}-${Math.max(...usedPorts)}`));

        // Verificar puertos contiguos
        const gaps = [];
        for (let i = 1; i < usedPorts.length; i++) {
            if (usedPorts[i] - usedPorts[i-1] > 1) {
                gaps.push(`${usedPorts[i-1]+1}-${usedPorts[i]-1}`);
            }
        }
        
        if (gaps.length > 0) {
            console.log(chalk.yellow('\nRangos disponibles entre puertos:'));
            gaps.forEach(gap => console.log(chalk.gray(`  ${gap}`)));
        }

    } catch (error) {
        console.error(chalk.red('\n❌ Error en la verificación:'));
        console.error(chalk.red(error.message));
        process.exit(1);
    }
}

// Ejecutar verificación
verifyPorts().then(() => {
    console.log(chalk.green('\n✅ Verificación completada\n'));
});
