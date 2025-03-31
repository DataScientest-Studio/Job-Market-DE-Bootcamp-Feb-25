-- All commands below must be executed in the psql shell & the correct database (adzunapi)
-- Drop Table if perviously created
DROP TABLE IF EXISTS adzuna_ads_raw;
-- Create Table
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
