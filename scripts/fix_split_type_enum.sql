-- Drop the existing enum type if it exists and recreate the table structure
-- This will reset your data, but fix the enum issue

-- Drop existing tables in correct order (due to foreign keys)
DROP TABLE IF EXISTS expense_splits CASCADE;
DROP TABLE IF EXISTS expenses CASCADE;
DROP TABLE IF EXISTS group_members CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop the enum type if it exists
DROP TYPE IF EXISTS splittype CASCADE;

-- Recreate tables with split_type as VARCHAR instead of enum
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id),
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    description VARCHAR NOT NULL,
    amount FLOAT NOT NULL,
    paid_by INTEGER REFERENCES users(id),
    group_id INTEGER REFERENCES groups(id),
    split_type VARCHAR NOT NULL CHECK (split_type IN ('equal', 'percentage')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expense_splits (
    id SERIAL PRIMARY KEY,
    expense_id INTEGER REFERENCES expenses(id),
    user_id INTEGER REFERENCES users(id),
    amount FLOAT NOT NULL,
    percentage FLOAT
);

-- Insert sample data
INSERT INTO users (name, email) VALUES 
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com'),
('Charlie Brown', 'charlie@example.com'),
('Diana Prince', 'diana@example.com'),
('Eve Wilson', 'eve@example.com');

-- Create sample groups
INSERT INTO groups (name) VALUES 
('Weekend Trip'),
('Office Lunch'),
('Roommate Expenses');

-- Add members to groups
-- Weekend Trip (Alice, Bob, Charlie, Diana)
INSERT INTO group_members (group_id, user_id) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4);

-- Office Lunch (Alice, Bob, Charlie, Diana, Eve)
INSERT INTO group_members (group_id, user_id) VALUES 
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5);

-- Roommate Expenses (Alice, Bob, Charlie)
INSERT INTO group_members (group_id, user_id) VALUES 
(3, 1), (3, 2), (3, 3);

-- Add sample expenses with string split_type
INSERT INTO expenses (description, amount, paid_by, group_id, split_type) VALUES 
('Hotel booking', 200.00, 1, 1, 'equal'),
('Gas for car', 80.00, 2, 1, 'equal'),
('Groceries', 120.00, 3, 1, 'equal'),
('Restaurant dinner', 150.75, 4, 1, 'equal');

-- Office Lunch expenses
INSERT INTO expenses (description, amount, paid_by, group_id, split_type) VALUES 
('Pizza order', 45.50, 1, 2, 'equal'),
('Coffee run', 25.00, 3, 2, 'equal'),
('Sandwich delivery', 35.00, 5, 2, 'equal');

-- Roommate Expenses
INSERT INTO expenses (description, amount, paid_by, group_id, split_type) VALUES 
('Electricity bill', 150.00, 1, 3, 'equal'),
('Internet bill', 60.00, 2, 3, 'equal'),
('Cleaning supplies', 40.00, 3, 3, 'equal');
