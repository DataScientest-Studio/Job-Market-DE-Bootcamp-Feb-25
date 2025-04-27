# Make sure to have pip install python-dotenv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

import requests
import time
import json

# Get your API keys from environment variables
API_KEY = os.getenv('API_KEY')
API_ID = os.getenv('API_ID')

# Base API URL
# DE market, adjust for GB if needed
BASE_URL = "http://api.adzuna.com/v1/api/jobs/de/search/"

# Configuration
RESULTS_PER_PAGE = 10  # Number of results per API call
MAX_PAGES = 12295  # Limit the number of pages to prevent too many requests
CATEGORY_TAG = "it-jobs"  # Adzuna category tag for IT Jobs

def fetch_jobs_by_category(category_tag):
    """Fetch job listings for a given category across multiple pages."""
    all_jobs = []
    
    for page in range(1, MAX_PAGES + 1):  # Iterate through pages
        url = f"{BASE_URL}{page}"
        params = {
            "app_id": API_ID,
            "app_key": API_KEY,
            "results_per_page": RESULTS_PER_PAGE,
            "category": category_tag,  # Search by category
            "content-type": "application/json"
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                all_jobs.extend(data["results"])  # Append jobs from this page
            else:
                break  # Stop if no more results
        else:
            print(f"Error fetching data for category {category_tag} on page {page}")
            break
        
        time.sleep(1)  # Add a delay to avoid being blocked

    return all_jobs

def extract_job_data(job):
    """Extract relevant details from a job listing."""
    return {
        "title": job.get("title"),
        "company": job.get("company", {}).get("display_name", "N/A"),
        "category": job.get("category", {}).get("label", "N/A"),
        "location": job.get("location", {}).get("display_name", "N/A"),
        "created": job.get("created", "N/A"),
        "salary_min": job.get("salary_min", "N/A"),
        "salary_max": job.get("salary_max", "N/A"),
        "contract_type": job.get("contract_type", "N/A"),
    }

# Fetch jobs for the category "IT Jobs"
jobs = fetch_jobs_by_category(CATEGORY_TAG)

# Extract job data
extracted_jobs = [extract_job_data(job) for job in jobs]

# Get unique job titles from the extracted data
job_titles = sorted(set(job["title"] for job in extracted_jobs))

final_output = {
    "category": "IT Jobs",
    "total_jobs": len(extracted_jobs),  # Count total jobs
    "job_titles": sorted(set(job["title"] for job in extracted_jobs)),  # Unique job titles
    "job_listings": extracted_jobs
}

print(json.dumps(final_output, indent=4))

# Save to JSON file
#with open("adzuna_it_jobs.json", "w") as f:
    #json.dump(final_output, f, indent=4)