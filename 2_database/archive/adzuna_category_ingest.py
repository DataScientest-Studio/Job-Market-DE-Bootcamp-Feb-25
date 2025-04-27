import psycopg2
import pandas as pd
DB_NAME = "adzunadb"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    """Establish connection to PostgreSQL"""
    try:
        print(f"Connecting to: dbname={DB_NAME}, user={DB_USER}, host={DB_HOST}")
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, options="-c client_encoding=UTF8"
        )
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

def load_csv(file_path):
    """Load job categories from the CSV into a pandas DataFrame"""
    try:
        # Try reading the file with latin1 encoding
        df = pd.read_csv(file_path, encoding="utf-8", header=0)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def insert_job_categories(df):
    """Insert job categories into the database dynamically"""
    conn = connect_db()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        # Define the insert query
        insert_query = """
            INSERT INTO categories (tag, class, label)
            VALUES (%s, %s, %s);
        """
        
        # Prepare job data
        category_data = [
            (
                row["tag"],  # Using the "categoryid" column from CSV
                row["__CLASS__"],  # Using the "categorytag" column from CSV
                row["label"]  # Using the "countrylanguagecategorytag" column from CSV
            )
            for _, row in df.iterrows()
        ]
        # Bulk insert the data
        cursor.executemany(insert_query, category_data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted.")
    except Exception as e:
        print(f"Error during insert: {e}")
    finally:
        cursor.close()
        conn.close()


# Main execution
csv_file_path = r"C:\Users\Kris\DE_DataScientest\Job-Market-DE-Bootcamp-Feb-25\data_collection\output_files\adzuna_category_utf.csv"
df = load_csv(csv_file_path)
if df is not None:
    insert_job_categories(df)
else:
    print("Error: No data loaded from the CSV.")

