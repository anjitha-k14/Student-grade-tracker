-- Run this file in MySQL to set up the database
-- Command: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS studentdb;

USE studentdb;

CREATE TABLE IF NOT EXISTS students (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100)  NOT NULL,
    subject VARCHAR(100)  NOT NULL,
    grade   INT           NOT NULL CHECK (grade BETWEEN 0 AND 100),
    created_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
);

-- Optional: insert sample data to test
INSERT INTO students (name, subject, grade) VALUES
    ('Anjith Kumar',  'Cloud Computing',  88),
    ('Priya Nair',    'Data Structures',  72),
    ('Rahul Menon',   'Web Technologies', 55),
    ('Sneha Thomas',  'Operating Systems',35);
