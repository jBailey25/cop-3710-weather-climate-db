# Global Weather & Climate Analytics Database

## Application Domain:
This database supports weather and climate data analysis, stores weather data, analyzes it over time, and identifies patterns. 

## High-Level Goals:
- Store weather observations by date and location
- Support the analysis of weather trends over time
- Identify unusual weather patterns
- Support user queries for summarized weather information

## Intended Users:
- Climate researchers
- Data analysts
- Environmental planners and engineers
- Students and educators

## Data Sources:
The database will use publicly available weather and climate datasets

## Update - Database Application (Part B) :
This project designa a relational Weather and Climate Analytics databse to store and analyse daily weather observations by station and date. A subset of NOAA GHCHN-D (Global Historical Climatology Network - Daily) data from 02/02/2026 to 02/07/2026 for Orlando, FL and Denver, CO is used as the data source. 

The schema models stations, weather variables, and observations, including a weak entity (Sensor) and an associative entity (Observation). 

# Final Normalized ER / Relational Schema (BCNF)

## DATASET
- Dataset_ID (PK)
- Source_name

## STATION
- Station_ID (PK)
- Dataset_ID (FK → DATASET.Dataset_ID)
- Name
- Latitude
- Longitude
- Elevation

## STATION_PROFILE
- Station_ID (PK, FK → STATION.Station_ID)
- Status

## SENSOR
- Station_ID (PK, FK → STATION.Station_ID)
- Sen_Num (PK)
- Sen_Type
- Install_Date

## WEATHER_VARIABLE
- Variable_Code (PK)
- Variable_Name
- Unit

## OBSERVATION
- Observation_ID (PK)
- Station_ID (FK → STATION.Station_ID)
- Variable_Code (FK → WEATHER_VARIABLE.Variable_Code)
- Value
- Observed_At
