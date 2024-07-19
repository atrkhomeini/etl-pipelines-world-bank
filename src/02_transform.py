import pandas as pd
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