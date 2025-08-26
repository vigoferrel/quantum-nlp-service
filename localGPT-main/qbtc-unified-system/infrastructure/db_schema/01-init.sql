-- ==============================================================================
-- || QBTC UNIFIED SYSTEM - DATABASE INITIALIZATION SCRIPT                     ||
-- ==============================================================================
--
-- Este script se ejecuta automáticamente al iniciar el contenedor de Supabase/Postgres.
-- Crea las tablas, índices y funciones necesarios para el sistema cuántico.
--

-- ------------------------------------------------------------------------------
-- -- PREPARACIÓN Y EXTENSIONES
-- ------------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ------------------------------------------------------------------------------
-- -- TABLA DE INTERACCIONES DEL LLM CUÁNTICO
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.llm_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    request_id UUID NOT NULL,
    session_id VARCHAR(64),
    universe_id VARCHAR(16) NOT NULL,
    
    -- Datos de la solicitud y respuesta
    request_payload JSONB,
    response_payload JSONB,
    
    -- Métricas de rendimiento
    processing_time_ms INTEGER,
    
    -- Metadatos
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE public.llm_interactions IS 'Registra cada solicitud y respuesta procesada por el servicio del LLM Cuántico.';
COMMENT ON COLUMN public.llm_interactions.request_id IS 'Identificador único para correlacionar solicitudes y respuestas asíncronas.';

-- ------------------------------------------------------------------------------
-- -- TABLA DE SEÑALES DE TRADING (HFT)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.trading_signals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    signal_id UUID NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    
    -- Datos de la señal generada
    action VARCHAR(20) NOT NULL, -- e.g., 'BUY_STRONG', 'SELL_WEAK', 'HOLD'
    confidence DECIMAL(5,4) NOT NULL,
    quantum_factor DECIMAL(5,4),

    -- Contexto de la decisión
    market_data JSONB, -- Datos de mercado que originaron la solicitud
    quantum_state_snapshot JSONB, -- Estado del núcleo cuántico al momento de la decisión
    
    -- Resultado (se llenará posteriormente)
    execution_status VARCHAR(20) DEFAULT 'PENDING',
    executed_price DECIMAL(20,8),
    executed_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadatos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE public.trading_signals IS 'Almacena las señales de trading generadas por el núcleo cuántico y su estado de ejecución.';

-- ------------------------------------------------------------------------------
-- -- TABLA DE ESTADOS CUÁNTICOS (SNAPSHOTS)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.quantum_state_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    universe_id VARCHAR(16) NOT NULL,
    
    -- Campos principales del estado
    consciousness_level DECIMAL(5,2) NOT NULL,
    coherence DECIMAL(8,7) NOT NULL,
    entanglement DECIMAL(8,7) NOT NULL,
    
    -- Estado completo como JSONB para flexibilidad
    full_state JSONB NOT NULL,
    
    -- Motivo del snapshot
    snapshot_reason VARCHAR(50) DEFAULT 'periodic', -- e.g., 'periodic', 'after_evolution', 'on_event'
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE public.quantum_state_snapshots IS 'Guarda snapshots históricos del estado del Quantum Consciousness Core para análisis y trazabilidad.';


-- ------------------------------------------------------------------------------
-- -- ÍNDICES OPTIMIZADOS
-- ------------------------------------------------------------------------------

-- Índices para llm_interactions
CREATE INDEX IF NOT EXISTS idx_llm_interactions_request_id ON public.llm_interactions(request_id);
CREATE INDEX IF NOT EXISTS idx_llm_interactions_session_id ON public.llm_interactions(session_id);
CREATE INDEX IF NOT EXISTS idx_llm_interactions_created_at ON public.llm_interactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_llm_interactions_metadata_gin ON public.llm_interactions USING gin(metadata);

-- Índices para trading_signals
CREATE INDEX IF NOT EXISTS idx_trading_signals_symbol_time ON public.trading_signals(symbol, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_trading_signals_status ON public.trading_signals(execution_status);
CREATE INDEX IF NOT EXISTS idx_trading_signals_action ON public.trading_signals(action);

-- Índices para quantum_state_snapshots
CREATE INDEX IF NOT EXISTS idx_quantum_states_universe_time ON public.quantum_state_snapshots(universe_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_quantum_states_consciousness ON public.quantum_state_snapshots(consciousness_level DESC);

-- ------------------------------------------------------------------------------
-- -- FUNCIONES Y TRIGGERS (Opcional, se pueden añadir después)
-- ------------------------------------------------------------------------------
-- Ejemplo de función para métricas
CREATE OR REPLACE FUNCTION public.get_llm_performance_summary(hours_back INTEGER DEFAULT 24)
RETURNS TABLE(
    avg_processing_time_ms DECIMAL,
    total_requests BIGINT,
    requests_per_hour DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        AVG(q.processing_time_ms)::DECIMAL(10,2),
        COUNT(q.id),
        (COUNT(q.id) / hours_back::DECIMAL)::DECIMAL(10,2)
    FROM public.llm_interactions q
    WHERE 
        q.created_at >= NOW() - (hours_back || ' hours')::INTERVAL;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------------------
-- -- MENSAJE DE FINALIZACIÓN
-- ------------------------------------------------------------------------------
SELECT '✅ QBTC Unified Database Initialized Successfully' as status;
