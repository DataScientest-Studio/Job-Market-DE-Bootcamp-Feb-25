-----------------UTF Cleaned--------------------
-- Drop Table if perviously created
DROP TABLE IF EXISTS categories;
-- Create Table
CREATE TABLE categories(
    index NUMERIC,
    categoryid TEXT NOT NULL,
    categorytag TEXT NOT NULL,
    countrylanguagecategorytag TEXT NOT NULL
);

--categories: table name in adzunadb
COPY categories(index,categoryid,categorytag,countrylanguagecategorytag)
FROM '/tmp/adzuna_category_utf.csv'
DELIMITER ','
CSV HEADER;
