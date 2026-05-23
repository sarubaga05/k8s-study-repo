CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    choice VARCHAR(10) CHECK (choice IN ('cat', 'dog')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_votes_choice ON votes(choice);