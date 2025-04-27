CREATE TABLE adzuna_ads (
    ads_id SERIAL PRIMARY KEY,
    job_title TEXT NOT NULL,
    employer TEXT NOT NULL,
    job_category TEXT,
    job_location TEXT,
    posted_date TIMESTAMP,
    salary_min FLOAT,
    salary_max FLOAT,
    contract_type TEXT,
    fixed_contract BOOLEAN,
    limited_contract BOOLEAN,
    contract_undefined BOOLEAN,
    UNIQUE (job_title, employer, posted_date)
);
title,company,category,location,created,salary_min,salary_max,contract_type

------------------NON UTF-----------------------
-- Drop Table if perviously created
DROP TABLE IF EXISTS categories;
-- Create Table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    tag TEXT NOT NULL,
    class TEXT NOT NULL,
    label TEXT NOT NULL
);

--categories: table name in adzunadb
COPY categories(id, tag, class, label)
FROM '/tmp/adzuna_category.csv'
DELIMITER ','
CSV HEADER;

----------------OLD-------------------
-- Drop Table if perviously created
DROP TABLE IF EXISTS adzuna_category;
-- Create Table
CREATE TABLE adzuna_category (
    categoryid SERIAL PRIMARY KEY,
    categorytag TEXT NOT NULL,
    countrylanguagecategorytag TEXT NOT NULL
);
-- Insert Data from exitsting CSV file - doesn't work
COPY Salary_M24(Index, Month, Location, "Job Title", Salary)
FROM '../data_collection/output_files/adzuna_salary_24M.csv'
DELIMITER ','
CSV HEADER;
