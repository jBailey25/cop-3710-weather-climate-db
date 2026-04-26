import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect("teammate_database.db", check_same_thread=False)

st.title("🌦️ Weather Analytics App")
st.write("**Units:** Temperature = °F | Precipitation = inches | Snow Depth = inches")

option = st.selectbox(
    "Choose a feature",
    [
        "View all available states",
        "View stations in a selected state",
        "View observations by state and weather variable",
        "Filter observations by date range",
        "View top values for a selected weather variable",
        "Average weather variable by state",
        "View available types of weather variables",
    ]
)

# 1. Show all states
if option == "View all available states":
    if st.button("Run Query"):
        query = """
        SELECT DISTINCT STATE
        FROM STATION
        WHERE STATE IS NOT NULL
        ORDER BY STATE
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)


# 2. View stations in selected state
elif option == "View stations in a selected state":
    states_df = pd.read_sql_query(
        """
        SELECT DISTINCT STATE
        FROM STATION
        WHERE STATE IS NOT NULL
        ORDER BY STATE
        """,
        conn
    )

    selected_state = st.selectbox("Select a state", states_df["STATE"].tolist())

    if st.button("Run Query"):
        query = """
        SELECT STATION AS Station_ID,
               NAME,
               STATE
        FROM STATION
        WHERE STATE = ?
        ORDER BY NAME
        """
        df = pd.read_sql_query(query, conn, params=(selected_state,))
        st.dataframe(df)

elif option == "View observations by state and weather variable":
    states_df = pd.read_sql_query(
        """
        SELECT DISTINCT STATE
        FROM STATION
        WHERE STATE IS NOT NULL
        ORDER BY STATE
        """,
        conn
    )

    selected_state = st.selectbox("Select a state", states_df["STATE"].tolist())

    variable = st.selectbox(
        "Select a weather variable",
        ["PRCP", "SNWD", "TMAX", "TMIN"]
    )

    if st.button("Run Query"):
        query = """
        SELECT s.NAME,
               s.STATE,
               o.OBS_DATE,
               o.VAR_CODE,
               o.VALUE
        FROM OBSERVATION o
        JOIN STATION s ON o.STATION_ID = s.STATION
        WHERE s.STATE = ?
          AND o.VAR_CODE = ?
        ORDER BY o.OBS_DATE
        LIMIT 100
        """
        df = pd.read_sql_query(query, conn, params=(selected_state, variable))
        st.dataframe(df)

elif option == "Filter observations by date range":
    # Show available date range
    date_range = pd.read_sql_query(
        """
        SELECT MIN(OBS_DATE) AS Earliest_Date,
               MAX(OBS_DATE) AS Latest_Date
        FROM OBSERVATION
        """,
        conn
    )

    st.write(
        f"Available date range: {date_range['Earliest_Date'][0]} "
        f"to {date_range['Latest_Date'][0]}"
    )

    # Get states for dropdown
    states_df = pd.read_sql_query(
        """
        SELECT DISTINCT STATE
        FROM STATION
        WHERE STATE IS NOT NULL
        ORDER BY STATE
        """,
        conn
    )

    selected_state = st.selectbox("Select a state", states_df["STATE"].tolist())

    start = st.text_input("Start date (YYYY-MM-DD)")
    end = st.text_input("End date (YYYY-MM-DD)")

    if st.button("Run Query"):
        query = """
        SELECT s.STATE,
               o.STATION_ID,
               o.OBS_DATE,
               o.VAR_CODE,
               o.VALUE
        FROM OBSERVATION o
        JOIN STATION s ON o.STATION_ID = s.STATION
        WHERE s.STATE = ?
          AND o.OBS_DATE BETWEEN ? AND ?
        ORDER BY o.OBS_DATE
        LIMIT 100
        """
        df = pd.read_sql_query(query, conn, params=(selected_state, start, end))
        st.dataframe(df)

# Option 5. "View top values for a specific variable"
elif option == "View top values for a selected weather variable":
    variable = st.selectbox(
        "Select a weather variable",
        ["PRCP", "SNWD", "TMAX", "TMIN"]
    )

    top_n = st.number_input(
        "How many top values do you want to see? (Max 50)",
        min_value=1,
        max_value=50,
        value=5
    )

    if st.button("Run Query"):
        query = """
        SELECT s.NAME,
               s.STATE,
               o.OBS_DATE,
               o.VAR_CODE,
               o.VALUE
        FROM OBSERVATION o
        JOIN STATION s ON o.STATION_ID = s.STATION
        WHERE o.VAR_CODE = ?
        ORDER BY o.VALUE DESC
        LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(variable, top_n))
        st.dataframe(df)

# 6. Average weather variable by state
elif option == "Average weather variable by state":
    variable = st.selectbox(
        "Select a weather variable",
        ["PRCP", "SNWD", "TMAX", "TMIN"]
    )

    if st.button("Run Query"):
        query = """
        SELECT s.STATE,
               o.VAR_CODE,
               ROUND(AVG(o.VALUE), 2) AS Avg_Value
        FROM OBSERVATION o
        JOIN STATION s ON o.STATION_ID = s.STATION
        WHERE o.VAR_CODE = ?
        GROUP BY s.STATE, o.VAR_CODE
        ORDER BY Avg_Value DESC
        """
        df = pd.read_sql_query(query, conn, params=(variable,))
        st.dataframe(df)

# Option 3. View Varible Types and Names
elif option == "View available types of weather variables":
    if st.button("Run Query"):
        query = """
        SELECT VAR_CODE,
               VAR_NAME
        FROM VARIABLES
        WHERE VAR_NAME IS NOT NULL
        ORDER BY VAR_CODE
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)