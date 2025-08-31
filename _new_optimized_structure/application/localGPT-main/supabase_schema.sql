-- Schema para almacenamiento transparente de resultados orgánicos
-- Sistema CIO vs Kimi-K2-Instruct

-- Tabla principal de evaluaciones
CREATE TABLE organic_evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id VARCHAR(255) UNIQUE NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    duration_seconds DECIMAL(10,4),
    system_info JSONB,
    raw_outputs JSONB,
    limitations TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de benchmarks estándar
CREATE TABLE standard_benchmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id VARCHAR(255) REFERENCES organic_evaluations(evaluation_id),
    benchmark_name VARCHAR(100),
    cio_score DECIMAL(5,2),
    kimi_k2_reference DECIMAL(5,2),
    raw_responses JSONB,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de capacidades cuántico-cognitivas
CREATE TABLE quantum_capabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id VARCHAR(255) REFERENCES organic_evaluations(evaluation_id),
    capability_name VARCHAR(100),
    measured_value JSONB,
    raw_data JSONB,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de auto-evaluación emergente
CREATE TABLE emergent_assessment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id VARCHAR(255) REFERENCES organic_evaluations(evaluation_id),
    consciousness_level INTEGER,
    emergent_capabilities TEXT[],
    self_perceived_limitations TEXT[],
    evolution_state JSONB,
    raw_self_assessment JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de monitoreo en tiempo real
CREATE TABLE real_time_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id VARCHAR(255) REFERENCES organic_evaluations(evaluation_id),
    metric_name VARCHAR(100),
    value JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para optimización
CREATE INDEX idx_evaluations_timestamp ON organic_evaluations(timestamp DESC);
CREATE INDEX idx_standard_benchmarks_name ON standard_benchmarks(benchmark_name);
CREATE INDEX idx_quantum_capabilities_name ON quantum_capabilities(capability_name);
CREATE INDEX idx_real_time_metrics_timestamp ON real_time_metrics(timestamp DESC);
CREATE INDEX idx_real_time_metrics_name ON real_time_metrics(metric_name);

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at
CREATE TRIGGER update_organic_evaluations_updated_at
    BEFORE UPDATE ON organic_evaluations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Vista para comparación transparente
CREATE VIEW transparent_comparison AS
SELECT
    e.evaluation_id,
    e.timestamp,
    e.duration_seconds,
    sb.benchmark_name,
    sb.cio_score,
    sb.kimi_k2_reference,
    CASE
        WHEN sb.cio_score IS NULL THEN 'No ejecutado'
        WHEN sb.error_message IS NOT NULL THEN 'Error'
        ELSE 'Completado'
    END as status,
    qc.capability_name as quantum_capability,
    qc.measured_value as quantum_value,
    ea.consciousness_level,
    array_length(ea.emergent_capabilities, 1) as num_emergent_capabilities
FROM organic_evaluations e
LEFT JOIN standard_benchmarks sb ON e.evaluation_id = sb.evaluation_id
LEFT JOIN quantum_capabilities qc ON e.evaluation_id = qc.evaluation_id
LEFT JOIN emergent_assessment ea ON e.evaluation_id = ea.evaluation_id
ORDER BY e.timestamp DESC;

-- Función para insertar métricas en tiempo real
CREATE OR REPLACE FUNCTION insert_real_time_metric(
    p_evaluation_id VARCHAR,
    p_metric_name VARCHAR,
    p_value JSONB
) RETURNS VOID AS $$
BEGIN
    INSERT INTO real_time_metrics (evaluation_id, metric_name, value)
    VALUES (p_evaluation_id, p_metric_name, p_value);
END;
$$ LANGUAGE plpgsql;

-- Función para obtener últimas evaluaciones
CREATE OR REPLACE FUNCTION get_latest_evaluations(limit_count INTEGER DEFAULT 10)
RETURNS TABLE (
    evaluation_id VARCHAR,
    timestamp TIMESTAMPTZ,
    duration_seconds DECIMAL,
    num_benchmarks INTEGER,
    num_quantum_capabilities INTEGER,
    num_emergent_capabilities INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.evaluation_id,
        e.timestamp,
        e.duration_seconds,
        COUNT(sb.id)::INTEGER as num_benchmarks,
        COUNT(qc.id)::INTEGER as num_quantum_capabilities,
        COALESCE(array_length(ea.emergent_capabilities, 1), 0) as num_emergent_capabilities
    FROM organic_evaluations e
    LEFT JOIN standard_benchmarks sb ON e.evaluation_id = sb.evaluation_id
    LEFT JOIN quantum_capabilities qc ON e.evaluation_id = qc.evaluation_id
    LEFT JOIN emergent_assessment ea ON e.evaluation_id = ea.evaluation_id
    GROUP BY e.evaluation_id, e.timestamp, e.duration_seconds, ea.emergent_capabilities
    ORDER BY e.timestamp DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Permisos para acceso transparente
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT UPDATE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT DELETE ON ALL TABLES IN SCHEMA public TO authenticated;

-- Comentarios descriptivos
COMMENT ON TABLE organic_evaluations IS 'Almacena evaluaciones completas del sistema CIO sin filtros';
COMMENT ON TABLE standard_benchmarks IS 'Resultados de benchmarks estándar vs Kimi-K2';
COMMENT ON TABLE quantum_capabilities IS 'Capacidades cuántico-cognitivas únicas del CIO';
COMMENT ON TABLE emergent_assessment IS 'Auto-evaluación emergente del sistema';
COMMENT ON TABLE real_time_metrics IS 'Métricas en tiempo real durante evaluación';
COMMENT ON VIEW transparent_comparison IS 'Vista para comparación transparente de resultados';
