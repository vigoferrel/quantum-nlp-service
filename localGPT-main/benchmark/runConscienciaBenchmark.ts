import { QuantumConscienciaFinanciera } from '../src/quantum-consciousness/QuantumConscienciaFinanciera';
import { BenchmarkObserver } from './src/BenchmarkObserver';

const NUM_ITERATIONS = 100;

async function runBenchmark() {
  console.log('Iniciando Framework de Observabilidad Cuántica...');
  console.log(`Número de iteraciones de prueba: ${NUM_ITERATIONS}`);
  
  const observer = new BenchmarkObserver();
  const consciencia = new QuantumConscienciaFinanciera(observer);
  
  console.time('Tiempo total del Benchmark');
  for (let i = 0; i < NUM_ITERATIONS; i++) {
    process.stdout.write(`\rEjecutando iteración ${i + 1}/${NUM_ITERATIONS}...`);
    await consciencia.calculateExtremeMomentum('BTCUSDT');
  }
  console.timeEnd('Tiempo total del Benchmark');
  
  console.log('\n\n' + observer.generateReport(NUM_ITERATIONS));
}

runBenchmark().catch(error => {
  console.error('El benchmark ha fallado:', error);
  process.exit(1);
});