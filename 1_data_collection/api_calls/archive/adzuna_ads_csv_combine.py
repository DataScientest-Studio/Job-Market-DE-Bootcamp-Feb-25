import pandas as pd

def append_csv_files(file_list, output_file):
    # Read and concatenate all CSV files
    dataframes = [pd.read_csv(file) for file in file_list]
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Save the concatenated dataframe to a new CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"CSV files successfully merged into {output_file}")

if __name__ == "__main__":
    file_list = [
    "../output_files/adzuna_ads_itjobs.csv", 
    "../output_files/adzuna_ads_itjobs2.csv", 
    "../output_files/adzuna_ads_itjobs3.csv"]
    output_file = "../output_files/combined_adzuna_ads_itjobs.csv"
    append_csv_files(file_list, output_file)