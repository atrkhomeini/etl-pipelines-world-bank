import pandas as pd
import numpy as np
from encodings.aliases import aliases
import matplotlib.pyplot as plt
%matplotlib inline

#-------------------------------------
# Combining Data
#-------------------------------------

# read population data
f = open('../artifacts/raw/rural_population_percent.csv')
for i in range(10):
    line = f.readline()
    print('line:', i, line)
f.close()

df_rural = pd.read_csv('../artifacts/raw/rural_population_percent.csv', skiprows=4)
df_rural.head()

# read electricity data
f= open('../artifacts/raw/electricity_access_percent.csv')
for i in range(10):
    line = f.readline()
    print('line:', i, line)
f.close()

df_electricity = pd.read_csv('../artifacts/raw/electricity_access_percent.csv', skiprows=4) 
df_electricity.head()

#remove unnamed column
df_rural = df_rural.drop(['Unnamed: 62'], axis=1)
df_electricity = df_electricity.drop(['Unnamed: 62'], axis=1)


df = pd.concat([df_rural, df_electricity])
df.head()


#-------------------------------------
# Cleaning Data
#-------------------------------------

df_indic = pd.read_csv('../artifacts/raw/population_data.csv', skiprows=4)
df_indic = df_indic.drop(['Unnamed: 62'], axis=1)

df_projects = pd.read_csv('../artifacts/raw/projects_data.csv')
df_projects = df_projects.drop(['Unnamed: 56'], axis=1)

df_indic[['Country Name', 'Country Code']].drop_duplicates()

df_projects['countryname'].unique()

# 'Kingdom of Spain;Kingdom of Spain'
# 'New Zealand;New Zealand'

df_projects['Official Country Name'] = df_projects['countryname'].str.split(';').str.get(0)

from pycountry import countries

countries.get(name='Spain')
countries.lookup('Kingdom of Spain')

#set up libraries
from collections import defaultdict
country_unknown = []
project_country_abbrev_dict = defaultdict(str)

#iterate over the unique country names in the projects data
#create a dictionary that mapping the country name into the alpha_3 ISO code
for country in df_projects['Official Country Name'].drop_duplicates().sort_values():
    try:
        #look up the country name in the pycountry library
        #store the alpha_3 ISO code in the dictionary
        project_country_abbrev_dict[country] = countries.lookup(country).alpha_3
    except:
        # If the country name is not in the pycountry library, then print out the country name
        # And store the results in the country_not_found list
        print(country, ' not found')
        country_unknown.append(country)

# Run this cell to iterate through the country_not_found list and check if the country name is in the df_indicator data set
indicator_countries = df_indic[['Country Name', 'Country Code']].drop_duplicates().sort_values(by='Country Name')

for country in country_unknown:
    if country in indicator_countries['Country Name'].tolist():
        print(country)

country_not_found_mapping = {'Co-operative Republic of Guyana': 'GUY',
             'Commonwealth of Australia':'AUS',
             'Democratic Republic of Sao Tome and Prin':'STP',
             'Democratic Republic of the Congo':'COD',
             'Democratic Socialist Republic of Sri Lan':'LKA',
             'East Asia and Pacific':'EAS',
             'Europe and Central Asia': 'ECS',
             'Islamic  Republic of Afghanistan':'AFG',
             'Latin America':'LCN',
              'Caribbean':'LCN',
             'Macedonia':'MKD',
             'Middle East and North Africa':'MEA',
             'Oriental Republic of Uruguay':'URY',
             'Republic of Congo':'COG',
             "Republic of Cote d'Ivoire":'CIV',
             'Republic of Korea':'KOR',
             'Republic of Niger':'NER',
             'Republic of Kosovo':'XKX',
             'Republic of Rwanda':'RWA',
              'Republic of The Gambia':'GMB',
              'Republic of Togo':'TGO',
              'Republic of the Union of Myanmar':'MMR',
              'Republica Bolivariana de Venezuela':'VEN',
              'Sint Maarten':'SXM',
              "Socialist People's Libyan Arab Jamahiriy":'LBY',
              'Socialist Republic of Vietnam':'VNM',
              'Somali Democratic Republic':'SOM',
              'South Asia':'SAS',
              'St. Kitts and Nevis':'KNA',
              'St. Lucia':'LCA',
              'St. Vincent and the Grenadines':'VCT',
              'State of Eritrea':'ERI',
              'The Independent State of Papua New Guine':'PNG',
              'West Bank and Gaza':'PSE',
              'World':'WLD'}

