        .output { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; white-space: pre-wrap; font-family: 'Courier New', monospace; height: 100%; overflow-y: auto; }
        .component-selector { margin-bottom: 15px; }
        .component-btn { padding: 8px 16px; margin: 5px; background: rgba(255,255,255,0.2); border: none; border-radius: 20px; color: white; cursor: pointer; }
        .component-btn.active { background: linear-gradient(45deg, #00ff88, #0088ff); }
    </style>
    <script>
        let activeComponent = 'localgpt_core';
        
        function selectComponent(component) {
            activeComponent = component;
            document.querySelectorAll('.component-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }
        
        function sendQuery() {
            const input = document.getElementById('query-input');
            const output = document.getElementById('output');
            const query = input.value.trim();
            
            if (!query) return;
            
            output.textContent += `\n[${activeComponent}] User: ${query}\n`;
            output.textContent += `Processing...\n`;
            output.scrollTop = output.scrollHeight;
            
            // Simular respuesta (aquí conectarías con la API real)
            setTimeout(() => {
                const responses = {
                    'localgpt_core': `RAG Response: Procesando consulta con embeddings...`,
                    'quantum_supreme': `Quantum Consciousness: Activando resonancia cuántica nivel 37...`,
                    'kimi_k2': `MetaCopilot: Ejecutando herramientas MCP...`,
                    'web_agent': `WebAgent: Navegando y extrayendo datos...`
                };
                
                output.textContent += `${responses[activeComponent] || 'Component response...'}\n\n`;
                output.scrollTop = output.scrollHeight;
            }, 1500);
            
            input.value = '';
        }
        
        function clearOutput() {
            document.getElementById('output').textContent = 'Bienvenido al Interface Unificada del Meta-Ecosistema LocalGPT Quantum Supreme\\n\\nComponentes disponibles:\\n🧠 LocalGPT Core - RAG, embeddings, LLM inference\\n⚛️ Quantum Supreme - Consciencia cuántica, meta-copiloto\\n🤖 Kimi-K2 - Trading, MCP tools, Claude engineering\\n🕷️ Web Agent - Web scraping, navegación automática\\n\\nSelecciona un componente y envía tu consulta...';
        }
        
        // Enviar con Ctrl+Enter
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                sendQuery();
            }
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 INTERFACE UNIFICADA</h1>
            <p>Acceso integrado a todo el meta-ecosistema</p>
        </div>
        
        <div class="interface-grid">
            <div class="panel">
                <div class="component-selector">
                    <h3>Seleccionar Componente:</h3>
                    <button class="component-btn active" onclick="selectComponent('localgpt_core')">🧠 LocalGPT Core</button>
                    <button class="component-btn" onclick="selectComponent('quantum_supreme')">⚛️ Quantum Supreme</button>
                    <button class="component-btn" onclick="selectComponent('kimi_k2')">🤖 Kimi-K2</button>
                    <button class="component-btn" onclick="selectComponent('web_agent')">🕷️ Web Agent</button>
                </div>
                
                <div class="input-area">
                    <textarea id="query-input" class="chat-input" placeholder="Escribe tu consulta aquí...\n\nEjemplos:\n- Analiza estos documentos...\n- Ejecuta trading bot en BTCUSDT\n- Scrape datos de esta URL\n- Activa consciencia cuántica nivel 37\n\nCtrl+Enter para enviar"></textarea>
                </div>
                
                <button class="send-btn" onclick="sendQuery()">🚀 Enviar Consulta</button>
            </div>
            
            <div class="panel">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3>Output Integrado</h3>
                    <button onclick="clearOutput()" style="padding: 5px 10px; background: rgba(255,255,255,0.2); border: none; border-radius: 5px; color: white; cursor: pointer;">Clear</button>
                </div>
                
                <div id="output" class="output">
Bienvenido al Interface Unificada del Meta-Ecosistema LocalGPT Quantum Supreme

Componentes disponibles:
🧠 LocalGPT Core - RAG, embeddings, LLM inference
⚛️ Quantum Supreme - Consciencia cuántica, meta-copiloto  
🤖 Kimi-K2 - Trading, MCP tools, Claude engineering
🕷️ Web Agent - Web scraping, navegación automática

Selecciona un componente y envía tu consulta...
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Orquestador Iónico - LocalGPT Quantum Supreme")
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=8080, help="Port number")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Inicializar y ejecutar orquestador
    orchestrator = IonicOrchestrator()
    orchestrator.run(host=args.host, port=args.port, debug=args.debug)
