-- Drop Table if perviously created
DROP TABLE IF EXISTS adzuna_category;
-- Create Table
CREATE TABLE adzuna_category (
    categoryid SERIAL PRIMARY KEY,
    categorytag TEXT NOT NULL,
    countrylanguagecategorytag TEXT NOT NULL
);