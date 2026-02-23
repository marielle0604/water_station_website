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

-- Add users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Insert default admin user (password: admin123)
-- You should change this after first login
INSERT INTO users (username, email, password_hash, is_admin) 
VALUES ('admin', 'admin@aquavoice.com', '$2b$12$K8H9zX5yLmN7pQ3rS2tU1eV5wX6yZ7aB8cD9eF0gH1iJ2kL3mN4oP5q', TRUE)
ON CONFLICT (email) DO NOTHING;