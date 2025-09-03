const { google } = require('googleapis');
const { MCPServer } = require('./mcp-server');
const path = require('path');
const fs = require('fs').promises;

// Performance optimizations
const CACHE_TTL = 300; // 5 minutes
const MAX_BATCH_SIZE = 25;
const MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024; // 10MB
const messageCache = new Map();
const pendingBatches = new Map();

// Initialize OAuth2 client with error handling
const initializeOAuth2Client = async () => {
    try {
        const credentials = JSON.parse(
            await fs.readFile(process.env.GOOGLE_CREDENTIALS_PATH)
        );

        const oauth2Client = new google.auth.OAuth2(
            credentials.installed.client_id,
            credentials.installed.client_secret,
            credentials.installed.redirect_uris[0]
        );

        // Add token refresh handling
        oauth2Client.on('tokens', (tokens) => {
            if (tokens.refresh_token) {
                process.env.GOOGLE_REFRESH_TOKEN = tokens.refresh_token;
            }
        });

        return oauth2Client;
    } catch (error) {
        console.error('Error initializing OAuth2 client:', error);
        throw error;
    }
};

// Initialize Gmail API with connection pooling
const initializeGmailAPI = async (auth) => {
    return google.gmail({ 
        version: 'v1', 
        auth,
        pool: {
            maxSockets: 5,
            maxFreeSockets: 2,
            keepAlive: true,
            keepAliveMsecs: 30000
        }
    });
};

// Cache management
const getCachedMessages = (key) => {
    const cached = messageCache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL * 1000) {
        return cached.data;
    }
    return null;
};

const cacheMessages = (key, data) => {
    messageCache.set(key, {
        data,
        timestamp: Date.now()
    });
};

// Batch processing
const addToBatch = (batchKey, item) => {
    if (!pendingBatches.has(batchKey)) {
        pendingBatches.set(batchKey, []);
    }
    pendingBatches.get(batchKey).push(item);

    if (pendingBatches.get(batchKey).length >= MAX_BATCH_SIZE) {
        return processBatch(batchKey);
    }
    return null;
};

const processBatch = async (batchKey) => {
    const items = pendingBatches.get(batchKey);
    pendingBatches.delete(batchKey);
    return items;
};

// Error handling wrapper
const withErrorHandling = async (operation) => {
    try {
        return await operation();
    } catch (error) {
        console.error(`Operation failed: ${error.message}`);
        if (error.code === 401 || error.code === 403) {
            await refreshTokens();
        }
        throw error;
    }
};

// Message processing utilities
const encodeMessage = (message) => {
    const encodedMessage = Buffer.from(message)
        .toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
    return encodedMessage;
};

const createMessage = ({ to, subject, body, attachments }) => {
    const messageParts = [
        'MIME-Version: 1.0',
        'Content-Type: multipart/mixed; boundary="boundary"',
        '',
        '--boundary',
        'Content-Type: text/plain; charset="UTF-8"',
        `To: ${to}`,
        `Subject: ${subject}`,
        '',
        body
    ];

    if (attachments?.length) {
        attachments.forEach(({ filename, content, mimeType }) => {
            if (Buffer.byteLength(content) <= MAX_ATTACHMENT_SIZE) {
                messageParts.push(
                    '--boundary',
                    `Content-Type: ${mimeType}`,
                    'Content-Transfer-Encoding: base64',
                    `Content-Disposition: attachment; filename="${filename}"`,
                    '',
                    content.toString('base64')
                );
            }
        });
    }

    messageParts.push('--boundary--');
    return messageParts.join('\n');
};

// Initialize OAuth2 client
const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    'http://localhost'
);

// Initialize Gmail API
const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

// Create MCP Server
const server = new MCPServer();

// Handle Gmail operations
server.on('listMessages', async (params) => {
    const { maxResults = 10, query } = params;
    
    try {
        const response = await gmail.users.messages.list({
            userId: 'me',
            maxResults: maxResults,
            q: query
        });
        
        const messages = await Promise.all(
            response.data.messages.map(async (msg) => {
                const fullMsg = await gmail.users.messages.get({
                    userId: 'me',
                    id: msg.id
                });
                return fullMsg.data;
            })
        );
        
        return messages;
    } catch (error) {
        console.error('Error listing messages:', error);
        throw error;
    }
});

server.on('sendMessage', async (params) => {
    const { to, subject, body } = params;
    
    try {
        const email = [
            'Content-Type: text/plain; charset="UTF-8"',
            'MIME-Version: 1.0',
            `To: ${to}`,
            `Subject: ${subject}`,
            '',
            body
        ].join('\n');

        const encodedMessage = Buffer.from(email).toString('base64')
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=+$/, '');

        const response = await gmail.users.messages.send({
            userId: 'me',
            requestBody: {
                raw: encodedMessage
            }
        });
        
        return response.data;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
});

// Start the server
server.start();
