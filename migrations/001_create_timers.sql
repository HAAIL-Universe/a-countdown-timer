CREATE TABLE timers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    duration INTEGER NOT NULL,
    elapsed_time INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'idle',
    urgency_level INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
