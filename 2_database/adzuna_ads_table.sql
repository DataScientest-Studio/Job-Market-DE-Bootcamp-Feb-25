-- All commands below must be executed in the psql shell & the correct database (adzunadb)
-- Drop Table if perviously created
DROP TABLE IF EXISTS adzuna_ads_raw;
-- Create Table
CREATE TABLE adzuna_ads (
    id SERIAL PRIMARY KEY,
    title TEXT NULL,
    company TEXT NULL,
    category TEXT,
    location TEXT,
    created TIMESTAMP,
    salary_min FLOAT,
    salary_max FLOAT,
    contract_type TEXT
);

COPY adzuna_ads(title,company,category,location,created,salary_min,salary_max,contract_type)
FROM '/tmp/adzuna_ads.csv'
DELIMITER ','
CSV HEADER;