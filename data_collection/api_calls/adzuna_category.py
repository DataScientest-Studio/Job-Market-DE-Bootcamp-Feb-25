from dotenv import load_dotenv
import os
import requests
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# DE market, adjust for GB if needed
API_URL = "https://api.adzuna.com/v1/api/jobs/de/categories"
API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")

def get_all_labels():
    params = {
        "app_id": API_ID,
        "app_key": API_KEY
    }
    response = requests.get(API_URL, params=params)
    return response.json() if response.status_code == 200 else {}

all_labels = get_all_labels()

# Convert to DataFrame
df = pd.DataFrame(all_labels.get("results", []))

# Save to CSV
df.to_csv("adzuna_category.csv", index=False)

# Display the DataFrame
print(df)
print("Data saved to adzuna_category.csv")