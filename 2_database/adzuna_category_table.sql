-----------------UTF Cleaned--------------------
-- Drop Table if perviously created
DROP TABLE IF EXISTS categories;
-- Create Table
CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    tag TEXT NOT NULL,
    label TEXT NOT NULL

);

-- in separate terminal execute:
-- docker cp "..\Job-Market-DE-Bootcamp-Feb-25\1_data_collection\cleanup_output_files\adzuna_category_clean.csv" postgres_db:/tmp/

--categories: table name in adzunadb
COPY categories(id, tag, label)
FROM '/tmp/adzuna_category_clean.csv'
DELIMITER ','
CSV HEADER;
