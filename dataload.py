import oracledb
import pandas as pd

oracledb.init_oracle_client(
    lib_dir="/Users/justineb/instantclient-basic-macos.arm64-23.3.0.23.09-2 2"
)

conn = oracledb.connect(
    user="JBAILEY6814_SCHEMA_CQK42",
    password="MyPassword",
    dsn="db.freesql.com:1521/23ai_34ui2"
)

cursor = conn.cursor()
cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")

def load(table_name, file_name):
    df = pd.read_csv(file_name)
    # convert all columns to strings or None
