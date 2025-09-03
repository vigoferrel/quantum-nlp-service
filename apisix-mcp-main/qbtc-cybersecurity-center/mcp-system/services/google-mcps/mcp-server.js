const { EventEmitter } = require('events');
const { createServer } = require('net');

class MCPServer extends EventEmitter {
    constructor() {
        super();
        this.server = createServer((socket) => {
            let buffer = '';
            
            socket.on('data', (data) => {
                buffer += data;
                
                try {
                    const messages = buffer.split('\n');
                    buffer = messages.pop();
                    
                    for (const message of messages) {
                        if (!message) continue;
                        const request = JSON.parse(message);
                        
                        this.handleRequest(request).then(response => {
                            socket.write(JSON.stringify(response) + '\n');
                        }).catch(error => {
                            socket.write(JSON.stringify({
                                error: error.message
                            }) + '\n');
                        });
                    }
                } catch (error) {
                    console.error('Error processing message:', error);
                }
            });
        });
    }

    async handleRequest(request) {
        const { type, params } = request;
        const listeners = this.listeners(type);
        
        if (listeners.length === 0) {
            throw new Error(`No handler for request type: ${type}`);
        }
        
        return await listeners[0](params);
    }

    start(port = 0) {
        return new Promise((resolve, reject) => {
            this.server.listen(port, () => {
                console.log(`MCP Server listening on port ${this.server.address().port}`);
                resolve(this.server.address().port);
            });
            
            this.server.on('error', reject);
        });
    }

    stop() {
        return new Promise((resolve, reject) => {
            this.server.close((err) => {
                if (err) reject(err);
                else resolve();
            });
        });
    }
}

module.exports = { MCPServer };
