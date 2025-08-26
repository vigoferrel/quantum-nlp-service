#!/usr/bin/env node

/**
 * VIGOLEONROCKS CONSTRAINED SUPREMACY BENCHMARK v6.0-Modular
 * ==========================================================
 * Un framework modular para probar la supremacía de IA bajo restricciones.
 */

const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../../.env.global') });

const Logger = require('./src/Logger');
const ConfigLoader = require('./src/ConfigLoader'); // Lo mantendremos por ahora para leer la suite
const DataGenerator = require('./src/DataGenerator');
const TestRunner = require('./src/TestRunner');
const Evaluator = require('./src/Evaluator');
const ReportGenerator = require('./src/ReportGenerator');

async function main() {
  Logger.header('🚀 INICIANDO VIGOLEONROCKS CONSTRAINED SUPREMACY BENCHMARK v6.0');

  try {
    // 1. Cargar Configuración de la Suite de Pruebas
    const configLoader = new ConfigLoader(); // Solo para la suite de pruebas
    const config = await configLoader.load();
    const { testSuite } = config;

    // El entorno ahora viene de process.env (cargado del .env.global)
    const environment = {
      ENDPOINT: `http://localhost:${process.env.PORT || 3000}/api/constrained_holistic_analysis`,
      REQUEST_TIMEOUT: process.env.REQUEST_TIMEOUT || 600000,
      IOPS_LIMIT: process.env.IOPS_LIMIT || 6000,
      DB_CONNECTIONS_MAX: process.env.DB_CONNECTIONS_MAX || 240,
    };

    // 2. Instanciar Módulos
    const testRunner = new TestRunner(environment);
    const evaluator = new Evaluator(environment);
    const reportGenerator = new ReportGenerator(environment);

    // 3. Ejecutar Pruebas en Paralelo
    const testPromises = testSuite.map(testConfig => {
      Logger.info(`🔧 Preparando prueba: ${testConfig.description}`);
      const context = DataGenerator.generateFor(testConfig);
      return testRunner.run(testConfig, context, environment);
    });

    const settledResults = await Promise.allSettled(testPromises);

    // 4. Evaluar Resultados
    const detailedResults = settledResults.map((result, index) => {
      const testConfig = testSuite[index];
      if (result.status === 'rejected') {
        Logger.error(`Prueba fallida catastróficamente: ${testConfig.description}. Razón: ${result.reason.message}`);
        return {
          id: testConfig.id,
          description: testConfig.description,
          pass: false,
          error: 'Catastrophic failure in test runner.',
        };
      }

      const evaluation = evaluator.evaluate(result.value, testConfig);
      if (evaluation.pass) {
        Logger.success(`Prueba completada: ${testConfig.description}`);
      } else {
        Logger.error(`Prueba fallida: ${testConfig.description}`);
      }
      Logger.result(`Eficiencia: ${evaluation.efficiencyScore?.toFixed(2) ?? 0}% | Calidad: ${evaluation.qualityScore?.toFixed(2) ?? 0}% -> Score Holístico: ${evaluation.holisticScore?.toFixed(2) ?? 0}%`);

      return { id: testConfig.id, description: testConfig.description, ...evaluation };
    });

    // 5. Calcular Score Final y Clasificar
    const successfulTests = detailedResults.filter(r => r.holisticScore > 0);
    const finalScore = successfulTests.reduce((acc, r) => acc + r.holisticScore, 0) / (successfulTests.length || 1);

    Logger.header('🏆 VEREDICTO FINAL - EFICIENCIA Y SUPREMACÍA RESTRINGIDA');
    Logger.info(`🧠 ÍNDICE DE SUPREMACÍA RESTRINGIDA: ${finalScore.toFixed(2)}%`);
    Logger.info(`🎯 CLASIFICACIÓN: ${classifyConstrainedSupremacy(finalScore)}`);

    // 6. Guardar Reporte
    const reportPath = await reportGenerator.save(finalScore, detailedResults);
    Logger.success(`Reporte guardado en: ${reportPath}`);

  } catch (error) {
    Logger.error(`El benchmark no pudo completarse: ${error.message}`);
    process.exit(1);
  }
}

function classifyConstrainedSupremacy(score) {
  if (score >= 90) return 'SUPREMACÍA EFICIENTE TRASCENDENTAL - Inteligencia Adaptativa Cuántica';
  if (score >= 75) return 'ALTO RENDIMIENTO EN RESTRICCIONES - Optimización Holística';
  if (score >= 50) return 'OPERACIONAL BAJO PRESIÓN';
  return 'REQUIERE OPTIMIZACIÓN';
}

main();
