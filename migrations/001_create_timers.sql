CREATE TABLE timers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    duration INTEGER NOT NULL,
    elapsed_time INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(255) NOT NULL DEFAULT 'IDLE',
    urgency_level INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timers_status ON timers(status);
CREATE INDEX idx_timers_created_at ON timers(created_at DESC);