# Update the project_country_abbrev_dict with the country_not_found_mapping dictionary
# HINT: This is relatively straightforward. Python dictionaries have a method called update(), which essentially
# appends a dictionary to another dictionary

project_country_abbrev_dict.update(country_not_found_mapping)

# Use the project_country_abbrev_dict and the df_projects['Country Name'] column to make a new column
# of the alpha-3 country codes. This new column should be called 'Country Code'.

# HINT: Use the apply method and a lambda function
# HINT: The lambda function will use the project_country_abbrev_dict that maps the country name to the ISO code
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.apply.html

df_projects['Country Code'] = df_projects['Official Country Name'].apply(lambda x: project_country_abbrev_dict[x])
# Run this code cell to see which projects in the df_projects data frame still have no country code abbreviation.
# In other words, these projects do not have a matching population value in the df_indicator data frame.
df_projects[df_projects['Country Code'] == '']

#-------------------------------------
# Data Types
#-------------------------------------

df_indic.dtypes
# Calculate the population sum by year for Canada,
#       the United States, and Mexico.

# the keepcol variable makes a list of the column names to keep. You can use this if you'd like
keepcol = ['Country Name']
for i in range(1960, 2018, 1):
    keepcol.append(str(i))

# In the df_nafta variable, store a data frame that only contains the rows for 
#      Canada, United States, and Mexico.
df_nafta = df_indic[(df_indic['Country Name'] == 'Canada') | 
             (df_indic['Country Name'] == 'United States') | 
            (df_indic['Country Name'] == 'Mexico')].iloc[:,]


# Calculate the sum of the values in each column in order to find the total population by year.
# You can use the keepcol variable if you want to control which columns get outputted
df_nafta.sum(axis=0)[keepcol]

df_projects[['totalamt', 'lendprojectcost']].head()

# Convert the totalamt column from a string to a float and save the results back into the totalamt column

# Step 1: Remove the commas from the 'totalamt' column
# HINT: https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.Series.str.replace.html

# Step 2: Convert the 'totalamt' column from an object data type (ie string) to an integer data type.
# HINT: https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.to_numeric.html

df_projects['totalamt'] = pd.to_numeric(df_projects['totalamt'].str.replace(',',""))

#-------------------------------------
# Parsing Dates
#-------------------------------------
df_projects.head(15)[['boardapprovaldate', 'board_approval_month', 'closingdate']]

df_projects['boardapprovaldate'] = pd.to_datetime(df_projects['boardapprovaldate'])
df_projects['closingdate'] = pd.to_datetime(df_projects['closingdate'])


df_projects['approvalyear'] = df_projects['boardapprovaldate'].dt.year
df_projects['approvalday'] = df_projects['boardapprovaldate'].dt.day
df_projects['approvalweekday'] = df_projects['boardapprovaldate'].dt.weekday
df_projects['closingyear'] = df_projects['closingdate'].dt.year
df_projects['closingday'] = df_projects['closingdate'].dt.day
df_projects['closingweekday'] = df_projects['closingdate'].dt.weekday

def save_file(file_path):
    if os.path.exists(file_path):
        print("File already exists!")
    else:
        df_projects.to_csv(file_path, index=False)
        print("File saved successfully!")

save_file('../artifacts/transform/df_projects_parsing_dates.csv')
#-------------------------------------
# Encoding Data
#-------------------------------------

alias_values = set(aliases.values())

for encoding in set(aliases.values()):
    try:
        df_mystery=pd.read_csv('../artifacts/raw/mystery.csv', encoding=encoding)
        print('successful', encoding)
    except:
        pass

import chardet
with open ('../artifacts/raw/mystery.csv', 'rb') as file:
    print(chardet.detect(file.read()))


