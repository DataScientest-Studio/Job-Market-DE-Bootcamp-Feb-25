import psycopg2
import os
from psycopg2 import sql
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
        print(f"Connecting to: dbname={DB_NAME}, user={DB_USER}, host={DB_HOST}")
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, options="-c client_encoding=UTF8" # enforcing UTF-8 during connection
        )
        conn.set_client_encoding('UTF8')

        # Debug PostgreSQL encoding
        cursor = conn.cursor()
        cursor.execute("SHOW server_encoding;")
        print("Server Encoding:", cursor.fetchone()[0])  # Expect "UTF8"

        cursor.execute("SHOW client_encoding;")
        print("Client Encoding:", cursor.fetchone()[0])  # Expect "UTF8"

        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def insert_job_categories(categories):
    """Insert job categories into the database dynamically"""
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        
        insert_query = """
            INSERT INTO adzuna_job_categories (index_id, tag, __class__, label)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (tag, __class__, label) DO NOTHING;
        """

        # Prepare job data, including incremental index
        category_data = [
            (
                idx + 1,  # Incremental index (starts at 1)
                category["tag"],
                category["__class__"],
                category["label"]
            )
            for idx, category in enumerate(categories)
        ]

        cursor.executemany(insert_query, category_data)  # Bulk insert for efficiency
        conn.commit()

        print(f"{cursor.rowcount} records inserted.")
    except Exception as e:
        print(f"Error during insert: {e}")
    finally:
        cursor.close()
        conn.close()

def load_csv(file_path):
    """Load job categories from the CSV into a pandas DataFrame"""
    try:
        
        df = pd.read_csv(file_path, sep = ',', encoding = 'utf-8')
        
        # Ensure index is used as an identifier
        df.insert(0, "category_id", df.index)  # Assign index to ads_id column
        
        # Clean or rename the columns if needed (though they seem correct for your table)
        df.rename(columns={
            "category_id": "category_id",
            'tag': 'category_tag',
            '__class__': 'api_class',
            'label': 'country_language_category_tag'
        }, inplace=True)
        
        # Convert DataFrame to list of dictionaries (each row becomes a dictionary)
        category_list = df.to_dict(orient='records')

        return category_list
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

# Load data from the CSV
csv_file_path = "../data_collection/output_files/adzuna_category.csv"
extracted_categories = load_csv(csv_file_path)

for category in extracted_categories: # To Catch Encoding Errors
    try:
        str(category).encode("utf-8")  # Try encoding
    except UnicodeEncodeError as e:
        print(f"Encoding error in row: {category}, Error: {e}")

# Insert job categories data into the database
if extracted_categories:
    insert_job_categories(extracted_categories)
else:
    print("No category data to insert.")
