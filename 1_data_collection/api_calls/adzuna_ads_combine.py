import pandas as pd
import os
from glob import glob

# Base this on the script's location, not the working directory
script_dir = os.path.dirname(os.path.abspath(__file__))

base_path = os.path.join(script_dir, "..", "api_output_files")
yesterday_path = os.path.join(base_path, "yesterdays_ads_files")
daily_files_pattern = os.path.join(yesterday_path, "adzuna_ads_*.csv")
main_csv_path = os.path.join(base_path, "adzuna_ads.csv")
may_file_path = os.path.join(base_path, "adzuna_ads_may.csv")  # <--- New file
output_path = os.path.join(base_path, "adzuna_ads_all.csv")    # <--- Full path corrected

# Collect daily CSVs
daily_files = glob(daily_files_pattern)
print(f"Found {len(daily_files)} daily files.")

# Read daily CSVs
daily_dfs = [pd.read_csv(f) for f in daily_files]

# Add May file if it exists
if os.path.exists(may_file_path):
    may_df = pd.read_csv(may_file_path)
    print("adzuna_ads_may.csv found and loaded.")
    daily_dfs.append(may_df)
else:
    print("adzuna_ads_may.csv not found.")

# Read main adzuna_ads.csv if it exists
if os.path.exists(main_csv_path):
    main_df = pd.read_csv(main_csv_path)
    print("Main adzuna_ads.csv found and loaded.")
else:
    print("Main adzuna_ads.csv not found.")
    main_df = pd.DataFrame(columns=[
        "title", "company", "category", "location", 
        "created", "salary_min", "salary_max", "contract_type"
    ])

# Combine everything
all_dfs = [main_df] + daily_dfs if daily_dfs else [main_df]
final_df = pd.concat(all_dfs, ignore_index=True).drop_duplicates()

# Ensure output folder exists
os.makedirs(base_path, exist_ok=True)

# Save combined result
final_df.to_csv(output_path, index=False)
print(f"Saved combined data to: {output_path} ({len(final_df)} rows)")
