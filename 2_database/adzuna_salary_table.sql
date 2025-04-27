-- All commands below must be executed in the psql shell & the correct database (adzunapi)
-- Drop Table if perviously created
DROP TABLE IF EXISTS Salary_M24;
-- Create Table
CREATE TABLE Salary_M24 (
    Index SERIAL PRIMARY KEY,
    Month VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    "Job Title" VARCHAR(100) NOT NULL,
    Salary NUMERIC
);

-- when inside the container: adzunadb # Docker is searching for a file there and cannot access it locally
COPY Salary_M24(Index, Month, Location, "Job Title", Salary)
FROM '/tmp/adzuna_salary_24M.csv'
DELIMITER ','
CSV HEADER;
