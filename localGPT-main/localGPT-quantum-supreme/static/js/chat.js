document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');

    // Configure marked to use highlight.js
    marked.setOptions({
        highlight: function(code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
        },
        langPrefix: 'hljs language-' // For CSS classes
    });

    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        displayMessage(message, 'user');
        messageInput.value = '';
        showLoading();

        try {
            const response = await fetch('/api/quantum_query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message })
            });

            if (response.ok) {
                const data = await response.json();
                displayMessage(data.response, 'assistant');
                // Efecto Trompeta: Reaccionar a eventos de trascendencia
                if (data.event === 'TRANSCENDENCE') {
                    showNotification('🌀 ¡El sistema ha trascendido! 🌀', 'transcendence');
                    updateTranscendenceLevel(data.dna.transcendence_events);
                }
            } else {
                const errorData = await response.json();
                displayError(`Error del servidor: ${errorData.error || 'Desconocido'}`);
            }
        } catch (error) {
            displayError(`Error de conexión: ${error.message}`);
        }
    });

    function showLoading() {
        const loadingHtml = `
            <div class="message-wrapper" id="loading-indicator">
                <div class="flex items-start space-x-4 space-y-1">
                    <div class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-white font-bold text-xs">AI</div>
                    <div class="flex-1">
                        <div class="prose prose-slate max-w-none text-gray-300">
                           <p>Procesando consulta cuántica...</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', loadingHtml);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeLoading() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }

    function displayMessage(message, role) {
        removeLoading();
        const avatar = role === 'user' ? 'TÚ' : 'AI';
        const avatarBg = role === 'user' ? 'bg-indigo-600' : 'bg-gray-700';

        // Usar marked para convertir Markdown a HTML
        const formattedMessage = marked.parse(message);

        const messageHtml = `
            <div class="message-wrapper py-4">
                <div class="flex items-start space-x-4">
                    <div class="w-8 h-8 rounded-full ${avatarBg} flex items-center justify-center text-white font-bold text-xs">${avatar}</div>
                    <div class="flex-1">
                        <div class="prose prose-slate max-w-none text-gray-300">
                           ${formattedMessage}
                        </div>
                    </div>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', messageHtml);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function updateTranscendenceLevel(level) {
        const levelElement = document.getElementById('transcendence-level');
        if (levelElement) {
            levelElement.textContent = level;
        }
    }

    function displayError(message) {
        removeLoading();
        const errorHtml = `
            <div class="message-wrapper py-4">
                <div class="flex items-start space-x-4">
                    <div class="w-8 h-8 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-xs">!</div>
                    <div class="flex-1">
                        <div class="prose prose-slate max-w-none text-red-400">
                           <p><strong>Error:</strong> ${message}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', errorHtml);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
