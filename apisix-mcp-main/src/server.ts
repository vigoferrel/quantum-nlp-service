import { apisixServer } from './quantum-apisix-vigoleonrocks-ultimate-enhanced';
import express from 'express';
import cors from 'cors';

export function createHttpServer() {
    const app = express();
    const PORT = process.env.PORT || 9080;

    app.use(cors());
    app.use(express.json());

    // Inicializar servidor APISIX
    apisixServer.initialize().then(result => {
        if (result.isSuccess()) {
            console.log('Servidor de lógica cuántica para HTTP inicializado correctamente');

            // Configurar rutas
            app.post('/qbtc/tensor-4d/calculate/:symbol', async (req, res) => {
                try {
                    const { symbol } = req.params;
                    const { dimensions } = req.body;

                    const result = await apisixServer.executeQuantumOperation('tensor4d_calculate', {
                        method: 'POST',
                        path: `/tensor-4d/calculate/${symbol}`,
                        data: { dimensions }
                    });

                    res.json(result);
                } catch (err) {
                    const error = err instanceof Error ? err : new Error('Error desconocido');
                    res.status(500).json({
                        success: false,
                        error: error.message
                    });
                }
            });

            // Iniciar servidor
            app.listen(PORT, () => {
                const diagnostics = apisixServer.getDiagnostics();
                console.log(`
    ╔══════════════════════════════════════════════════════════════╗
    ║                 QBTC APISIX HTTP-MCP SERVER                  ║
    ║                   VIGOLEONROCKS 7919 (HTTP)                  ║
    ╠══════════════════════════════════════════════════════════════╣
    ║ Servidor HTTP iniciado en puerto: ${PORT}                      ║
    ║ Coherencia cuántica: ${apisixServer.getCoherenceLevel()}    ║
    ║ Frecuencia: ${apisixServer.getFrequency()} Hz               ║
    ║ Estado: ${diagnostics.systemState.lastOperation}             ║
    ╚══════════════════════════════════════════════════════════════╝
                `);
            });

            return app; // Retornamos la app por si se necesita
        } else {
            // Acceder al error usando el método fold de QuantumTry
            const errorMsg = result.fold<string>(
                (success) => `Error inesperado en la inicialización: coherencia ${success.metrics.coherenceLevel}`,
                (error) => `Error: ${error.message}`
            );
            console.error('Error inicializando servidor:', errorMsg);
            process.exit(1);
        }
    }).catch(err => {
        const error = err instanceof Error ? err : new Error('Error fatal desconocido');
        console.error('Error fatal:', error.message);
        process.exit(1);
    });
}