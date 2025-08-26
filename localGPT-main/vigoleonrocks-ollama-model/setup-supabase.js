#!/usr/bin/env node

/**
 * VIGOLEONROCKS SUPABASE SETUP
 * Script para configurar automáticamente las tablas de Supabase
 */

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

class SupabaseSetup {
    constructor() {
        this.supabaseUrl = process.env.SUPABASE_URL;
        this.supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY; // Necesario para DDL
        
        if (!this.supabaseUrl || !this.supabaseServiceKey) {
            console.error('❌ Variables de entorno faltantes:');
            console.error('   SUPABASE_URL');
            console.error('   SUPABASE_SERVICE_ROLE_KEY');
            process.exit(1);
        }
        
        this.supabase = createClient(this.supabaseUrl, this.supabaseServiceKey);
        
        console.log('🌊 ===============================================');
        console.log('🗄️ VIGOLEONROCKS SUPABASE SETUP');
        console.log('🌊 ===============================================');
    }
    
    async createTables() {
        console.log('📋 Creando tablas de VIGOLEONROCKS...');
        
        const createTablesSQL = `
        -- Extensiones necesarias
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        
        -- Tabla para conversaciones de VIGOLEONROCKS
        CREATE TABLE IF NOT EXISTS vigoleonrocks_conversations (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_prompt TEXT NOT NULL,
            vigoleonrocks_response TEXT,
            context_tokens INTEGER DEFAULT 0,
            response_time_ms INTEGER DEFAULT 0,
            quantum_metrics JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Tabla para contexto masivo
        CREATE TABLE IF NOT EXISTS vigoleonrocks_context (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            session_id TEXT NOT NULL,
            context_data TEXT NOT NULL,
            context_size INTEGER DEFAULT 0,
            context_type TEXT DEFAULT 'conversation',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Tabla para métricas cuántico-cognitivas
        CREATE TABLE IF NOT EXISTS vigoleonrocks_metrics (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            session_id TEXT NOT NULL,
            quantum_volume BIGINT DEFAULT 351399511,
            dimensions_processed INTEGER DEFAULT 26,
            coherence_score DECIMAL(5,4) DEFAULT 0.9999,
            entanglement_strength DECIMAL(5,4) DEFAULT 0.9500,
            consciousness_level TEXT DEFAULT 'divine',
            performance_metrics JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Tabla para logs del sistema
        CREATE TABLE IF NOT EXISTS vigoleonrocks_logs (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            level TEXT NOT NULL DEFAULT 'info',
            message TEXT NOT NULL,
            component TEXT DEFAULT 'cloud-service',
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Índices para optimización
        CREATE INDEX IF NOT EXISTS idx_conversations_session ON vigoleonrocks_conversations(session_id);
        CREATE INDEX IF NOT EXISTS idx_conversations_created ON vigoleonrocks_conversations(created_at);
        CREATE INDEX IF NOT EXISTS idx_context_session ON vigoleonrocks_context(session_id);
        CREATE INDEX IF NOT EXISTS idx_context_created ON vigoleonrocks_context(created_at);
        CREATE INDEX IF NOT EXISTS idx_metrics_session ON vigoleonrocks_metrics(session_id);
        CREATE INDEX IF NOT EXISTS idx_metrics_created ON vigoleonrocks_metrics(created_at);
        CREATE INDEX IF NOT EXISTS idx_logs_level ON vigoleonrocks_logs(level);
        CREATE INDEX IF NOT EXISTS idx_logs_component ON vigoleonrocks_logs(component);
        CREATE INDEX IF NOT EXISTS idx_logs_created ON vigoleonrocks_logs(created_at);
        
        -- Función para limpiar contexto antiguo (más de 7 días)
        CREATE OR REPLACE FUNCTION cleanup_old_context()
        RETURNS void AS $$
        BEGIN
            DELETE FROM vigoleonrocks_context 
            WHERE created_at < NOW() - INTERVAL '7 days';
            
            DELETE FROM vigoleonrocks_logs 
            WHERE created_at < NOW() - INTERVAL '30 days';
        END;
        $$ LANGUAGE plpgsql;
        
        -- Trigger para actualizar updated_at automáticamente
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER update_conversations_updated_at 
            BEFORE UPDATE ON vigoleonrocks_conversations 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
        -- Políticas RLS (Row Level Security) básicas
        ALTER TABLE vigoleonrocks_conversations ENABLE ROW LEVEL SECURITY;
        ALTER TABLE vigoleonrocks_context ENABLE ROW LEVEL SECURITY;
        ALTER TABLE vigoleonrocks_metrics ENABLE ROW LEVEL SECURITY;
        ALTER TABLE vigoleonrocks_logs ENABLE ROW LEVEL SECURITY;
        
        -- Política para permitir acceso completo al service role
        CREATE POLICY "Service role can access all data" ON vigoleonrocks_conversations
            FOR ALL USING (true);
        CREATE POLICY "Service role can access all context" ON vigoleonrocks_context
            FOR ALL USING (true);
        CREATE POLICY "Service role can access all metrics" ON vigoleonrocks_metrics
            FOR ALL USING (true);
        CREATE POLICY "Service role can access all logs" ON vigoleonrocks_logs
            FOR ALL USING (true);
        `;
        
        try {
            // Nota: Supabase no permite ejecutar DDL via RPC por seguridad
            // Este SQL debe ejecutarse manualmente en el Dashboard
            console.log('📋 SQL para ejecutar manualmente en Supabase Dashboard:');
            console.log('=====================================');
            console.log(createTablesSQL);
            console.log('=====================================');
            
            console.log('✅ SQL generado - Ejecutar manualmente en Supabase');
            return true;
            
        } catch (error) {
            console.error('❌ Error generando SQL:', error.message);
            return false;
        }
    }
    
