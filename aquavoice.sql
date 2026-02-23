-- Create database
CREATE DATABASE aquavoice_db;

-- Connect to database
\c aquavoice_db;

-- Create water stations table
CREATE TABLE IF NOT EXISTS water_stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES water_stations(id),
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT NOT NULL,
    suggestions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'read', 'archived'))
);

-- Insert water stations
INSERT INTO water_stations (name) VALUES
    ('VIOLY''S WATER REFILLING STATION'),
    ('BWM''S WATER REFILLING STATION'),
    ('FERNANDO''S WATER REFILLING STATION'),
    ('YAKAP AT HALIK WATER REFILLING STATION'),
    ('MARKEN MIST WATER REFILLING STATION')
ON CONFLICT (name) DO NOTHING;