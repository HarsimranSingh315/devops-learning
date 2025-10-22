-- Create visitors table if it doesn't exist
CREATE TABLE IF NOT EXISTS visitors (
    id SERIAL PRIMARY KEY,              -- Auto-incrementing ID
    name VARCHAR(100) NOT NULL,          -- Visitor name (max 100 chars)
    message TEXT,                        -- Their message (unlimited length)
    timestamp TIMESTAMP DEFAULT NOW()    -- When they visited (auto-filled)
);

-- Create index on timestamp for faster queries
CREATE INDEX IF NOT EXISTS idx_timestamp ON visitors(timestamp DESC);

-- Insert sample data for testing
INSERT INTO visitors (name, message) VALUES 
    ('Alice', 'Hello from the first visitor!'),
    ('Bob', 'This is an amazing guestbook!');
