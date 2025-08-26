-- Create model artifacts table
CREATE TABLE IF NOT EXISTS model_artifacts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    model_id TEXT NOT NULL,
    file_path TEXT NOT NULL,
    model_name TEXT,
    model_version TEXT,
    framework TEXT,
    architecture TEXT,
    training_data TEXT,
    metrics JSONB,
    parameters JSONB,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create model checkpoints table
CREATE TABLE IF NOT EXISTS model_checkpoints (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    model_id TEXT NOT NULL,
    checkpoint_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    epoch INTEGER,
    step INTEGER,
    metrics JSONB,
    hyperparameters JSONB,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create model configs table
CREATE TABLE IF NOT EXISTS model_configs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    model_id TEXT NOT NULL,
    config_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    config_type TEXT,
    parameters JSONB,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create training logs table
CREATE TABLE IF NOT EXISTS training_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    model_id TEXT NOT NULL,
    log_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    log_type TEXT,
    metrics JSONB,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_model_artifacts_model_id ON model_artifacts(model_id);
CREATE INDEX IF NOT EXISTS idx_model_checkpoints_model_id ON model_checkpoints(model_id);
CREATE INDEX IF NOT EXISTS idx_model_configs_model_id ON model_configs(model_id);
CREATE INDEX IF NOT EXISTS idx_training_logs_model_id ON training_logs(model_id);

-- Create RLS policies
ALTER TABLE model_artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE model_checkpoints ENABLE ROW LEVEL SECURITY;
ALTER TABLE model_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_logs ENABLE ROW LEVEL SECURITY;

-- Grant access to authenticated users
CREATE POLICY "Enable read access for authenticated users" ON model_artifacts
    FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Enable write access for authenticated users" ON model_artifacts
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Enable read access for authenticated users" ON model_checkpoints
    FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Enable write access for authenticated users" ON model_checkpoints
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Enable read access for authenticated users" ON model_configs
    FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Enable write access for authenticated users" ON model_configs
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Enable read access for authenticated users" ON training_logs
    FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Enable write access for authenticated users" ON training_logs
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
