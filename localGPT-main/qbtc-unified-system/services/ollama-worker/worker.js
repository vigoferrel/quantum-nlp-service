// worker.js - Servicio para consumir tareas de RabbitMQ y llamar a Ollama

const amqp = require('amqplib');
const fetch = require('node-fetch');

// --- Configuración ---
const RABBITMQ_URL = process.env.RABBITMQ_URL || 'amqp://guest:guest@localhost';
const OLLAMA_API_URL = process.env.OLLAMA_API_URL || 'http://localhost:11434/api/generate';
const INFERENCE_QUEUE = 'ollama_inference_queue';
const RESULTS_QUEUE = 'ollama_results_queue';


// --- Lógica del Worker ---

/**
 * Llama a la API de Ollama para ejecutar la inferencia y publica el resultado.
 * @param {object} task - La tarea que contiene el prompt y el perfil.
 * @param {object} channel - El canal de RabbitMQ.
 */
async function executeOllamaInference(task, channel) {
    console.log(`[${task.task_id}] Ejecutando inferencia para el modelo: ${task.profile.model}`);

    const body = {
        model: task.profile.model,
        prompt: task.prompt,
        stream: false,
        options: {
            temperature: task.profile.temperature,
            top_k: task.profile.top_k,
            top_p: task.profile.top_p,
        },
    };

    let outcome = null;
    let success = false;

    try {
        const response = await fetch(OLLAMA_API_URL, {
            method: 'POST',
            body: JSON.stringify(body),
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`La API de Ollama respondió con el estado ${response.status}: ${errorBody}`);
        }

        const result = await response.json();
        outcome = result.response;
        success = true;
        console.log(`[${task.task_id}] Respuesta de Ollama recibida:`, outcome.substring(0, 200), '...');

    } catch (error) {
        console.error(`[${task.task_id}] Error durante la llamada a Ollama:`, error);
        outcome = error.toString();
    }

    // Publicar el resultado en la cola de resultados
    const resultPayload = {
        ...task,
        outcome: outcome,
        success: success,
        processed_at: new Date().toISOString()
    };

    channel.sendToQueue(RESULTS_QUEUE, Buffer.from(JSON.stringify(resultPayload)), { persistent: true });
    console.log(`[${task.task_id}] Resultado enviado a la cola '${RESULTS_QUEUE}'.`)
}

/**
 * Inicia el worker, se conecta a RabbitMQ y consume mensajes.
 */
async function startWorker() {
    console.log('Iniciando el worker de Ollama...');
    let connection;
    try {
        connection = await amqp.connect(RABBITMQ_URL);
        const channel = await connection.createChannel();

        // Asegurarse de que ambas colas existen
        await channel.assertQueue(INFERENCE_QUEUE, { durable: true });
        await channel.assertQueue(RESULTS_QUEUE, { durable: true });

        console.log(`[*] Esperando mensajes en la cola '${INFERENCE_QUEUE}'. Para salir, presiona CTRL+C`);

        channel.consume(INFERENCE_QUEUE, async (msg) => {
            if (msg !== null) {
                try {
                    const task = JSON.parse(msg.content.toString());
                    console.log(`[${task.task_id}] Tarea de inferencia recibida.`);
                    await executeOllamaInference(task, channel); // Pasar el canal
                    channel.ack(msg); // Confirma que el mensaje fue procesado
                } catch (error) {
                    console.error('Error procesando el mensaje:', error);
                    channel.nack(msg, false, false);
                }
            }
        });
    } catch (error) {
        console.error('Error fatal del worker, reintentando en 10 segundos:', error);
        setTimeout(startWorker, 10000); // Reintento de conexión
    }
}

startWorker();
