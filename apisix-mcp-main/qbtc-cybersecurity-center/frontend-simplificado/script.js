// Constants
const API_ENDPOINTS = {
    status: '/api/status',
    security: '/api/security',
    quantum: '/api/quantum',
    modules: '/api/modules'
};

const UPDATE_INTERVAL = 5000; // Update every 5 seconds
const MAX_LOG_ENTRIES = 100;

// State Management
let systemState = {
    quantumState: {},
    securityMetrics: {},
    engineStatus: {},
    performance: {}
};

// Utility Functions
const formatTimestamp = () => {
    return new Date().toLocaleTimeString('es-ES', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
};

const addLogEntry = (message, type = 'info') => {
    const log = document.getElementById('event-log');
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.innerHTML = `[${formatTimestamp()}] ${message}`;
    log.insertBefore(entry, log.firstChild);

    // Limit log entries
    while (log.children.length > MAX_LOG_ENTRIES) {
        log.removeChild(log.lastChild);
    }
};

// API Functions
const fetchData = async (endpoint) => {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        addLogEntry(`Error al obtener datos de ${endpoint}: ${error.message}`, 'error');
        return null;
    }
};

// Update Functions
const updateQuantumState = (data) => {
    if (!data) return;
    
    document.getElementById('quantum-state').textContent = data.state;
    document.getElementById('quantum-coherence').textContent = data.coherence;
    document.getElementById('error-rate').textContent = data.errorRate;
    document.getElementById('active-qubits').textContent = data.activeQubits;

    // Update header coherence status
    const coherenceElement = document.querySelector('.coherence-value');
    coherenceElement.textContent = data.state;
    coherenceElement.style.color = data.state === 'ESTABLE' ? 'var(--success-color)' : 'var(--warning-color)';
};

const updateSecurityMetrics = (data) => {
    if (!data) return;

    document.getElementById('threats').textContent = data.threatsDetected;
    document.getElementById('blocks').textContent = data.attacksBlocked;
    document.getElementById('quantum-score').textContent = data.quantumScore;
    document.getElementById('protection-level').textContent = data.protectionLevel;

    // Add log entry for new threats
    if (data.newThreats && data.newThreats.length > 0) {
        data.newThreats.forEach(threat => {
            addLogEntry(`Nueva amenaza detectada: ${threat}`, 'warning');
        });
    }
};

const updateEngineStatus = (data) => {
    if (!data) return;

    document.getElementById('monitoring').textContent = data.monitoring;
    document.getElementById('analysis').textContent = data.analysis;
    document.getElementById('response').textContent = data.response;
    document.getElementById('simulation').textContent = data.simulation;

    // Add log entry for engine state changes
    Object.entries(data).forEach(([engine, status]) => {
        if (systemState.engineStatus[engine] && systemState.engineStatus[engine] !== status) {
            addLogEntry(`Estado del motor ${engine} cambió a: ${status}`);
        }
    });
};

const updatePerformance = (data) => {
    if (!data) return;

    document.getElementById('quantum-processing').textContent = data.processing;
    document.getElementById('qubit-fidelity').textContent = data.fidelity;
    document.getElementById('quantum-memory').textContent = data.memory;
    document.getElementById('quantum-bandwidth').textContent = data.bandwidth;
};

// Main Update Loop
const updateAll = async () => {
    const [quantumData, securityData, engineData, performanceData] = await Promise.all([
        fetchData(API_ENDPOINTS.quantum),
        fetchData(API_ENDPOINTS.security),
        fetchData(API_ENDPOINTS.modules),
        fetchData(API_ENDPOINTS.status)
    ]);

    updateQuantumState(quantumData);
    updateSecurityMetrics(securityData);
    updateEngineStatus(engineData);
    updatePerformance(performanceData);

    // Update system state
    systemState = {
        quantumState: quantumData,
        securityMetrics: securityData,
        engineStatus: engineData,
        performance: performanceData
    };
};

// Server-Sent Events Setup
const setupSSE = () => {
    const eventSource = new EventSource('/api/events');

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        addLogEntry(data.message, data.type);

        // Update relevant metrics based on event type
        if (data.updates) {
            Object.entries(data.updates).forEach(([metric, value]) => {
                const element = document.getElementById(metric);
                if (element) element.textContent = value;
            });
        }
    };

    eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        addLogEntry('Error en la conexión de eventos. Reintentando...', 'error');
        eventSource.close();
        setTimeout(setupSSE, 5000); // Retry connection after 5 seconds
    };
};

// Initialization
const init = () => {
    // Initial update
    updateAll();
    
    // Setup periodic updates
    setInterval(updateAll, UPDATE_INTERVAL);
    
    // Setup SSE
    setupSSE();
    
    // Initial log entry
    addLogEntry('Sistema de monitoreo cuántico iniciado');
};

// Start the application
document.addEventListener('DOMContentLoaded', init);
