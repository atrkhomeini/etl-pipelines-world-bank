import pandas as pd
import numpy as np
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

api = KaggleApi()
api.authenticate()
api.dataset_download_files('nilaychauhan/world-bank-datasets', path='../artifacts/raw')
#------------------------
# Extract data from csv
#------------------------

# extract the downloaded zip file
with zipfile.ZipFile('../artifacts/raw/world-bank-datasets.zip', 'r') as zip_ref:
    zip_ref.extractall('../artifacts/raw')

# import the projects_data.csv file
df = pd.read_csv('../artifacts/raw/projects_data.csv')

