require('dotenv').config();

const Optimizer = require('./vigoleonrocks-optimizer-supreme.js');

console.log('🚀 Iniciando prueba del VIGOLEONROCKS Optimizer Supreme');
console.log('📊 Mejoras implementadas:');
console.log('  ✅ TTL del caché cuántico aumentado a 60 segundos');
console.log('  ✅ Validación asíncrona en pipeline');
console.log('  ✅ Corrección de métodos estáticos');
console.log('');

async function testOptimizer() {
  const optimizer = new Optimizer();
  
  console.log('📋 Información del sistema:');
  console.log('  CPU Cores:', optimizer.systemInfo.cpu);
  console.log('  Memory (MB):', Math.round(optimizer.systemInfo.memory / 1024 / 1024));
  console.log('  Platform:', optimizer.systemInfo.platform);
  console.log('  Architecture:', optimizer.systemInfo.arch);
  console.log('');
  
  console.log('⚡ Ejecutando optimización...');
  const startTime = Date.now();
  
  try {
    const result = await optimizer.optimize();
    const endTime = Date.now();
    const executionTime = endTime - startTime;
    
    console.log('');
    console.log('📊 RESULTADOS:');
    console.log('  Estado:', result ? '✅ ÉXITO' : '❌ FALLO');
    console.log('  Tiempo de ejecución:', executionTime + 'ms');
    
    // Mostrar métricas de coherencia
    const metrics = optimizer.getCoherenceMetrics();
    console.log('  Frecuencia:', metrics.frequency + 'Hz');
    console.log('  Coherencia cuántica:', metrics.coherence.toFixed(4));
    
    // Verificar caché
    const cacheSize = optimizer.cache.size();
    console.log('  Elementos en caché:', cacheSize);
    
    return result;
  } catch (error) {
    console.error('❌ Error durante la prueba:', error.message);
    return false;
  }
}

testOptimizer().then(result => {
  console.log('');
  console.log('🎯 PRUEBA COMPLETADA');
  process.exit(result ? 0 : 1);
});
