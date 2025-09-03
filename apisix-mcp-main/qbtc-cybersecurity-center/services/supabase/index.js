// Supabase Service Configuration and Setup
const { createClient } = require('@supabase/supabase-js');
const config = require('../../config/supabase.config');

class SupabaseService {
    constructor() {
        this.client = createClient(config.url, config.key);
    }

    async healthCheck() {
        try {
            const { data, error } = await this.client.from('health').select('*').limit(1);
            return !error;
        } catch (err) {
            console.error('Supabase Health Check Error:', err);
            return false;
        }
    }
}

module.exports = new SupabaseService();
