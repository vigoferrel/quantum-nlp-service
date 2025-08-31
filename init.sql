-- 🚀 VIGOLEONROCKS Database Initialization
-- Script para inicializar PostgreSQL con las tablas necesarias

-- Crear base de datos si no existe
-- CREATE DATABASE vigoleonrocks;

-- Conectar a la base de datos
-- \c vigoleonrocks;

-- Crear tabla para conversaciones
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'es',
    profile VARCHAR(50) DEFAULT 'human',
    quantum_states INTEGER DEFAULT 26,
    processing_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla para métricas del sistema
CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(255) NOT NULL,
    metric_value FLOAT,
    metric_type VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla para usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Crear tabla para configuraciones
CREATE TABLE IF NOT EXISTS configurations (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value TEXT,
    config_type VARCHAR(50) DEFAULT 'string',
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla para logs de API
CREATE TABLE IF NOT EXISTS api_logs (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255),
    method VARCHAR(10),
    user_id VARCHAR(255),
    ip_address INET,
    user_agent TEXT,
    request_data JSONB,
    response_data JSONB,
    status_code INTEGER,
    processing_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla para análisis arquetipal
CREATE TABLE IF NOT EXISTS archetypal_analysis (
    id SERIAL PRIMARY KEY,
    text_input TEXT NOT NULL,
    dominant_archetype VARCHAR(100),
    patterns JSONB,
    confidence FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla para traducciones
CREATE TABLE IF NOT EXISTS translations (
    id SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    source_language VARCHAR(10),
    target_language VARCHAR(10),
    confidence FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_api_logs_created_at ON api_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_archetypal_analysis_created_at ON archetypal_analysis(created_at);
CREATE INDEX IF NOT EXISTS idx_translations_created_at ON translations(created_at);

-- Insertar configuraciones por defecto
INSERT INTO configurations (config_key, config_value, config_type, description) VALUES
('quantum_states', '26', 'integer', 'Número de estados cuánticos activos'),
('default_profile', 'human', 'string', 'Perfil por defecto para respuestas'),
('max_request_size', '1048576', 'integer', 'Tamaño máximo de request en bytes'),
('rate_limit_requests', '100', 'integer', 'Límite de requests por hora'),
('cache_timeout', '300', 'integer', 'Timeout de cache en segundos'),
('log_level', 'INFO', 'string', 'Nivel de logging'),
('maintenance_mode', 'false', 'boolean', 'Modo mantenimiento activado/desactivado')
ON CONFLICT (config_key) DO NOTHING;

-- Insertar usuario administrador por defecto
-- NOTA: Cambia la contraseña después de la instalación
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@vigoleonrocks.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fMmiP0K6', 'admin')
ON CONFLICT (username) DO NOTHING;

-- Crear función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Crear triggers para updated_at
CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_configurations_updated_at BEFORE UPDATE ON configurations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Crear vista para estadísticas de uso
CREATE OR REPLACE VIEW usage_statistics AS
SELECT
    DATE(created_at) as date,
    COUNT(*) as total_requests,
    COUNT(DISTINCT user_id) as unique_users,
    AVG(processing_time) as avg_processing_time,
    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
FROM api_logs
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Comentarios en las tablas
COMMENT ON TABLE conversations IS 'Almacena todas las conversaciones del sistema';
COMMENT ON TABLE system_metrics IS 'Métricas del sistema para monitoreo';
COMMENT ON TABLE users IS 'Usuarios del sistema con roles y permisos';
COMMENT ON TABLE configurations IS 'Configuraciones del sistema';
COMMENT ON TABLE api_logs IS 'Logs detallados de todas las llamadas a la API';
COMMENT ON TABLE archetypal_analysis IS 'Resultados de análisis arquetipal';
COMMENT ON TABLE translations IS 'Historial de traducciones realizadas';

-- Otorgar permisos básicos (ajusta según necesites)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO vigoleonrocks;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO vigoleonrocks;