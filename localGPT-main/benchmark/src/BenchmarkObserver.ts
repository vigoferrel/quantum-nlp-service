import { IQuantumStateObserver, QuantumEdgeFactors } from '../../src/types/IQuantumStateObserver';

export class BenchmarkObserver implements IQuantumStateObserver {
    private recordedMetrics: QuantumEdgeFactors[] = [];
    private recordedDependencies: { name: string, input: any, output: any }[] = [];

    public recordMetrics(metrics: QuantumEdgeFactors): void {
        this.recordedMetrics.push(metrics);
    }

    public recordDependency(name: string, input: any, output: any): void {
        this.recordedDependencies.push({ name, input, output });
    }

    public generateReport(totalIterations: number): string {
        if (this.recordedMetrics.length === 0) {
            return "No se registraron métricas.";
        }

        const report_parts: string[] = [];
        report_parts.push("=================================================");
        report_parts.push("=    REPORTE DE DISTRIBUCION DE REALIDAD QBTC   =");
        report_parts.push("=================================================");
        report_parts.push(`Total de Iteraciones: ${totalIterations}`);
        report_parts.push(`Iteraciones Exitosas: ${this.recordedMetrics.length}`);
        report_parts.push("\n--- Análisis Estadístico de Quantum Edge (Q_edge) ---");

        const getStats = (key: keyof QuantumEdgeFactors) => {
            const values = this.recordedMetrics.map(m => m[key]);
            const sum = values.reduce((a, b) => a + b, 0);
            const avg = sum / values.length;
            const min = Math.min(...values);
            const max = Math.max(...values);
            const stdDev = Math.sqrt(values.map(x => Math.pow(x - avg, 2)).reduce((a, b) => a + b, 0) / values.length);
            return { avg, min, max, stdDev, values };
        };

        const edgeStats = getStats('totalEdge');
        report_parts.push(`Q_edge Total   => Promedio: ${edgeStats.avg.toFixed(3)}, Desv.Std: ${edgeStats.stdDev.toFixed(3)}, Min: ${edgeStats.min.toFixed(3)}, Max: ${edgeStats.max.toFixed(3)}`);
        
        report_parts.push("\n--- Desglose de Factores Promedio ---");
        const speedupStats = getStats('speedup');
        const accuracyStats = getStats('accuracy');
        const efficiencyStats = getStats('efficiency');
        const coherenceStats = getStats('coherence');
        const entanglementStats = getStats('entanglement');

        report_parts.push(`S (Speedup)      => Promedio: ${speedupStats.avg.toFixed(3)}x`);
        report_parts.push(`A (Accuracy)     => Promedio: ${accuracyStats.avg.toFixed(3)}x`);
        report_parts.push(`E (Efficiency)   => Promedio: ${efficiencyStats.avg.toFixed(3)}x`);
        report_parts.push(`C (Coherence)    => Promedio: ${coherenceStats.avg.toFixed(3)}x`);
        report_parts.push(`T (Entanglement) => Promedio: ${entanglementStats.avg.toFixed(3)} (adaptabilidad)`);

        report_parts.push("\n--- Visualización de Tendencia (Sparkline) ---");
        report_parts.push(`Evolución de Q_edge: ${this.generateSparkline(edgeStats.values)}`);
        
        report_parts.push("\n=================================================");

        return report_parts.join('\n');
    }

    private generateSparkline(data: number[]): string {
        const ticks = [' ', '▂', '▃', '▄', '▅', '▆', '▇', '█'];
        const min = Math.min(...data);
        const max = Math.max(...data);
        if (min === max) return ticks[0].repeat(data.length);

        const range = max - min;
        const scaled = data.map(d => Math.round(((d - min) / range) * (ticks.length - 1)));

        return scaled.map(s => ticks[s]).join('');
    }
}