#-------------------------------------
# Imputing Data
#-------------------------------------

df_gdp = pd.read_csv('../artifacts/raw/gdp_data.csv', skiprows=4)
df_gdp = df_gdp.drop(['Unnamed: 62'], axis=1)

df_gdp.isnull().sum()

#Plot the missing values in the df_gdp data frame

# put the data set into long form instead of wide
df_melt = pd.melt(df_gdp, id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], var_name='year', value_name='GDP')

# convert year to a date time
df_melt['year'] = pd.to_datetime(df_melt['year'])

def plot_results(column_name):
    # plot the results for Afghanistan, Albania, and Honduras
    fig, ax = plt.subplots(figsize=(8,6))

    df_melt[(df_melt['Country Name'] == 'Indonesia') | 
            (df_melt['Country Name'] == 'South Korea') | 
            (df_melt['Country Name'] == 'Japan')].groupby('Country Name').plot('year', column_name, legend=True, ax=ax)
    ax.legend(labels=['Indonesia', 'South Korea', 'Japan'])
    
plot_results('GDP')

#-------------------------------------
# Dupplicate Data
#-------------------------------------
df_project = pd.read_csv('../artifacts/transform/df_projects_parsing_dates.csv', dtype=str)
df_project['totalamt'] = pd.to_numeric(df_project['totalamt'].str.replace(',',""))
df_project['countryname'] = df_project['countryname'].str.split(';', expand = True)[0]
df_project['boardapprovaldate'] = pd.to_datetime(df_project['boardapprovaldate'])
# filter the data frame for projects over 1 billion dollars

# count the number of unique countries in the results
df_project[df_project['totalamt'] > 1000000000]['countryname'].nunique()

#-------------------------------------
# Dummy Variables
#-------------------------------------

sector = df_project.copy()
sector = sector[['project_name', 'lendinginstr', 'sector1', 'sector2', 'sector3', 'sector4', 'sector5', 'sector',
          'mjsector1', 'mjsector2', 'mjsector3', 'mjsector4', 'mjsector5',
          'mjsector', 'theme1', 'theme2', 'theme3', 'theme4', 'theme5', 'theme ',
          'goal', 'financier', 'mjtheme1name', 'mjtheme2name', 'mjtheme3name',
          'mjtheme4name', 'mjtheme5name']]

# output percentage of values that are missing
100 * sector.isnull().sum() / sector.shape[0]

# Create a list of the unique values in sector1. Use the sort_values() and unique() pandas methods. 
# And then convert those results into a Python list
uniquesectors1 = sector['sector1'].sort_values().unique()
uniquesectors1

print('Number of unique sectors:', len(uniquesectors1))

# TODO: In the sector1 variable, replace the string '!$10' with nan
# HINT: you can use the pandas replace() method and numpy.nan
sector['sector1'] = sector['sector1'].replace('!$!0', np.nan)

# TODO: In the sector1 variable, remove the last 10 or 11 characters from the sector1 variable.
# HINT: There is more than one way to do this including the replace method
# HINT: You can use a regex expression '!.+'
# That regex expression looks for a string with an exclamation
# point followed by one or more characters

sector['sector1'] = sector['sector1'].replace('!.+', '', regex=True)

# TODO: Remove the string '(Historic)' from the sector1 variable
# HINT: You can use the replace method
sector['sector1'] = sector['sector1'].replace('^(\(Historic\))', '', regex=True)

print('Number of unique sectors after cleaning:', len(list(sector['sector1'].unique())))
print('Percentage of null values after cleaning:', 100 * sector['sector1'].isnull().sum() / sector['sector1'].shape[0])

dummies = pd.DataFrame(pd.get_dummies(sector['sector1']))

#  Filter the projects data for the totalamt, the year from boardapprovaldate, and the dummy variables
df_projects['year'] = df_projects['boardapprovaldate'].dt.year
df_dummy = df_projects[['totalamt','year']]
df_final = pd.concat([df_dummy, dummies], axis=1)

df_final.head()

#-------------------------------------
# Finding Outliers
#-------------------------------------



