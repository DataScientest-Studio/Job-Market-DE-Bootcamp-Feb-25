### This file cleans the data from "adzuna_it_jobs.csv"-file for further analysis in a pandas.DataFrame-format

### import relevant packages
import numpy as np
import pandas as pd
from datetime import datetime as dt
import os

###################################################################
###################### clean 'adzuna_ads.csv ##################
###################################################################

### read the csv-data-file
# Get the path where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the absolute path to the CSV file
csv_file_path = os.path.join(script_dir, "..", "api_output_files", "adzuna_ads_all.csv")
csv_output_path = os.path.join(script_dir, "..", "cleanup_output_files", "adzuna_ads_all_clean.csv")

# Read the CSV file
df = pd.read_csv(csv_file_path, sep=',', encoding='utf-8')

### encode German special characters => solved when reading csv-file by encoding
### transform missing values to NaNs => solved when reding csv-file as a dataframe
### rename columns => solved when writing extracted data to the csv-file

### delete duplicates
df.drop_duplicates(keep='first')

### replace NaNs with the value 0 ???
df = df.replace(to_replace = [np.nan], value = [0])

### transform data into the right data type for each column
### atomize dates => better option: define as type date
df['title'] = df['title'].astype('string')
df['company'] = df['company'].astype('string')
df['category'] = df['category'].astype('string')
df['location'] = df['location'].astype('string')
df['created'] = pd.to_datetime(df['created'], format='ISO8601')
df['salary_min'] = pd.to_numeric(df['salary_min'])
df['salary_max'] = pd.to_numeric(df['salary_max'])
df['contract_type'] = df['contract_type'].astype('string')

change_types = {'salary_min' : 'int',
                'salary_max' : 'int'}
df = df.astype(change_types)

### set index
df.index = list(range(0,len(df),1))

### delete "garbage"
df= df[-(df['company'].str.contains('persona service AG & Co. KG'))]

### eliminate 'outliers'
df = df.drop(df[(df.salary_min > 0) & (df.salary_min < 10000)].index)
df = df.drop(df[(df.salary_max > 0) & (df.salary_max < 10000)].index)

### reset index
df.index = list(range(0,len(df),1))
df.index.name = 'job_offer_id'

### dissolve'contract_type' for further computation
df['fixed_contract'] = np.nan
df['limited_contract'] = np.nan
df['contract_undefined'] = np.nan

df['fixed_contract'] = df['fixed_contract'].mask(df.contract_type == 'permanent', True).mask(df.contract_type != 'permanent', False).replace({True : 1, False : 0})
df['limited_contract'] = df['limited_contract'].mask(df.contract_type == 'contract', True).mask(df.contract_type != 'contract', False).replace({True : 1, False : 0})
df['contract_undefined'] = df['contract_undefined'].mask(df.contract_type == '0', True).mask(df.contract_type != '0', False).replace({True : 1, False : 0})

### check df
print(df.head())

### save df to csv-file
df.to_csv(csv_output_path, sep=',', encoding='utf-8', index=True)