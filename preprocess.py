import pandas as pd
import os

# load the file
df = pd.read_csv('4274851.csv')

# STATION Table
# Pull State from NAME column
df['STATE'] = df['NAME'].str.extract(r', ([A-Z]{2}) [A-Z]{2}$')
stations = df[['STATION', 'NAME', 'STATE']].drop_duplicates(subset=['STATION'])
stations.to_csv('stations.csv', index=False)

# WEATHER_VARIABLE Table
vars_data = [
    {'VAR_CODE': 'PRCP', 'VAR_NAME': 'Precipitation'},
    {'VAR_CODE': 'SNWD', 'VAR_NAME': 'Snow Depth'},
    {'VAR_CODE': 'TMAX', 'VAR_NAME': 'Max Temp'},
    {'VAR_CODE': 'TMIN', 'VAR_NAME': 'Min Temp'}
]
