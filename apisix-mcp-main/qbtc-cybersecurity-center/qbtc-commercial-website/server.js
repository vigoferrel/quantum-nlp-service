/**
 * QBTC Commercial Website Server
 * Servidor para sitio web comercial de servicios de ciberseguridad
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const config = {
    port: process.env.PORT || 7070,
    host: process.env.HOST || 'localhost'
};

// MIME types para servir archivos correctamente
const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

function serveFile(filePath, res) {
    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'text/plain';
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') {
                // Archivo no encontrado - servir 404
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end(`
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>404 - Página no encontrada</title>
                        <style>
                            body { 
                                font-family: Arial, sans-serif; 
                                background: #0a0a0a; 
                                color: #00ffff; 
                                text-align: center; 
                                padding: 50px; 
                            }
                            h1 { font-size: 4rem; margin-bottom: 20px; }
                            p { font-size: 1.2rem; }
                            a { color: #00ffff; text-decoration: none; }
                            a:hover { text-decoration: underline; }
                        </style>
                    </head>
                    <body>
                        <h1>404</h1>
                        <p>Página no encontrada</p>
                        <p><a href="/">Volver al inicio</a></p>
                    </body>
                    </html>
                `);
            } else {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Error interno del servidor');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(data);
        }
    });
}

function handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    let pathname = parsedUrl.pathname;
    
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // Redirigir raíz a index.html
    if (pathname === '/') {
        pathname = '/index.html';
    }
    
    // API endpoints simulados
    if (pathname.startsWith('/api/')) {
        res.setHeader('Content-Type', 'application/json');
        
        if (pathname === '/api/contact' && req.method === 'POST') {
            let body = '';
            req.on('data', chunk => { body += chunk; });
            req.on('end', () => {
                try {
                    const data = JSON.parse(body);
                    console.log('📩 Nueva consulta recibida:', data);
                    res.writeHead(200);
                    res.end(JSON.stringify({
                        success: true,
                        message: 'Consulta recibida correctamente. Nos pondremos en contacto pronto.',
                        id: Math.random().toString(36).substr(2, 9)
                    }));
                } catch (error) {
                    res.writeHead(400);
                    res.end(JSON.stringify({
                        success: false,
                        message: 'Error en los datos enviados'
                    }));
                }
            });
            return;
        }
        
        if (pathname === '/api/status') {
            res.writeHead(200);
            res.end(JSON.stringify({
                status: 'operational',
                services: {
                    enterprise: 'available',
                    government: 'available',
                    personal: 'available'
                },
                timestamp: new Date().toISOString()
            }));
            return;
        }
        
        // API no encontrada
        res.writeHead(404);
        res.end(JSON.stringify({ error: 'API endpoint no encontrado' }));
        return;
    }
    
    // Construir ruta del archivo
    const filePath = path.join(__dirname, pathname);
    
    // Verificar que el archivo está dentro del directorio del proyecto (seguridad)
    if (!filePath.startsWith(__dirname)) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Acceso denegado');
        return;
    }
    
    serveFile(filePath, res);
}

// Crear y configurar servidor
const server = http.createServer(handleRequest);

// Manejar errores del servidor
server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`❌ Puerto ${config.port} ya está en uso. Intentando con puerto alternativo...`);
        config.port = parseInt(config.port) + 1;
        setTimeout(() => {
            server.listen(config.port, config.host);
        }, 1000);
    } else {
        console.error('❌ Error del servidor:', err);
    }
});

// Iniciar servidor
server.listen(config.port, config.host, () => {
    console.log(`🌐 QBTC Commercial Website Server iniciado`);
    console.log(`🔗 URL: http://${config.host}:${config.port}`);
    console.log(`📁 Sirviendo archivos desde: ${__dirname}`);
    console.log(`📊 Endpoints disponibles:`);
    console.log(`   🏠 Inicio: http://${config.host}:${config.port}/`);
    console.log(`   🛡️ Servicios: http://${config.host}:${config.port}/pages/services.html`);
    console.log(`   📧 API Contacto: http://${config.host}:${config.port}/api/contact`);
    console.log(`   📊 API Status: http://${config.host}:${config.port}/api/status`);
    console.log(`⚡ Servidor listo para recibir consultas comerciales!`);
});

// Manejo de señales para cierre limpio
process.on('SIGINT', () => {
    console.log('\n🛑 Cerrando servidor comercial...');
    server.close(() => {
        console.log('✅ Servidor comercial cerrado correctamente');
        process.exit(0);
    });
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Cerrando servidor comercial...');
    server.close(() => {
        console.log('✅ Servidor comercial cerrado correctamente');
        process.exit(0);
    });
});

module.exports = server;
