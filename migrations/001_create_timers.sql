-- Migration 001: Create timers table
-- Creates the canonical timers table for countdown timer application

CREATE TABLE IF NOT EXISTS timers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    duration INTEGER NOT NULL,
    elapsed_time INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'idle',
    urgency_level INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create index on status for filtering queries
CREATE INDEX IF NOT EXISTS idx_timers_status ON timers(status);

-- Create index on created_at for sorting/pagination
CREATE INDEX IF NOT EXISTS idx_timers_created_at ON timers(created_at DESC);