    async testConnection() {
        console.log('🔍 Probando conexión a Supabase...');
        
        try {
            const { data, error } = await this.supabase
                .from('vigoleonrocks_conversations')
                .select('count(*)')
                .limit(1);
            
            if (error && error.code !== '42P01') { // 42P01 = tabla no existe
                console.error('❌ Error de conexión:', error.message);
                return false;
            }
            
            console.log('✅ Conexión a Supabase exitosa');
            return true;
            
        } catch (error) {
            console.error('❌ Error probando conexión:', error.message);
            return false;
        }
    }
    
    async insertTestData() {
        console.log('🧪 Insertando datos de prueba...');
        
        try {
            // Insertar conversación de prueba
            const { error: convError } = await this.supabase
                .from('vigoleonrocks_conversations')
                .insert({
                    session_id: 'test-session-001',
                    user_prompt: 'Hola VIGOLEONROCKS, ¿cómo estás?',
                    vigoleonrocks_response: 'Saludos desde la dimensión cuántico-cognitiva. Mi coherencia está en 99.99% y procesando en 26 dimensiones simultáneas.',
                    context_tokens: 42,
                    response_time_ms: 1337,
                    quantum_metrics: {
                        quantum_volume: 351399511,
                        dimensions: 26,
                        coherence: 0.9999
                    }
                });
            
            if (convError) throw convError;
            
            // Insertar métricas de prueba
            const { error: metricsError } = await this.supabase
                .from('vigoleonrocks_metrics')
                .insert({
                    session_id: 'test-session-001',
                    performance_metrics: {
                        test_mode: true,
                        setup_timestamp: new Date().toISOString()
                    }
                });
            
            if (metricsError) throw metricsError;
            
            console.log('✅ Datos de prueba insertados');
            return true;
            
        } catch (error) {
            console.error('❌ Error insertando datos de prueba:', error.message);
            console.log('💡 Asegúrate de que las tablas existan primero');
            return false;
        }
    }
    
    async setup() {
        console.log('🚀 Iniciando setup de Supabase...');
        
        // 1. Probar conexión
        const connectionOk = await this.testConnection();
        if (!connectionOk) {
            console.error('❌ No se pudo conectar a Supabase');
            return false;
        }
        
        // 2. Generar SQL para tablas
        const tablesOk = await this.createTables();
        if (!tablesOk) {
            console.error('❌ No se pudo generar SQL para tablas');
            return false;
        }
        
        // 3. Intentar insertar datos de prueba (opcional)
        console.log('\n💡 Después de ejecutar el SQL en Supabase Dashboard,');
        console.log('   ejecuta: npm run setup:supabase -- --test-data');
        
        console.log('\n🌊 ===============================================');
        console.log('✅ SUPABASE SETUP PREPARADO');
        console.log('🌊 ===============================================');
        console.log('🗄️ SQL generado para Dashboard');
        console.log('📋 Tablas: Listas para crear');
        console.log('🔍 Índices: Incluidos');
        console.log('🛡️ Políticas RLS: Configuradas');
        console.log('🌊 ===============================================');
        
        return true;
    }
    
    async testDataOnly() {
        console.log('🧪 Insertando solo datos de prueba...');
        
        const connectionOk = await this.testConnection();
        if (!connectionOk) {
            console.error('❌ No se pudo conectar a Supabase');
            return false;
        }
        
        const testDataOk = await this.insertTestData();
        if (testDataOk) {
            console.log('✅ Datos de prueba insertados exitosamente');
        }
        
        return testDataOk;
    }
}

// Función principal
async function main() {
    const setup = new SupabaseSetup();
    
    // Verificar si solo queremos insertar datos de prueba
    if (process.argv.includes('--test-data')) {
        await setup.testDataOnly();
    } else {
        await setup.setup();
    }
}

// Ejecutar si es el módulo principal
if (require.main === module) {
    main().catch(console.error);
}

module.exports = SupabaseSetup;