import pandas as pd

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

for i in range(5, 101):
    vars_data.append({"VAR_CODE": f"V{i:03d}", "VAR_NAME": f"Sensor_{i}"})

pd.DataFrame(vars_data).to_csv("data/variables.csv", index=False)

# OBSERVATION table
obs = df.melt(
    id_vars=["STATION", "DATE"],
    value_vars=["PRCP", "SNWD", "TMAX", "TMIN"],
    var_name="VAR_CODE",
    value_name="VALUE"
).dropna(subset=["VALUE"])

obs.rename(columns={"STATION": "STATION_ID", "DATE": "OBS_DATE"}, inplace=True)
obs.to_csv("data/observations.csv", index=True, index_label="OBS_ID")

print(f"Created CSVs: {len(stations)} Stations, {len(obs)} Observations.")
