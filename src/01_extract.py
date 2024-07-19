import pandas as pd
import numpy as np
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
from bs4 import BeautifulSoup
import sqlite3

#------------------------
# Download data from Kaggle
#------------------------

#set API credentials
api = KaggleApi()
api.authenticate()
dataset_name = 'nilaychauhan/world-bank-datasets'
download_path = '../artifacts/raw'
#check if the file already exists
if not os.path.exists(download_path):
    api.dataset_download_files(dataset_name, path=download_path)
    print("Download completed.")
else:
    print("The file already exists.")

#------------------------
# Extract data from csv
#------------------------

# extract the downloaded zip file
zip_file_path = '../artifacts/raw/world-bank-datasets.zip'
extract_path = '../artifacts/raw'

if not os.path.exists(extract_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
else:
    print("The file already exists.")

# import the projects_data.csv file
df = pd.read_csv('../artifacts/raw/projects_data.csv')
# check number of null
print(df.isnull().sum())
# output shape of the dataframe
print(df.shape)

#read population data
df_population = pd.read_csv('../artifacts/raw/population_data.csv') # might error
# check number error line
f = open('../artifacts/raw/population_data.csv')
for i in range(10):
    line = f.readline()
    print('line:', i, line)
f.close()
# we knew that the error line are between 1-4, so we will skip 4 rows
df_population = pd.read_csv('../artifacts/raw/population_data.csv', skiprows=4)
#check number of null
print(df_population.isnull().sum())
df_population.isnull().sum(axis=1)
#Drop collumn Unnamed: 62
df_population = df_population.drop('Unnamed: 62', axis=1)

#------------------------
#Extract from JSON to XML
#------------------------

def print_lines(n, file_name):
    f = open(file_name)
    for i in range(n):
        print(f.readline())
    f.close()

print_lines(1, '../artifacts/raw/population_data.json')

# Read in the population_data.json file using pandas's 
# read_json method. Don't forget to specific the orient option
# store the results in df_json
df_json = pd.read_json('../artifacts/raw/population_data.json', orient='records')
df_json.head()

# Or we can read JSON using json library
import json
with open('../artifacts/raw/population_data.json') as f:
    json_data = json.load(f)

print(json_data[0])
print('\n')
print(json_data[0]['Country Name'])
print(json_data[0]['Country Code'])

#---------------------------------
# Extract XML
#---------------------------------
#!pip install lxml html5lib
print_lines(15, '../artifacts/raw/population_data.xml')

with open('../artifacts/raw/population_data.xml') as fp:
    soup = BeautifulSoup(fp, "html.parser")

# output the first 5 records in the xml file
# this is an example of how to navigate the XML document with BeautifulSoup

i = 0
# use the find_all method to get all record tags in the document
for record in soup.find_all('record'):
    # use the find_all method to get all fields in each record
    i += 1
    for record in record.find_all('field'):
        print(record['name'], ': ' , record.text)
    print()
    if i == 5:
        break


#---------------------------------
# Extract data from SQL Databases
#---------------------------------

#Connect to databases
connect = sqlite3.connect('../artifacts/raw/population_data.db')
#run a query
pd.read_sql('SELECT * FROM population_data', connect)
pd.read_sql('SELECT "Country_Name", "Country_Code", "1960" FROM population_data', connect)
