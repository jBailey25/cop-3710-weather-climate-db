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
This project designa a relational Weather and Climate Analytics databse to store and analyse daily weather observations by station and date. A subset of NOAA GHCHN-D (Global Historical Climatology Network - Daily) data from 01/01/2026 to 01/07/2026. It uses real-world observations from 3,625 unique weather stations across 10 different U.S. states. 

The schema models weather stations, weather variables, and observations.

# Final (UPDATED) Normalized ER / Relational Schema (BCNF)

## STATION
- STATION_ID (PK)
- NAME
- STATE

## WEATHER_VARIABLE
- VAR_CODE (PK)
- VAR_NAME

## OBSERVATION
- OBS_ID (PK)
- STATION_ID (FK → STATION.STATION_ID)
- OBS_DATE
- VAR_CODE (FK → WEATHER_VARIABLE.VAR_CODE)
- VALUE
