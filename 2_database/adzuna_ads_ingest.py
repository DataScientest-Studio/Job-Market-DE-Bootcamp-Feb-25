import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Database credentials from environment variables
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "localhost"  # Change if needed
DB_PORT = "5432"

def connect_db():
    """Establish connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST, 
            port=DB_PORT
        )
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def insert_jobs(jobs):
    """Insert job listings into the database dynamically"""
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO job_listings (
                job_offer_id, title, company, category, location, created, 
                salary_min, salary_max, contract_type, fixed_contract, limited_contract, contract_undefined
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (title, company, created) DO NOTHING;
        """

        job_data = [
            (
                job["job_offer_id"],   # Index
                job["title"],      
                job["company"],       
                job["category"],   
                job["location"],   
                job["created"],   
                job["salary_min"],     
                job["salary_max"],     
                job["contract_type"],
                job["fixed_contract"],
                job["limited_contract"],
                job["contract_undefined"]
            )
            for job in jobs
        ]

        cursor.executemany(insert_query, job_data)  # Bulk insert for efficiency
        conn.commit()

        print(f"{cursor.rowcount} records inserted.")
    except Exception as e:
        print(f"Error during insert: {e}")
    finally:
        cursor.close()
        conn.close()

def load_csv(file_path):
    """Load job listings from the CSV into a pandas DataFrame"""
    try:
        df = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1', on_bad_lines='warn')
        
        # Ensure index is used as an identifier
        df.insert(0, "ads_id", df.index)  # Assign index to ads_id column

        # Clean or rename the columns to match the database schema
        df.rename(columns={
            'job_offer_id': 'job_offer_id',
            'title': 'jtitle',
            'company': 'company',
            'category': 'category',
            'location': 'location',
            'created': 'created',
            'salary_min': 'salary_min',
            'salary_max': 'salary_max',
            'contract_type': 'contract_type',
            'fixed_contract': 'fixed_contract',
            'limited_contract': 'limited_contract',
            'contract_undefined': 'contract_undefined'
        }, inplace=True)
        
        # Convert DataFrame to list of dictionaries (each row becomes a dictionary)
        job_listings = df.to_dict(orient='records')

        return job_listings
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

# Load data from the CSV
csv_file_path = "../cleanup_output_files/adzuna_ads_all_clean.csv"
extracted_jobs = load_csv(csv_file_path)

# Insert job data into the database
if extracted_jobs:
    insert_jobs(extracted_jobs)
else:
    print("No job data to insert.")

