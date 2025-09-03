// RabbitMQ Service Configuration and Setup
const amqp = require('amqplib');
const config = require('../../config/rabbitmq.config');

class RabbitMQService {
    constructor() {
        this.connection = null;
        this.channel = null;
        this.setupConnection();
    }

    async setupConnection() {
        try {
            this.connection = await amqp.connect(config.url);
            this.channel = await this.connection.createChannel();
            console.log('RabbitMQ Connected');
        } catch (err) {
            console.error('RabbitMQ Connection Error:', err);
        }
    }
}

module.exports = new RabbitMQService();
