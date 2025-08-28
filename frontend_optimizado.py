#!/usr/bin/env python3
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Sistema Optimizado</title></head>
<body>
    <h1>🚀 Sistema Optimizado</h1>
    <div id="status">Estado: Conectando...</div>
    <div id="chatBox" style="border:1px solid #ccc;height:300px;overflow-y:scroll;padding:10px;"></div>
    <input type="text" id="messageInput" placeholder="Escribe tu mensaje...">
    <button onclick="sendMessage()">Enviar</button>
    
    <script>
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value;
            if (!message) return;
            
            addMessage('Usuario: ' + message, 'user');
            input.value = '';
            
            try {
                const response = await fetch('http://localhost:5004/api/process_text', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: message, session_id: 'session_' + Date.now()})
                });
                
                const data = await response.json();
                addMessage('Sistema: ' + data.response, 'system');
                
                if (data.nlp_analysis) {
                    addMessage('NLP: ' + JSON.stringify(data.nlp_analysis, null, 2), 'analysis');
                }
                
                document.getElementById('status').innerHTML = 'Estado: Conectado (Tiempo: ' + data.processing_time.toFixed(3) + 's)';
                
            } catch (error) {
                addMessage('Error: ' + error.message, 'error');
                document.getElementById('status').innerHTML = 'Estado: Error de conexión';
            }
        }
        
        function addMessage(text, type) {
            const chatBox = document.getElementById('chatBox');
            const div = document.createElement('div');
            div.style.marginBottom = '10px';
            div.style.padding = '5px';
            
            if (type === 'user') div.style.backgroundColor = '#e3f2fd';
            else if (type === 'system') div.style.backgroundColor = '#f3e5f5';
            else if (type === 'analysis') {div.style.backgroundColor = '#e8f5e8'; div.style.fontSize = '12px';}
            else if (type === 'error') {div.style.backgroundColor = '#ffebee'; div.style.color = 'red';}
            
            div.textContent = text;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        window.onload = async function() {
            try {
                const response = await fetch('http://localhost:5004/health');
                const data = await response.json();
                document.getElementById('status').innerHTML = 'Estado: Conectado - ' + data.status;
            } catch (error) {
                document.getElementById('status').innerHTML = 'Estado: No conectado';
            }
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🌐 Iniciando Frontend Optimizado en puerto 5003...")
    app.run(host='0.0.0.0', port=5003, debug=False)
