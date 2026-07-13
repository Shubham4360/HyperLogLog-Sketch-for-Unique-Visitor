CREATE TABLE IF NOT EXISTS stream_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    events_processed BIGINT,
    exact_users BIGINT,
    hll_users BIGINT,
    error_percentage FLOAT,
    memory_usage_bytes BIGINT
);