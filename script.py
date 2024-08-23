import sqlite3

print('---------------------------------------------------------------')
print('----------------- DB Creation And Interaction -----------------')
print('---------------------------------------------------------------')

print('Creating and connecting to DB...')
conn = sqlite3.connect('sample.db')  # Connect to the database (or create it if it doesn't exist)

cursor = conn.cursor()  # Create a cursor object

print('Creating table "data" if not already there...')
# Create a table if not present
cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    zip_code TEXT,
    title TEXT
)
''')

print('Empting table "data"...')
# Delete all rows
cursor.execute('''
DELETE FROM data;
''')

print('Adding new data...')
# Insert data into the table
for params in [('Hadi' , 'Hadi@gmail.com' ,'123','Backend Developer')
               , ('Ramy' , 'Ramy@gmail.com' ,'456','Frontend Developer')
               , ('Samy' , 'Samy@gmail.com' ,'789','IT')
               , ('Hend' , 'Hend@gmail.com' ,'123','HR')
               , ('Amira', 'Amira@gmail.com','456','Backend Developer')
               , ('Emad' , 'Emad@gmail.com' ,'789','Frontend Developer')
               , ('Fathy', 'Fathy@gmail.com','123','IT')
               , ('Fahmy', 'Fahmy@gmail.com','456','HR')
               , ('Omar' , 'Omar@gmail.com' ,'789','Backend Developer')
               , ('Rana' , 'Rana@gmail.com' ,'123','Frontend Developer') ]:
    
    cursor.execute('''
    INSERT INTO data (name,email,zip_code,title) VALUES (?, ?, ?, ?)
    '''
                , params
    )
conn.commit()  # Commit the changes

print('---------------------------------------------------------------')
print('-------------------- Export to CSV and JSON -------------------')
print('---------------------------------------------------------------')

print("Reading data from DB...")
# Query the data
cursor.execute('SELECT id,name,email,zip_code,title FROM data')
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

conn.close()  # Close the connection

# print("Printing retreived data...")
# print(columns)
# print(rows)

## here we have the data (rows) and metadata (columns)


data = [dict(zip(columns, row)) for row in rows]   # Convert rows to a list of dictionaries

import json,csv

print('Writing data to JSON file.')
# Write data to a JSON file
with open('output.json', 'w') as jsonfile:
    json.dump(data, jsonfile, indent=4)

print('Writing data to CSV file with headers.')
# Write data to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(columns)  # Write column headers
    
    csvwriter.writerows(rows) # Write data rows

##############################################################################################

print('---------------------------------------------------------------')
print('--------------- Read Files and Generate Report ----------------')
print('---------------------------------------------------------------')

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('output.csv')

# Read the JSON file into a DataFrame
# df = pd.read_json('output.json')

# # use 'id' as an index
# df.set_index('id', inplace=True)

### needed report 
print(' Report')
print('--------------------------------------------------')
#  - Total number of records retrieved from the database.
#  - Sample records (at least 5 records) from the dataset.
#  - Any additional insights or statistics you find relevant.


# 1. Total number of records.
data_length = len(df)
print('1.Number of records in dataset: ',data_length)

# 2. Sample of 5 rows
print('2.Sample of 5 rows:-')

# sample_count = 5 if 5 < len(df) else len(df)
# print(df.sample(n=sample_count))  # ,random_state=2 

# print(df.sample(n=5,replace=True)) # get 5 rows even if length is less than 5.

# 3. Other insights
print('3.Insights on data:-')

# 3.1   Top used email provider.
print('  3.1 top 3 used email domains with counts:-')
df['domain'] = df['email'].apply(lambda x: x.split('@')[1])  # Extract the domain part from the email
domain_counts = df['domain'].value_counts()  # Count the frequency of each domain
top_3_domains = domain_counts.head(3).add_prefix('    ')  # Get the top 3 most frequent domains
print(top_3_domains.to_string())

# 3.2   3 Most frequently occurring titles.
print('  3.2 top 3 assigned titles with counts:-')
top_3_titles = df['title'].value_counts().head(3).add_prefix('    ')
print(top_3_titles.to_string())

# 3.3   Count of incomplete records.
print('  3.3 Count of incomplete records: ', end='')
incomplete_records = df.isnull().any(axis=1).sum()
print(incomplete_records)
print('--------------------------------------------------')