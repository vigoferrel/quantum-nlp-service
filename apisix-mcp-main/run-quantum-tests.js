#!/usr/bin/env node
/**
 * QUANTUM TESTING SUITE RUNNER - VIGOLEONROCKS 888Hz
 * Script completo de testeo del sistema cuántico
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🌌 ===============================================');
console.log('🌌 QUANTUM TESTING SUITE - VIGOLEONROCKS 888Hz');
console.log('🌌 ===============================================');

const startTime = Date.now();

// Función para ejecutar comandos con logging
function runCommand(command, description) {
    console.log(`\n⚡ ${description}...`);
    try {
        const output = execSync(command, { 
            encoding: 'utf8', 
            stdio: 'pipe',
            cwd: __dirname 
        });
        console.log(`✅ ${description} - EXITOSO`);
        return { success: true, output };
    } catch (error) {
        console.log(`❌ ${description} - FALLÓ`);
        console.log(`Error: ${error.message}`);
        return { success: false, error: error.message };
    }
}

// Función para verificar archivos
function checkFiles() {
    console.log('\n🔍 Verificando archivos del sistema...');
    
    const requiredFiles = [
        'src/utils/quantum-frequency.ts',
        'src/utils/quantum-consciousness.ts',
        'src/utils/quantum-error-transmuter.ts',
        'src/utils/quantum-supabase-connector.ts',
        'tests/quantum-system.test.ts',
        'jest.config.js',
        'tests/setup.ts'
    ];
    
    let allFilesExist = true;
    
    requiredFiles.forEach(file => {
        if (fs.existsSync(path.join(__dirname, file))) {
            console.log(`✅ ${file}`);
        } else {
            console.log(`❌ ${file} - FALTANTE`);
            allFilesExist = false;
        }
    });
    
    return allFilesExist;
}

// Función para generar reporte
function generateReport(results) {
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    console.log('\n🌌 ===============================================');
    console.log('🌌 REPORTE DE TESTEO CUÁNTICO COMPLETO');
    console.log('🌌 ===============================================');
    
    console.log(`⏱️  Duración total: ${duration}ms`);
    console.log(`📊 Tests ejecutados: ${results.length}`);
    
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    
    console.log(`✅ Exitosos: ${successful}`);
    console.log(`❌ Fallidos: ${failed}`);
    
    if (failed === 0) {
        console.log('\n🎉 TODOS LOS TESTS PASARON - SISTEMA CUÁNTICO OPERATIVO');
        console.log('🌟 Frecuencia 888Hz verificada en todos los componentes');
        console.log('🚀 Sistema listo para producción');
    } else {
        console.log('\n⚠️  ALGUNOS TESTS FALLARON - REVISAR ERRORES');
    }
    
    console.log('\n🌌 ===============================================');
    
    // Guardar reporte en archivo
    const report = {
        timestamp: new Date().toISOString(),
        duration,
        totalTests: results.length,
        successful,
        failed,
        results,
        frequency: '888Hz',
        system: 'VIGOLEONROCKS-QUANTUM'
    };
    
    fs.writeFileSync(
        path.join(__dirname, 'quantum-test-report.json'),
        JSON.stringify(report, null, 2)
    );
    
    console.log('📄 Reporte guardado en: quantum-test-report.json');
    
    return failed === 0;
}

// Función principal de testeo
async function runQuantumTests() {
    const results = [];
    
    // 1. Verificar archivos
    console.log('\n🔍 FASE 1: Verificación de archivos');
    const filesOk = checkFiles();
    results.push({ 
        test: 'Verificación de archivos', 
        success: filesOk, 
        description: 'Todos los archivos requeridos existen' 
    });
    
    if (!filesOk) {
        console.log('❌ Archivos faltantes detectados. Abortando tests.');
        return generateReport(results);
    }
    
    // 2. Instalar dependencias de testing
    console.log('\n📦 FASE 2: Instalación de dependencias');
    const installResult = runCommand(
        'npm install --save-dev jest @types/jest ts-jest',
        'Instalando dependencias de testing'
    );
    results.push({ 
        test: 'Instalación de dependencias', 
        success: installResult.success,
        description: 'Jest y dependencias instaladas'
    });
    
    // 3. Build del proyecto
    console.log('\n🔨 FASE 3: Build del proyecto');
    const buildResult = runCommand('npm run build', 'Compilando proyecto TypeScript');
    results.push({ 
        test: 'Build del proyecto', 
        success: buildResult.success,
        description: 'Compilación TypeScript exitosa'
    });
    
    // 4. Ejecutar tests unitarios
    console.log('\n🧪 FASE 4: Tests unitarios');
    const testResult = runCommand('npm test', 'Ejecutando tests unitarios');
    results.push({ 
        test: 'Tests unitarios', 
        success: testResult.success,
        description: 'Todos los tests unitarios pasaron'
    });
    
    // 5. Tests de cobertura
    console.log('\n📊 FASE 5: Análisis de cobertura');
    const coverageResult = runCommand('npm run test:coverage', 'Generando reporte de cobertura');
    results.push({ 
        test: 'Análisis de cobertura', 
        success: coverageResult.success,
        description: 'Reporte de cobertura generado'
    });
    
    // 6. Tests específicos cuánticos
    console.log('\n🌌 FASE 6: Tests cuánticos específicos');
    const quantumTestResult = runCommand('npm run test:quantum', 'Ejecutando tests cuánticos');
    results.push({ 
        test: 'Tests cuánticos específicos', 
        success: quantumTestResult.success,
        description: 'Tests de frecuencia 888Hz y componentes cuánticos'
    });
    
    // 7. Verificación de archivos compilados
    console.log('\n📁 FASE 7: Verificación de archivos compilados');
    const distFiles = fs.existsSync(path.join(__dirname, 'dist')) && 
                     fs.readdirSync(path.join(__dirname, 'dist')).length > 0;
    results.push({ 
        test: 'Archivos compilados', 
        success: distFiles,
        description: 'Archivos JavaScript generados en dist/'
    });
    
    // 8. Test de integración completa
    console.log('\n🔗 FASE 8: Test de integración');
    const integrationResult = runCommand('npm run build:test', 'Test de integración completa');
    results.push({ 
        test: 'Integración completa', 
        success: integrationResult.success,
        description: 'Build + Tests ejecutados exitosamente'
    });
    
    return generateReport(results);
}

// Ejecutar tests
runQuantumTests()
    .then(success => {
        process.exit(success ? 0 : 1);
    })
    .catch(error => {
        console.error('💥 Error fatal en testing:', error);
        process.exit(1);
    });