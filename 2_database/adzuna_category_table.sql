-----------------UTF Cleaned--------------------
-- Drop Table if perviously created
DROP TABLE IF EXISTS categories;
-- Create Table
CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    tag TEXT NOT NULL,
    api_class TEXT NOT NULL,
    label TEXT NOT NULL
);

--categories: table name in adzunadb
COPY categories(id,tag,api_class,label)
FROM '/tmp/adzuna_category.csv'
DELIMITER ','
CSV HEADER;
