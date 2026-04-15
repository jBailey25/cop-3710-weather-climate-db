import sqlite3
import pandas as pd
import os

def load_local_data():
    # Connect to your local SQLite file
    conn = sqlite3.connect('teammate_database.db')
    
    # Load Stations from the data folder
    if os.path.exists('data/stations.csv'):
        df_stations = pd.read_csv('data/stations.csv')
        df_stations.to_sql('STATION', conn, if_exists='replace', index=False)
        print(f"✅ Stations loaded into SQLite.")

    # Load Observations from the data folder
    if os.path.exists('data/observations.csv'):
        df_obs = pd.read_csv('data/observations.csv')
        
        if 'date' in df_obs.columns:
            df_obs.rename(columns={'date': 'OBS_DATE'}, inplace=True)
        
        df_obs.to_sql('OBSERVATION', conn, if_exists='replace', index=False)
        print(f"✅ Observations loaded into SQLite.")

    conn.close()

if __name__ == "__main__":
    load_local_data()