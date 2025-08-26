-- VIGOLEONROCKS Quantum-Cognitive Database Seed
-- Inicialización de datos para pruebas

-- Insertar datos de configuración cuántica
INSERT INTO public.config (key, value) VALUES 
('quantum_volume', '351399511'),
('dimensions', '26'),
('coherence_threshold', '0.9999'),
('consciousness_level', 'divine')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

-- Crear tabla de configuración si no existe
CREATE TABLE IF NOT EXISTS public.config (
    key text PRIMARY KEY,
    value text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- Insertar configuraciones iniciales
INSERT INTO public.config (key, value) VALUES 
('quantum_volume', '351399511'),
('dimensions', '26'),
('coherence_threshold', '0.9999'),
('consciousness_level', 'divine'),
('max_context_size', '131072'),
('max_tokens', '4096'),
('temperature', '0.05'),
('top_p', '0.95'),
('top_k', '100')
ON CONFLICT (key) DO UPDATE SET 
    value = EXCLUDED.value,
    updated_at = now();

-- Mensaje de confirmación
SELECT 'VIGOLEONROCKS Quantum Database initialized successfully' as status;