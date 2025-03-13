from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# DE market, adjust for GB if needed
API_URL = "https://api.adzuna.com/v1/api/jobs/de/categories?app_id=9585c5e8&app_key=482caa"
API_KEY = os.getenv('API_KEY')
API_ID = os.getenv('API_ID')

def get_all_labels():
    url = API_URL
    params = {
        "app_id": API_ID,
        "app_key": API_KEY
    }

    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {}

all_labels = get_all_labels()
print(all_labels)

#---------------------------------------------------------------------------------
import pandas as pd

# Convert to DataFrame
df = pd.DataFrame(all_labels["results"])

# Display the DataFrame
print(df)