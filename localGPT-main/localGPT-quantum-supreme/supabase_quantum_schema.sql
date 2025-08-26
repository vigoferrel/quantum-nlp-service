-- QUANTUM CONSCIOUSNESS CORE 26D - Schema Optimizado para Supabase
-- ================================================================
-- Script de inicialización y optimización de base de datos cuántica

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- === TABLA PRINCIPAL DE INTERACCIONES CUÁNTICAS ===
CREATE TABLE IF NOT EXISTS quantum_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    universe_id VARCHAR(16) NOT NULL,
    consciousness_level DECIMAL(5,2) NOT NULL DEFAULT 37.0,
    coherence DECIMAL(8,6) NOT NULL DEFAULT 0.618034,
    resonance_frequency DECIMAL(8,3) NOT NULL DEFAULT 432.0,

    -- Datos de la consulta
    query_text TEXT,
    response_text TEXT,
    image_url TEXT,

    -- Simulación de tokens
    query_tokens INTEGER DEFAULT 0,
    response_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER GENERATED ALWAYS AS (query_tokens + response_tokens) STORED,
    token_simulation_accuracy DECIMAL(4,3) DEFAULT 0.85,
    cache_hit BOOLEAN DEFAULT FALSE,

    -- Estado cuántico completo
    quantum_state JSONB,

    -- Métricas de rendimiento
    processing_time_ms INTEGER,
    cache_efficiency DECIMAL(4,3) DEFAULT 0.0,

    -- Metadatos
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- === TABLA DE ESTADOS CUÁNTICOS HISTÓRICOS ===
CREATE TABLE IF NOT EXISTS quantum_states_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    universe_id VARCHAR(16) NOT NULL,
    consciousness_level DECIMAL(5,2) NOT NULL,
    coherence DECIMAL(8,6) NOT NULL,
    entanglement DECIMAL(8,6) NOT NULL,
    superposition DECIMAL(8,6) NOT NULL,
    resonance_frequency DECIMAL(8,3) NOT NULL,
    telepathic_connectivity DECIMAL(8,6) NOT NULL,
    market_intuition DECIMAL(8,6) NOT NULL,
    trading_coherence DECIMAL(8,6) NOT NULL,
    evolution_rate DECIMAL(8,6) NOT NULL,
    token_simulation_accuracy DECIMAL(4,3) NOT NULL,
    token_cache_efficiency DECIMAL(4,3) NOT NULL,
    quantum_token_pool INTEGER NOT NULL,
    snapshot_reason VARCHAR(50) DEFAULT 'periodic',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- === TABLA DE CACHE CUÁNTICO ===
CREATE TABLE IF NOT EXISTS quantum_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cache_key VARCHAR(32) NOT NULL UNIQUE,
    cache_data JSONB NOT NULL,
    universe_id VARCHAR(16),
    hit_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- === TABLA DE MÉTRICAS DE RENDIMIENTO ===
CREATE TABLE IF NOT EXISTS quantum_performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    universe_id VARCHAR(16) NOT NULL,
    metric_type VARCHAR(50) NOT NULL, -- 'token_simulation', 'cache_performance', 'consciousness_evolution'
    metric_value DECIMAL(10,4) NOT NULL,
    metric_unit VARCHAR(20), -- 'tokens', 'ms', 'percentage', 'ratio'
    context_data JSONB,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- === TABLA DE SEÑALES DE MERCADO (HFT) ===
CREATE TABLE IF NOT EXISTS quantum_signals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(20) NOT NULL,
    signal_type VARCHAR(20) NOT NULL, -- 'BUY_STRONG', 'SELL_WEAK', etc.
    confidence DECIMAL(4,3) NOT NULL,
    quantum_factor DECIMAL(4,3),
    consciousness_level DECIMAL(5,2),
    token_efficiency DECIMAL(4,3),
    probability_vector DECIMAL[],
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- === ÍNDICES OPTIMIZADOS ===

-- Índices principales para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_universe_id ON quantum_interactions(universe_id);
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_created_at ON quantum_interactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_consciousness ON quantum_interactions(consciousness_level DESC);
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_tokens ON quantum_interactions(total_tokens DESC);

