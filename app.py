import sqlite3
import os
from load_sqlite import load_local_data # Import your loading function

if not os.path.exists('teammate_database.db'):
    print("Database not found. Initializing...")
    load_local_data()

def run_app():
    # 1. Connect once at the very beginning
    conn = sqlite3.connect('teammate_database.db')
    cursor = conn.cursor()

    while True:
        print("\n--- Weather & Climate System ---")
        print("1. Get all observations for a specific station (JOIN)")
        print("2. Filter observations by date range (JOIN)")
        print("3. View average values for each station (GROUP BY + JOIN)")
        print("4. View all stations in a specific state")
        print("5. View raw observations for a station ID")
        print("6. Exit")
        
        # 2. Wait for user input (This stops the loop from being infinite)
        choice = input("\nSelect an option: ")

        if choice == '1':
            name = input("Enter Station Name: ")
            cursor.execute("SELECT NAME, OBS_DATE, VALUE FROM STATION NATURAL JOIN OBSERVATION WHERE NAME LIKE ?", (f"%{name}%",))
            for row in cursor.fetchall()[:10]: print(row)

        elif choice == '2':
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            
            # This query "talks" to both tables to get the name and the data
            query = """
            SELECT o.OBS_ID, o.STATION_ID, s.NAME, o.OBS_DATE, o.VAR_CODE, o.VALUE
            FROM OBSERVATION o
            JOIN STATION s ON o.STATION_ID = s.STATION
            WHERE o.OBS_DATE BETWEEN ? AND ?
            """
            
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            
            for row in results:
                # This prints the whole observation plus the station name (row[2])
                print(f"ID: {row[0]} | Station: {row[2]} | Date: {row[3]} | Var: {row[4]} | Val: {row[5]}")
                        

        elif choice == '3':
            print("\nCalculating averages (this may take a moment)...")
            
            query = """
            SELECT s.NAME, AVG(o.VALUE) 
            FROM STATION s
            JOIN OBSERVATION o ON s.STATION = o.STATION_ID 
            GROUP BY s.NAME
            ORDER BY AVG(o.VALUE) DESC
            LIMIT 20
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            print(f"\n{'Station Name':<30} | {'Average':<10}")
            print("-" * 45)
            
            for row in results:
                # row[0] is Name, row[1] is the calculated Average
                print(f"{row[0]:<30} | {row[1]:.2f}")

        elif choice == '4':
            state = input("Enter State (e.g., FL): ")
            cursor.execute("SELECT * FROM STATION WHERE STATE = ?", (state.upper(),))
            for row in cursor.fetchall(): print(row)
#place holder input state and show all observations within state
# search by if and will give all info
        elif choice == '5':
            s_id = input("Enter Station ID: ")
            cursor.execute("SELECT * FROM OBSERVATION WHERE STATION_ID = ?", (s_id,))
            for row in cursor.fetchall()[:10]: print(row)

        elif choice == '6':
            print("Closing application...")
            break
        
        else:
            print("Invalid choice, please try again.")
    
    # 3. Close once at the very end
    conn.close()

if __name__ == "__main__":
    run_app()
    #sqlite3 teammate_database.db < schema.sql