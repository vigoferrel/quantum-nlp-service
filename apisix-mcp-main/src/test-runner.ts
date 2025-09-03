console.log('[TEST RUNNER] Script iniciado.');

try {
    console.log('[TEST RUNNER] Intentando importar QuantumApisixMCPFinal...');
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const { QuantumApisixMCPFinal } = require('./quantum-apisix-vigoleonrocks-final');
    console.log('[TEST RUNNER] Importación exitosa.');

    console.log('[TEST RUNNER] Instanciando el servidor...');
    const quantumServer = new QuantumApisixMCPFinal();
    console.log('[TEST RUNNER] Instanciación exitosa.');

    console.log('[TEST RUNNER] Llamando al método start()...');
    quantumServer.start();
    console.log('[TEST RUNNER] El método start() fue llamado. El servidor debería estar escuchando.');

} catch (error) {
    console.error('[TEST RUNNER] Se capturó un error catastrófico:');
    console.error(error);
    process.exit(1);
}