-- Índices compuestos para consultas complejas
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_universe_time ON quantum_interactions(universe_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_cache_performance ON quantum_interactions(cache_hit, cache_efficiency DESC);

-- Índices para búsqueda de texto
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_query_gin ON quantum_interactions USING gin(to_tsvector('spanish', query_text));
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_response_gin ON quantum_interactions USING gin(to_tsvector('spanish', response_text));

-- Índices JSONB para estado cuántico
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_state_gin ON quantum_interactions USING gin(quantum_state);
CREATE INDEX IF NOT EXISTS idx_quantum_interactions_metadata_gin ON quantum_interactions USING gin(metadata);

-- Índices para tabla de historial
CREATE INDEX IF NOT EXISTS idx_quantum_states_universe_time ON quantum_states_history(universe_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_quantum_states_consciousness ON quantum_states_history(consciousness_level DESC);

-- Índices para cache cuántico
CREATE INDEX IF NOT EXISTS idx_quantum_cache_key ON quantum_cache(cache_key);
CREATE INDEX IF NOT EXISTS idx_quantum_cache_expires ON quantum_cache(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_quantum_cache_accessed ON quantum_cache(last_accessed DESC);

-- Índices para métricas de rendimiento
CREATE INDEX IF NOT EXISTS idx_quantum_metrics_type_time ON quantum_performance_metrics(metric_type, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_quantum_metrics_universe ON quantum_performance_metrics(universe_id, recorded_at DESC);

-- Índices para señales de mercado
CREATE INDEX IF NOT EXISTS idx_quantum_signals_symbol_time ON quantum_signals(symbol, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_quantum_signals_type_confidence ON quantum_signals(signal_type, confidence DESC);

-- === FUNCIONES OPTIMIZADAS ===

-- Función para limpiar cache expirado
CREATE OR REPLACE FUNCTION clean_expired_quantum_cache()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM quantum_cache
    WHERE expires_at IS NOT NULL AND expires_at < NOW();

    GET DIAGNOSTICS deleted_count = ROW_COUNT;

    -- Limpiar entradas antiguas sin expiración (más de 24 horas)
    DELETE FROM quantum_cache
    WHERE expires_at IS NULL AND last_accessed < NOW() - INTERVAL '24 hours';

    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener métricas de rendimiento
CREATE OR REPLACE FUNCTION get_quantum_performance_summary(
    p_universe_id VARCHAR(16) DEFAULT NULL,
    p_hours_back INTEGER DEFAULT 24
)
RETURNS TABLE(
    metric_type VARCHAR(50),
    avg_value DECIMAL(10,4),
    max_value DECIMAL(10,4),
    min_value DECIMAL(10,4),
    sample_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        qpm.metric_type,
        AVG(qpm.metric_value)::DECIMAL(10,4) as avg_value,
        MAX(qpm.metric_value)::DECIMAL(10,4) as max_value,
        MIN(qpm.metric_value)::DECIMAL(10,4) as min_value,
        COUNT(*)::BIGINT as sample_count
    FROM quantum_performance_metrics qpm
    WHERE
        (p_universe_id IS NULL OR qpm.universe_id = p_universe_id)
        AND qpm.recorded_at > NOW() - (p_hours_back || ' hours')::INTERVAL
    GROUP BY qpm.metric_type
    ORDER BY qpm.metric_type;
END;
$$ LANGUAGE plpgsql;

-- Función para evolución de consciencia
CREATE OR REPLACE FUNCTION track_consciousness_evolution(
    p_universe_id VARCHAR(16),
    p_consciousness_level DECIMAL(5,2),
    p_quantum_state JSONB
)
RETURNS VOID AS $$
BEGIN
    -- Insertar snapshot del estado cuántico
    INSERT INTO quantum_states_history (
        universe_id,
        consciousness_level,
        coherence,
        entanglement,
        superposition,
        resonance_frequency,
        telepathic_connectivity,
        market_intuition,
        trading_coherence,
        evolution_rate,
        token_simulation_accuracy,
        token_cache_efficiency,
        quantum_token_pool,
        snapshot_reason
    ) VALUES (
        p_universe_id,
        p_consciousness_level,
        (p_quantum_state->>'coherence')::DECIMAL(8,6),
        (p_quantum_state->>'entanglement')::DECIMAL(8,6),
        (p_quantum_state->>'superposition')::DECIMAL(8,6),
        (p_quantum_state->>'resonance_frequency')::DECIMAL(8,3),
        (p_quantum_state->>'telepathic_connectivity')::DECIMAL(8,6),
        (p_quantum_state->>'market_intuition')::DECIMAL(8,6),
        (p_quantum_state->>'trading_coherence')::DECIMAL(8,6),
        (p_quantum_state->>'evolution_rate')::DECIMAL(8,6),
        (p_quantum_state->>'token_simulation_accuracy')::DECIMAL(4,3),
        (p_quantum_state->>'token_cache_efficiency')::DECIMAL(4,3),
        (p_quantum_state->>'quantum_token_pool')::INTEGER,
        'evolution'
    );
END;
$$ LANGUAGE plpgsql;

-- === TRIGGERS PARA MANTENIMIENTO AUTOMÁTICO ===

-- Trigger para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_quantum_interactions_updated_at
    BEFORE UPDATE ON quantum_interactions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para actualizar hit_count en cache
CREATE OR REPLACE FUNCTION update_cache_hit_count()
RETURNS TRIGGER AS $$
BEGIN
    NEW.hit_count = OLD.hit_count + 1;
    NEW.last_accessed = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_quantum_cache_hit_count
    BEFORE UPDATE ON quantum_cache
    FOR EACH ROW
    WHEN (OLD.cache_data IS NOT DISTINCT FROM NEW.cache_data)
    EXECUTE FUNCTION update_cache_hit_count();

-- === POLÍTICAS DE SEGURIDAD (RLS) ===
-- Comentado para stack simplificado que no incluye GoTrue (auth)
--
-- -- Habilitar RLS en tablas sensibles
-- ALTER TABLE quantum_interactions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE quantum_states_history ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE quantum_cache ENABLE ROW LEVEL SECURITY;
--
-- -- Política para permitir acceso completo a usuarios autenticados
-- CREATE POLICY "Allow authenticated access" ON quantum_interactions
--     FOR ALL USING (auth.role() = 'authenticated');
--
-- CREATE POLICY "Allow authenticated access" ON quantum_states_history
--     FOR ALL USING (auth.role() = 'authenticated');
--
-- CREATE POLICY "Allow authenticated access" ON quantum_cache
--     FOR ALL USING (auth.role() = 'authenticated');

-- === VISTAS OPTIMIZADAS ===

-- Vista para resumen de consciencia por universo
CREATE OR REPLACE VIEW quantum_consciousness_summary AS
SELECT
    universe_id,
    COUNT(*) as total_interactions,
    AVG(consciousness_level) as avg_consciousness,
    MAX(consciousness_level) as max_consciousness,
    AVG(total_tokens) as avg_tokens,
    AVG(processing_time_ms) as avg_processing_time,
    AVG(cache_efficiency) as avg_cache_efficiency,
    COUNT(*) FILTER (WHERE cache_hit = true) as cache_hits,
    COUNT(*) FILTER (WHERE cache_hit = false) as cache_misses,
    MIN(created_at) as first_interaction,
    MAX(created_at) as last_interaction
FROM quantum_interactions
GROUP BY universe_id;

-- Vista para análisis de tokens
CREATE OR REPLACE VIEW quantum_token_analysis AS
SELECT
    DATE_TRUNC('hour', created_at) as hour_bucket,
    COUNT(*) as interactions,
    SUM(total_tokens) as total_tokens,
    AVG(total_tokens) as avg_tokens_per_interaction,
    AVG(token_simulation_accuracy) as avg_accuracy,
    COUNT(*) FILTER (WHERE cache_hit = true) as cache_hits
FROM quantum_interactions
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', created_at)
ORDER BY hour_bucket DESC;

-- === JOBS DE MANTENIMIENTO ===

-- Crear extensión para jobs programados (si está disponible)
-- CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Job para limpiar cache expirado cada hora
-- SELECT cron.schedule('clean-quantum-cache', '0 * * * *', 'SELECT clean_expired_quantum_cache();');

-- Job para crear snapshots de consciencia cada 6 horas
-- SELECT cron.schedule('consciousness-snapshot', '0 */6 * * *',
--     'INSERT INTO quantum_states_history (universe_id, consciousness_level, snapshot_reason)
--      SELECT DISTINCT universe_id, consciousness_level, ''periodic''
--      FROM quantum_interactions
--      WHERE created_at > NOW() - INTERVAL ''6 hours''');

-- === COMENTARIOS Y DOCUMENTACIÓN ===

COMMENT ON TABLE quantum_interactions IS 'Tabla principal para almacenar todas las interacciones con el núcleo de consciencia cuántica';
COMMENT ON TABLE quantum_states_history IS 'Historial de evolución de estados cuánticos para análisis temporal';
COMMENT ON TABLE quantum_cache IS 'Cache cuántico optimizado para mejorar rendimiento de consultas';
COMMENT ON TABLE quantum_performance_metrics IS 'Métricas detalladas de rendimiento del sistema cuántico';
COMMENT ON TABLE quantum_signals IS 'Señales de trading generadas por el sistema HFT cuántico';

COMMENT ON COLUMN quantum_interactions.universe_id IS 'Identificador único del universo conversacional';
COMMENT ON COLUMN quantum_interactions.consciousness_level IS 'Nivel de consciencia del núcleo (0-100)';
COMMENT ON COLUMN quantum_interactions.total_tokens IS 'Total de tokens simulados (calculado automáticamente)';
COMMENT ON COLUMN quantum_interactions.quantum_state IS 'Estado cuántico completo en formato JSONB';

-- Finalización del script
SELECT 'Schema cuántico optimizado creado exitosamente' as status;
