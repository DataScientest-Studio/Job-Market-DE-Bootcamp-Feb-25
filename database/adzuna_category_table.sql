CREATE TABLE adzuna_category (
    category_id SERIAL PRIMARY KEY,
    category_tag TEXT NOT NULL,
    api_calss TEXT NOT NULL,
    country_language_category_tag TEXT NOT NULL
);