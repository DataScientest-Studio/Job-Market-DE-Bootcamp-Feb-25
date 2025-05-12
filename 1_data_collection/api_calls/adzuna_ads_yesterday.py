import requests 
import time
import json
import csv
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
from pathlib import Path
# Load API credentials
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")

# API Base URL
BASE_URL = "http://api.adzuna.com/v1/api/jobs/de/search/"

# Configuration
RESULTS_PER_PAGE = 100
MAX_PAGES = 150  # Reduce max pages to a reasonable number
CATEGORY_TAG = "it-jobs"
MAX_RETRIES = 3  # Number of retries per request
RETRY_DELAY = 5  # Seconds to wait before retrying

def fetch_jobs_by_category(category_tag):
    """Fetch job listings for a given category across multiple pages with better error handling."""
    all_jobs = []
    yesterday = (datetime.utcnow() - timedelta(days=1)).date()

    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE_URL}{page}"
        params = {
            "app_id": API_ID,
            "app_key": API_KEY,
            "results_per_page": RESULTS_PER_PAGE,
            "category": category_tag,
            "content-type": "application/json"
        }

        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if "results" in data and data["results"]:
                        for job in data["results"]:
                            created_date = datetime.strptime(job["created"].split("T")[0], "%Y-%m-%d").date()
                            if created_date == yesterday:
                                all_jobs.append(job)
                    else:
                        print(f"No more results at page {page}. Stopping.")
                        return all_jobs  # Stop fetching if no more results

                    time.sleep(random.uniform(2, 5))  # Add randomness to avoid detection
                    break  # Exit retry loop on success

                elif response.status_code in [502, 503, 504]:  # Server issues
                    wait_time = RETRY_DELAY * (2 ** retries)  # Exponential backoff
                    print(f"Server error {response.status_code}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

                elif response.status_code == 403:
                    print("Access Denied: Check API Key and Permissions.")
                    return all_jobs
                
                elif response.status_code == 429:
                    print("Rate Limit Exceeded: Pausing before retrying...")
                    time.sleep(RETRY_DELAY * 2)  # Wait longer before retrying
                
                else:
                    print(f"API Error {response.status_code}: {response.text}")
                    time.sleep(RETRY_DELAY)
                
            except requests.exceptions.RequestException as e:
                wait_time = RETRY_DELAY * (2 ** retries)  # Exponential backoff
                print(f"Request failed on page {page}, attempt {retries + 1}: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  
            
            retries += 1

        if retries == MAX_RETRIES:
            print(f"Skipping page {page} after multiple failures.")
            break  # Stop fetching to prevent excessive failures

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

# Fetch jobs with improved error handling
jobs = fetch_jobs_by_category(CATEGORY_TAG)

# Extract job data
extracted_jobs = [extract_job_data(job) for job in jobs]

# Calculate yesterday's actual date
yesterday_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

# Output file name
output_dir = Path("../api_output_files/yesterdays_ads_files")
output_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
output_filename = output_dir / f"adzuna_ads_{yesterday_date}.csv"

# Save to CSV file
with open(output_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "company", "category", "location", "created", "salary_min", "salary_max", "contract_type"])
    writer.writeheader()  # Write the header row
    writer.writerows(extracted_jobs)  # Write job data rows

print(f"Data saved to {output_filename}")


'''
# json output:
# Calculate yesterday's actual date
yesterday_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

# Output
final_output = {
    "category": "IT Jobs",
    "date": yesterday_date,
    "total_jobs": len(extracted_jobs),
    "job_titles": sorted(set(job["title"] for job in extracted_jobs)),
    "job_listings": extracted_jobs
}

print(json.dumps(final_output, indent=4))

# Save to JSON file
with open(f"adzuna_ads_itjobs_{yesterday_date}.json", "w") as f:
    json.dump(final_output, f, indent=4)
'''