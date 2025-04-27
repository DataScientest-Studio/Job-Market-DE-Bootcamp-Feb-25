###################################################################
###################### clean 'adzuna_category.csv' ################
###################################################################

### read the csv-data-file
df = pd.read_csv('adzuna_category.csv', sep = ',', encoding = 'utf-8')

### transform data into the right data type for each column
df['label'] = df['label'].astype('string')
df['tag'] = df['tag'].astype('string')

### drop __CLASS__ column
df = df.drop('__CLASS__', axis = 1)

### check df
# print(df)

### save df to csv-file
# df.to_csv('adzuna_category_cleaned.csv', sep=',', encoding='utf-8', index=False)
