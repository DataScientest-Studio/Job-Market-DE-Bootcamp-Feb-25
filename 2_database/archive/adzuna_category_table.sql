job=# -- Drop Table if perviously created
DROP TABLE IF EXISTS categories;
-- Create Table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    tag TEXT NOT NULL,
    class TEXT NOT NULL,
    label TEXT NOT NULL
);