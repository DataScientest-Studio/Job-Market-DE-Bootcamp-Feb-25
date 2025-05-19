-- All commands below must be executed in the psql shell & the correct database (adzunadb)
-- Drop Table if perviously created
DROP TABLE IF EXISTS adzuna_ads_all;
-- Create Table
CREATE TABLE adzuna_ads_all (
    job_offer_id SERIAL PRIMARY KEY,
    title TEXT NULL,
    company TEXT NULL,
    category TEXT,
    location TEXT,
    created TIMESTAMP,
    salary_min FLOAT,
    salary_max FLOAT,
    contract_type TEXT,
    fixed_contract INT,
    limited_contract INT,
    contract_undefined INT
);

-- in different terminal execute:
-- docker cp "../Job-Market-DE-Bootcamp-Feb-25/1_data_collection/cleanup_output_files/adzuna_ads_all_clean.csv" postgres_db:/tmp/

COPY adzuna_ads_all(job_offer_id, title,company,category,location,created,salary_min,salary_max,contract_type, fixed_contract,limited_contract,contract_undefined)
FROM '/tmp/adzuna_ads_all_clean.csv'
DELIMITER ','
CSV HEADER;