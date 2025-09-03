const { google } = require('googleapis');
const { MCPServer } = require('./mcp-server');
const path = require('path');
const fs = require('fs').promises;

// Performance optimizations
const CACHE_TTL = 300; // 5 minutes
const MAX_BATCH_SIZE = 50;
const eventCache = new Map();
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
                // Store refresh token securely
                process.env.GOOGLE_REFRESH_TOKEN = tokens.refresh_token;
            }
        });

        return oauth2Client;
    } catch (error) {
        console.error('Error initializing OAuth2 client:', error);
        throw error;
    }
};

// Initialize Calendar API with connection pooling
const initializeCalendarAPI = async (auth) => {
    return google.calendar({ 
        version: 'v3', 
        auth,
        pool: {
            maxSockets: 5,
            maxFreeSockets: 2,
            keepAlive: true,
            keepAliveMsecs: 30000
        }
    });
};

// Cache management functions
const getCachedEvents = (key) => {
    const cached = eventCache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL * 1000) {
        return cached.data;
    }
    return null;
};

const cacheEvents = (key, data) => {
    eventCache.set(key, {
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
    // Process batch items
    return items;
};

// Error handling wrapper
const withErrorHandling = async (operation) => {
    try {
        return await operation();
    } catch (error) {
        console.error(`Operation failed: ${error.message}`);
        if (error.code === 401 || error.code === 403) {
            // Handle auth errors
            await refreshTokens();
        }
        throw error;
    }
};

// Initialize OAuth2 client
const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    'http://localhost'
);

// Initialize Calendar API
const calendar = google.calendar({ version: 'v3', auth: oauth2Client });

// Create MCP Server
const server = new MCPServer();

// Handle calendar events
server.on('listEvents', async (params) => {
    const { timeMin, timeMax, maxResults = 10 } = params;
    
    try {
        const response = await calendar.events.list({
            calendarId: 'primary',
            timeMin: timeMin || new Date().toISOString(),
            timeMax: timeMax,
            maxResults: maxResults,
            singleEvents: true,
            orderBy: 'startTime',
        });
        
        return response.data.items;
    } catch (error) {
        console.error('Error listing events:', error);
        throw error;
    }
});

server.on('createEvent', async (params) => {
    const { summary, description, start, end, attendees } = params;
    
    try {
        const event = {
            summary,
            description,
            start: { dateTime: start },
            end: { dateTime: end },
            attendees: attendees?.map(email => ({ email }))
        };
        
        const response = await calendar.events.insert({
            calendarId: 'primary',
            resource: event,
        });
        
        return response.data;
    } catch (error) {
        console.error('Error creating event:', error);
        throw error;
    }
});

// Start the server
server.start();
