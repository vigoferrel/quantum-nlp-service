import express from 'express';
import { json } from 'body-parser';
import { QuantumTokenizer } from './QuantumTokenizer';
import amqp from 'amqplib';

const app = express();
app.use(json());

// Initialize quantum tokenizer with default configuration
const tokenizer = new QuantumTokenizer({
    maxSequenceLength: 512,
    dimensionality: 768,  // Similar to BERT base
    quantumAmplitude: 0.5,
    consciousness: 0.8,
    entanglementThreshold: 0.3
});

// RabbitMQ connection and channel
let channel: amqp.Channel;

// Connect to RabbitMQ
async function setupRabbitMQ() {
    try {
        const connection = await amqp.connect('amqp://localhost');
        channel = await connection.createChannel();
        
        // Declare exchanges and queues
        await channel.assertExchange('quantum.nlp', 'topic', { durable: true });
        await channel.assertQueue('quantum.nlp.tokens', { durable: true });
        await channel.assertQueue('quantum.nlp.embeddings', { durable: true });
        
        // Bind queues to exchange
        await channel.bindQueue('quantum.nlp.tokens', 'quantum.nlp', 'tokens.*');
        await channel.bindQueue('quantum.nlp.embeddings', 'quantum.nlp', 'embeddings.*');
        
        console.log('✅ Connected to RabbitMQ');
    } catch (error) {
        console.error('Failed to connect to RabbitMQ:', error);
        process.exit(1);
    }
}

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'quantum-nlp' });
});

// Tokenization endpoint
app.post('/tokenize', async (req, res) => {
    try {
        const { text } = req.body;
        
        if (!text || typeof text !== 'string') {
            return res.status(400).json({
                error: 'Invalid input: text field is required and must be a string'
            });
        }

        const result = await tokenizer.tokenize(text);
        
        if (result.success) {
            // Publish result to RabbitMQ
            channel.publish('quantum.nlp', 'tokens.created', 
                Buffer.from(JSON.stringify(result.data)));
            
            res.json({ tokens: result.data });
        } else {
            res.status(500).json({ error: result.error });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Embedding generation endpoint
app.post('/embeddings', async (req, res) => {
    try {
        const { tokens } = req.body;
        
        if (!Array.isArray(tokens) || !tokens.every(t => typeof t === 'string')) {
            return res.status(400).json({
                error: 'Invalid input: tokens must be an array of strings'
            });
        }

        const result = await tokenizer.generateEmbeddings(tokens);
        
        if (result.success) {
            // Publish result to RabbitMQ
            channel.publish('quantum.nlp', 'embeddings.created', 
                Buffer.from(JSON.stringify(result.data)));
            
            res.json({ embeddings: result.data });
        } else {
            res.status(500).json({ error: result.error });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Start the service
const PORT = process.env.PORT || 3000;

async function startService() {
    await setupRabbitMQ();
    app.listen(PORT, () => {
        console.log(`✅ Quantum NLP Service running on port ${PORT}`);
    });
}

startService().catch(error => {
    console.error('Failed to start service:', error);
    process.exit(1);
});
