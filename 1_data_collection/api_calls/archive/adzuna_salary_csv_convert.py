import pandas as pd

# Load the Excel file
df = pd.read_excel("data_collection/output_files/adzuna_salary_24M.xlsx", engine="openpyxl")

# Save it as a CSV file (without the index column)
df.to_csv("data_collection/output_files/adzuna_salary_24M.csv", index=False)

print("Excel file converted to CSV successfully!")