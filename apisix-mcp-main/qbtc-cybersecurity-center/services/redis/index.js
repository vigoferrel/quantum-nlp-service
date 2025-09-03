// Redis Service Configuration and Setup
const Redis = require('ioredis');
const config = require('../../config/redis.config');

class RedisService {
    constructor() {
        this.client = new Redis(config);
        this.setupEventHandlers();
    }

    setupEventHandlers() {
        this.client.on('error', (err) => console.error('Redis Error:', err));
        this.client.on('connect', () => console.log('Redis Connected'));
    }
}

module.exports = new RedisService();
