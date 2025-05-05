import pandas as pd
import re
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "..", "api_output_files", "adzuna_category.csv")


def clean_text(text):
    """Replace hyphens with spaces, remove all other special characters, and trim spaces."""
    if pd.isna(text):  # Handle NaN values
        return ""
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text)  # Remove special characters except hyphens
    text = text.replace("-", " ")  # Replace hyphens with spaces
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

#Load CSV File and Process Data
def load_csv(file_path):
    """Load job categories from the CSV into a pandas DataFrame"""
    try:
        
        df = pd.read_csv(file_path, sep = ',', encoding = 'utf-8')
        df.drop(columns=['__CLASS__'], axis=1, inplace=True)  # Modify df in 
        
        # Clean 'tag' and 'label' columns
        df['tag'] = df['tag'].astype(str).apply(clean_text)
        df['label'] = df['label'].astype(str).apply(clean_text)
        
        # Ensure index is used as an identifier
        # df.insert(0, "category_id", df.index)  # Assign index to ads_id column
        
        # Clean or rename the columns if needed (though they seem correct for your table)
        df.rename(columns={
            "category_id": "id",
            'tag': 'tag',
            'label': 'label'
        }, inplace=True)
        
        # Convert DataFrame to list of dictionaries (each row becomes a dictionary)
        category_list = df.to_dict(orient='records')

        return category_list
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

df = pd.DataFrame(load_csv(input_path))
df.to_csv(os.path.join(script_dir, "..", "cleanup_output_files", "adzuna_category_clean.csv"))
#print(df)