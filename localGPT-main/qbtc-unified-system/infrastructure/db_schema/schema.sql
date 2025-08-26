-- #################################################################
-- # QBTC Unified System - Main Database Schema
-- # Version: 1.0
-- # Author: Roo
-- # Description: This schema defines the core data structures for
-- #              the QBTC system, including logs, states, user
-- #              interactions, and the knowledge graph for the
-- #              reasoning and learning core.
-- #################################################################

-- Create a dedicated schema to avoid conflicts
CREATE SCHEMA IF NOT EXISTS qbtc_main;
SET search_path TO qbtc_main;

-- #################################################################
-- # Table: Sessions
-- # Purpose: Tracks each unique interaction session with the system.
-- #################################################################
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255), -- Can be linked to an external user table
    start_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMPTZ,
    client_info JSONB, -- e.g., browser, IP, device
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- #################################################################
-- # Table: Interactions
-- # Purpose: Logs every individual request/response pair (turn)
-- #          within a session. This is the primary event log.
-- #################################################################
CREATE TABLE interactions (
    interaction_id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES sessions(session_id),
    parent_interaction_id BIGINT REFERENCES interactions(interaction_id), -- For threaded conversations
    request_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    request_payload JSONB NOT NULL,
    response_timestamp TIMESTAMPTZ,
    response_payload JSONB,
    -- Metadata captures routing, model selection, tool calls, etc.
    metadata JSONB,
    -- Tracks the status of the interaction (e.g., pending, success, failed)
    status VARCHAR(50) DEFAULT 'pending',
    -- Quick indexing for performance
    INDEX idx_interactions_session (session_id),
    INDEX idx_interactions_timestamp (request_timestamp)
);

-- #################################################################
-- # Table: ToolCalls
-- # Purpose: A detailed log of every tool selected and executed
-- #          during an interaction.
-- #################################################################
CREATE TABLE tool_calls (
    tool_call_id BIGSERIAL PRIMARY KEY,
    interaction_id BIGINT NOT NULL REFERENCES interactions(interaction_id),
    tool_name VARCHAR(255) NOT NULL,
    tool_input JSONB,
    tool_output JSONB,
    status VARCHAR(50) NOT NULL, -- e.g., 'success', 'error'
    execution_time_ms INT,
    call_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tool_calls_interaction (interaction_id),
    INDEX idx_tool_calls_name (tool_name)
);

-- #################################################################
-- # Table: KnowledgeGraphNodes
-- # Purpose: Stores nodes (entities) for the system's long-term
-- #          memory and reasoning graph (e.g., concepts, users, files).
-- #################################################################
CREATE TABLE knowledge_graph_nodes (
    node_id BIGSERIAL PRIMARY KEY,
    node_type VARCHAR(100) NOT NULL,
    -- The attributes and data of the node itself
    properties JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    -- For quick lookups by type
    INDEX idx_kg_nodes_type (node_type)
);

-- #################################################################
-- # Table: KnowledgeGraphEdges
-- # Purpose: Stores edges (relationships) between nodes in the
-- #          knowledge graph.
-- #################################################################
CREATE TABLE knowledge_graph_edges (
    edge_id BIGSERIAL PRIMARY KEY,
    source_node_id BIGINT NOT NULL REFERENCES knowledge_graph_nodes(node_id) ON DELETE CASCADE,
    target_node_id BIGINT NOT NULL REFERENCES knowledge_graph_nodes(node_id) ON DELETE CASCADE,
    relationship_type VARCHAR(100) NOT NULL,
    -- Attributes of the relationship itself (e.g., weight, certainty)
    properties JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_kg_edges_source (source_node_id),
    INDEX idx_kg_edges_target (target_node_id),
    INDEX idx_kg_edges_rel_type (relationship_type)
);

-- #################################################################
-- # Function to automatically update timestamps
-- #################################################################
CREATE OR REPLACE FUNCTION update_last_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.last_updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

-- #################################################################
-- # Triggers to manage the last_updated_at timestamps
-- #################################################################
CREATE TRIGGER tg_update_kg_nodes_timestamp
BEFORE UPDATE ON knowledge_graph_nodes
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at_column();

CREATE TRIGGER tg_update_kg_edges_timestamp
BEFORE UPDATE ON knowledge_graph_edges
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at_column();


-- End of Schema
