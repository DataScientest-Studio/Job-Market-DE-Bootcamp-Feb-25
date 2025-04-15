# Job-Market-DE-Bootcamp-Feb-25
This is our folder structure, with a short decription of its content:
```
Job-Market-DE-Bootcamp-Feb-25/
├── data_collection/
│   └── api_calls/
│       └── py scripts with adzuna API calls to extract data
│   └── api_output_files/
│       └── raw csv files from api_calls
│   └── cleanup_output/
│       └── py scripts to clean the raw csvs from api_output_files
│   └── cleanup_scripts/
│       └── csv scripts to insert into database
├── data_consumption/
│   └── streamlit_viz/
        └── streamlit py script to vizualize data
└── database/
    └── ingest py scripts, sql queries to create tables and docker-compose.yaml    
```
## Project Progress
### Data Collection:
Using the adzuna API we are able to collect information on:
- salary
- job ad postings
- job categories
We further filter it down to the German market for IT jobs.
The Adzuna API restricts requests made daily, so we decide to pull the max on jobs we can on one start date and enrich it with daily job posting data.

### Data Consumption
For our Data Visualization we chose Streamlit.

### Database
We chose to use PostgreSQL as our database, because we structure our data into csv and dataframes which makes it easy to ingest into the tabular form the database presets.
