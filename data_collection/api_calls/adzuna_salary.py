from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# DE market, adjust for GB if needed
API_URL = "https://api.adzuna.com/v1/api/jobs/de/history"
API_KEY = os.getenv('API_KEY')
API_ID = os.getenv('API_ID')

# Titles and City List adjustable | Non exhaustive list
job_titles = ["Engineer", "Analyst", "Data Engineer", "Data Analyst", "Software Developer"]
cities = ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"]

def get_jobs(job_title, city):
    params = {
        "app_id": API_ID,
        "app_key": API_KEY,
        "what": job_title,
        "where": city,
        "months": 24  # Keeping the historical data limit
    }
    response = requests.get(API_URL, params=params)
    return response.json() if response.status_code == 200 else {}

all_jobs = {} #dictionary
for job in job_titles:
    for city in cities:
        key = f"{job} in {city}"
        all_jobs[key] = get_jobs(job, city)

print(all_jobs) #dictionary

#---------------------------------------------------------------------------------
import pandas as pd

salary_data = []
for key, value in all_jobs.items():
    job_title, city = key.split(" in ")
    for month, salary in value.get("month", {}).items():
        salary_data.append([month, city, job_title, salary])

df = pd.DataFrame(salary_data, columns=['Month', 'Location', 'Job Title', 'Salary'])
df = df.sort_values('Month')

print(df)

#df.to_excel('adzuna_salary_call.xlsx')