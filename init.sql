-- Inicialización de la base de datos VIGOLEONROCKS
-- Versión: 1.0
-- Fecha: 2025-09-01

-- Crear esquema principal
CREATE SCHEMA IF NOT EXISTS vigoleonrocks;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS vigoleonrocks.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Tabla de sesiones de IA
CREATE TABLE IF NOT EXISTS vigoleonrocks.ai_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES vigoleonrocks.users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    model_used VARCHAR(100),
    total_tokens INTEGER DEFAULT 0,
    total_cost DECIMAL(10,6) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Tabla de mensajes de chat
CREATE TABLE IF NOT EXISTS vigoleonrocks.chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES vigoleonrocks.ai_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    processing_time DECIMAL(8,3),
    language_detected VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de métricas de rendimiento
CREATE TABLE IF NOT EXISTS vigoleonrocks.performance_metrics (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    response_time DECIMAL(8,3) NOT NULL,
    status_code INTEGER NOT NULL,
    user_agent TEXT,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de configuraciones del sistema
CREATE TABLE IF NOT EXISTS vigoleonrocks.system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value TEXT,
    config_type VARCHAR(50) DEFAULT 'string',
    is_encrypted BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de logs de errores
CREATE TABLE IF NOT EXISTS vigoleonrocks.error_logs (
    id SERIAL PRIMARY KEY,
    error_type VARCHAR(100) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    endpoint VARCHAR(255),
    user_id INTEGER REFERENCES vigoleonrocks.users(id),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de análisis arquetípicos
CREATE TABLE IF NOT EXISTS vigoleonrocks.archetype_analysis (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES vigoleonrocks.ai_sessions(id) ON DELETE CASCADE,
    text_content TEXT NOT NULL,
    dominant_archetype VARCHAR(100),
    archetype_patterns JSONB,
    confidence_score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de traducciones
CREATE TABLE IF NOT EXISTS vigoleonrocks.translations (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES vigoleonrocks.ai_sessions(id) ON DELETE CASCADE,
    source_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    source_language VARCHAR(10),
    target_language VARCHAR(10),
    translation_quality DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_users_email ON vigoleonrocks.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON vigoleonrocks.users(username);
CREATE INDEX IF NOT EXISTS idx_ai_sessions_user_id ON vigoleonrocks.ai_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_sessions_created_at ON vigoleonrocks.ai_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON vigoleonrocks.chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_created_at ON vigoleonrocks.performance_metrics(created_at);
CREATE INDEX IF NOT EXISTS idx_error_logs_created_at ON vigoleonrocks.error_logs(created_at);

-- Configuraciones iniciales del sistema
INSERT INTO vigoleonrocks.system_config (config_key, config_value, config_type) VALUES
('system_version', '1.0.0', 'string'),
('max_tokens_per_request', '4096', 'integer'),
('rate_limit_requests', '100', 'integer'),
('rate_limit_window', '3600', 'integer'),
('maintenance_mode', 'false', 'boolean'),
('quantum_states', '26', 'integer'),
('supported_languages', '["es", "en", "pt", "fr", "de", "it", "ja", "ko", "zh"]', 'json'),
('default_model', 'vigoleonrocks-quantum', 'string')
ON CONFLICT (config_key) DO NOTHING;

-- Usuario administrador por defecto (cambiar password en producción)
INSERT INTO vigoleonrocks.users (username, email, password_hash, full_name, is_admin) VALUES
('admin', 'admin@vigoleonrocks.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fMJyHnUeO', 'VIGOLEONROCKS Administrator', true)
ON CONFLICT (username) DO NOTHING;

-- Comentarios en las tablas
COMMENT ON TABLE vigoleonrocks.users IS 'Usuarios registrados en el sistema';
COMMENT ON TABLE vigoleonrocks.ai_sessions IS 'Sesiones de conversación con IA';
COMMENT ON TABLE vigoleonrocks.chat_messages IS 'Mensajes de chat en cada sesión';
COMMENT ON TABLE vigoleonrocks.performance_metrics IS 'Métricas de rendimiento del sistema';
COMMENT ON TABLE vigoleonrocks.system_config IS 'Configuraciones del sistema';
COMMENT ON TABLE vigoleonrocks.error_logs IS 'Logs de errores del sistema';
COMMENT ON TABLE vigoleonrocks.archetype_analysis IS 'Análisis arquetípicos realizados';
COMMENT ON TABLE vigoleonrocks.translations IS 'Traducciones realizadas por el sistema';

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION vigoleonrocks.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON vigoleonrocks.users
    FOR EACH ROW EXECUTE FUNCTION vigoleonrocks.update_updated_at_column();

CREATE TRIGGER update_ai_sessions_updated_at BEFORE UPDATE ON vigoleonrocks.ai_sessions
    FOR EACH ROW EXECUTE FUNCTION vigoleonrocks.update_updated_at_column();

CREATE TRIGGER update_system_config_updated_at BEFORE UPDATE ON vigoleonrocks.system_config
    FOR EACH ROW EXECUTE FUNCTION vigoleonrocks.update_updated_at_column();