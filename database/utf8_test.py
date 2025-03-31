'''
import pandas as pd
df = pd.read_csv("../data_collection/output_files/adzuna_category.csv", sep = ',', encoding = 'utf-8')
#print(df.head(30).to_string())

for col in df.columns:
    for i, val in enumerate(df[col]):
        try:
            val.encode('utf-8')
        except UnicodeEncodeError:
            print(f"Problematic character at row {i}, column '{col}': {val}")
'''          
import chardet

with open("../data_collection/output_files/adzuna_category.csv", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    print(result)