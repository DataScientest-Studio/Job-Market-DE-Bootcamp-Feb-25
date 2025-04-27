import requests
import time
#import json
import os
from dotenv import load_dotenv
import csv

# Load API credentials
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")

# API Base URL
BASE_URL = "http://api.adzuna.com/v1/api/jobs/de/search/"

# Configuration
RESULTS_PER_PAGE = 100
MAX_PAGES = 500  # Reduce max pages to a reasonable number
CATEGORY_TAG = "it-jobs"
MAX_RETRIES = 3  # Number of retries per request
RETRY_DELAY = 5  # Seconds to wait before retrying


def fetch_jobs_by_category(category_tag):
    """Fetch job listings for a given category across multiple pages."""
    all_jobs = []
    
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
                        all_jobs.extend(data["results"])
                    else:
                        print(f"No more results found at page {page}. Stopping.")
                        return all_jobs  # Stop fetching if no more results
                
                    time.sleep(1)  # Respect API rate limits
                    break  # Exit retry loop on success
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
                print(f"Request failed on page {page}, attempt {retries + 1}: {e}")
                time.sleep(RETRY_DELAY)  # Wait before retrying
            
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

# Output file name
output_filename = "data_collection/api_output_files/adzuna_ads.csv"

# Save to CSV file
with open(output_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "company", "category", "location", "created", "salary_min", "salary_max", "contract_type"])
    writer.writeheader()  # Write the header row
    writer.writerows(extracted_jobs)  # Write job data rows

print(f"Data saved to {output_filename}")



'''
#  Output as json
final_output = {
    "category": "IT Jobs",
    "total_jobs": len(extracted_jobs),
    "job_titles": sorted(set(job["title"] for job in extracted_jobs)),
    "job_listings": extracted_jobs
}

print(json.dumps(final_output, indent=4))

# Save to JSON file
with open("adzuna_ads_itjobs2.json", "w") as f:
    json.dump(final_output, f, indent=4)
'''