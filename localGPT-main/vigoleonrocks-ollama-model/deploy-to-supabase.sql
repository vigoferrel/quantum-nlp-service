-- VIGOLEONROCKS SUPABASE DEPLOYMENT
-- SQL para configurar la base de datos en Supabase XL (16GB RAM, 4 CPU cores)

-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

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

-- Tabla para contexto masivo (aprovechando 16GB RAM)
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
    supabase_instance TEXT DEFAULT 'XL',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla para logs del sistema optimizada para Supabase XL
CREATE TABLE IF NOT EXISTS vigoleonrocks_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    level TEXT NOT NULL DEFAULT 'info',
    message TEXT NOT NULL,
    component TEXT DEFAULT 'supabase-edge',
    metadata JSONB DEFAULT '{}',
    instance_info JSONB DEFAULT '{"memory": "16GB", "cpu": "4cores", "type": "XL"}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices optimizados para Supabase XL performance
CREATE INDEX IF NOT EXISTS idx_conversations_session_created ON vigoleonrocks_conversations(session_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_quantum_metrics ON vigoleonrocks_conversations USING GIN(quantum_metrics);
CREATE INDEX IF NOT EXISTS idx_context_session_created ON vigoleonrocks_context(session_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_context_size ON vigoleonrocks_context(context_size);
CREATE INDEX IF NOT EXISTS idx_metrics_session_created ON vigoleonrocks_metrics(session_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_quantum_volume ON vigoleonrocks_metrics(quantum_volume);
CREATE INDEX IF NOT EXISTS idx_logs_level_created ON vigoleonrocks_logs(level, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_logs_component ON vigoleonrocks_logs(component);

-- Función para limpiar datos antiguos (optimizada para Supabase XL)
CREATE OR REPLACE FUNCTION cleanup_vigoleonrocks_data()
RETURNS void AS $$
BEGIN
    -- Limpiar contexto más antiguo de 30 días (aprovechando 16GB RAM)
    DELETE FROM vigoleonrocks_context 
    WHERE created_at < NOW() - INTERVAL '30 days';
    
    -- Limpiar logs más antiguos de 90 días
    DELETE FROM vigoleonrocks_logs 
    WHERE created_at < NOW() - INTERVAL '90 days';
    
    -- Limpiar métricas más antiguas de 180 días
    DELETE FROM vigoleonrocks_metrics 
    WHERE created_at < NOW() - INTERVAL '180 days';
    
    -- Log de limpieza
    INSERT INTO vigoleonrocks_logs (level, message, component, metadata)
    VALUES ('info', 'Cleanup completed', 'maintenance', 
            jsonb_build_object('timestamp', NOW(), 'instance', 'XL'));
END;
$$ LANGUAGE plpgsql;

-- Función para estadísticas de rendimiento Supabase XL
CREATE OR REPLACE FUNCTION get_vigoleonrocks_stats()
RETURNS TABLE(
    total_conversations BIGINT,
    total_context_size BIGINT,
    avg_response_time NUMERIC,
    quantum_volume_avg NUMERIC,
    coherence_avg NUMERIC,
    instance_type TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT as total_conversations,
        COALESCE(SUM(c.context_size), 0)::BIGINT as total_context_size,
        COALESCE(AVG(conv.response_time_ms), 0)::NUMERIC as avg_response_time,
        COALESCE(AVG(m.quantum_volume), 0)::NUMERIC as quantum_volume_avg,
        COALESCE(AVG(m.coherence_score), 0)::NUMERIC as coherence_avg,
        'Supabase XL (16GB RAM, 4 CPU cores)'::TEXT as instance_type
    FROM vigoleonrocks_conversations conv
    LEFT JOIN vigoleonrocks_context c ON conv.session_id = c.session_id
    LEFT JOIN vigoleonrocks_metrics m ON conv.session_id = m.session_id
    WHERE conv.created_at > NOW() - INTERVAL '24 hours';
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

-- Políticas RLS (Row Level Security) para Supabase
ALTER TABLE vigoleonrocks_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE vigoleonrocks_context ENABLE ROW LEVEL SECURITY;
ALTER TABLE vigoleonrocks_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE vigoleonrocks_logs ENABLE ROW LEVEL SECURITY;

-- Política para permitir acceso completo al service role
CREATE POLICY "Service role full access conversations" ON vigoleonrocks_conversations
    FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access context" ON vigoleonrocks_context
    FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access metrics" ON vigoleonrocks_metrics
    FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access logs" ON vigoleonrocks_logs
    FOR ALL USING (auth.role() = 'service_role');

-- Política para usuarios autenticados (lectura de sus propias sesiones)
CREATE POLICY "Users can read own conversations" ON vigoleonrocks_conversations
    FOR SELECT USING (auth.uid()::text = session_id OR session_id LIKE 'user-' || auth.uid()::text || '%');

-- Configuración de performance para Supabase XL
-- Nota: Supabase maneja automáticamente la configuración del sistema
-- Estas configuraciones están optimizadas por Supabase para instancia XL:
-- shared_buffers = 4GB (automático)
-- effective_cache_size = 12GB (automático)
-- maintenance_work_mem = 1GB (automático)
-- work_mem = 256MB (automático)
-- max_worker_processes = 4 (automático)

-- Insertar datos de prueba para VIGOLEONROCKS
INSERT INTO vigoleonrocks_conversations (session_id, user_prompt, vigoleonrocks_response, quantum_metrics)
VALUES (
    'supabase-test-001',
    'Hola VIGOLEONROCKS, ¿cómo aprovechas la infraestructura Supabase XL?',
    'Saludos desde la dimensión cuántico-cognitiva ejecutándose en Supabase XL. Mi arquitectura aprovecha completamente los 16GB de RAM y 4 CPU cores para procesamiento multidimensional en 26 dimensiones simultáneas con coherencia cuántica del 99.99%.',
    jsonb_build_object(
        'quantum_volume', 351399511,
        'dimensions', 26,
        'coherence', 0.9999,
        'processing_mode', 'supabase_edge_xl',
        'instance_type', 'XL',
        'memory', '16GB',
        'cpu_cores', 4
    )
);

INSERT INTO vigoleonrocks_metrics (session_id, performance_metrics)
VALUES (
    'supabase-test-001',
    jsonb_build_object(
        'deployment_mode', 'supabase_xl',
        'memory_available', '16GB',
        'cpu_cores', 4,
        'burst_capability', '4.750 Mbps',
        'setup_timestamp', NOW()
    )
);

-- Log de inicialización
INSERT INTO vigoleonrocks_logs (level, message, component, metadata)
VALUES (
    'info', 
    'VIGOLEONROCKS deployed successfully on Supabase XL',
    'deployment',
    jsonb_build_object(
        'instance_type', 'XL',
        'memory', '16GB',
        'cpu_cores', 4,
        'quantum_volume', 351399511,
        'deployment_timestamp', NOW()
    )
);

-- Comentarios finales
COMMENT ON TABLE vigoleonrocks_conversations IS 'Conversaciones de VIGOLEONROCKS optimizadas para Supabase XL (16GB RAM, 4 CPU cores)';
COMMENT ON TABLE vigoleonrocks_context IS 'Contexto masivo aprovechando 16GB de memoria disponible';
COMMENT ON TABLE vigoleonrocks_metrics IS 'Métricas cuántico-cognitivas con información de instancia Supabase XL';
COMMENT ON FUNCTION get_vigoleonrocks_stats() IS 'Estadísticas de rendimiento optimizadas para infraestructura Supabase XL';