import sqlite3

def print_full_database(db_path='redfin_real_estate_data.db', batch_size=10):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Count total records
    cursor.execute('SELECT COUNT(*) FROM real_estate')
    total_rows = cursor.fetchone()[0]
    print(f"✅ Total rows in database: {total_rows}")
    
    if total_rows == 0:
        print("⚠️ Warning: No data found! (Maybe insertion failed?)")
        conn.close()
        return

    # Fetch and print in batches
    offset = 0
    while offset < total_rows:
        cursor.execute(f'SELECT * FROM real_estate LIMIT {batch_size} OFFSET {offset}')
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
        
        offset += batch_size
        input(f"📄 Printed {offset} rows. Press Enter to load next batch...")

    conn.close()
    print("✅ Finished printing entire database.")

def printalldbtables():
    import sqlite3

    conn = sqlite3.connect("redfin_real_estate_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM real_estate WHERE type='table';")
    tables = cursor.fetchall()

    print("Available tables:", tables)
    conn.close()

def csvtest():
    import pandas as pd
    df = pd.read_csv("us_zips.csv")
    df['zip'] = df['zip'].astype(str).str.zfill(5)
    print("20164" in df['zip'].values)  # Should print True

def addtocsv():
    import pandas as pd

    df = pd.read_csv("us_zips.csv")
    new_row = pd.DataFrame([{"zip": "20164", "lat": 39.0022, "lng": -77.3981}])
    df['zip'] = df['zip'].astype(str).str.zfill(5)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("us_zips.csv", index=False)

def get_distinct_property_types(db_path='redfin_real_estate_data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT "PROPERTY_TYPE" FROM real_estate')
    distinct_types = cursor.fetchall()

    print("Distinct Property Types:")
    for t in distinct_types:
        print(f" - {t[0]}")

    conn.close()

def fix_error():
    import sqlite3

    conn = sqlite3.connect("real_estate_data.db")
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(zip_data)")
    for row in cur.fetchall():
        print(row)

    conn.close()

def printalldbtables():
    conn = sqlite3.connect("redfin_real_estate_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Available tables:", tables)
    conn.close()






# Run the function


#print_full_database()
#printalldbtables()
#csvtest()
#addtocsv()
#get_distinct_property_types()
#fix_error()
printalldbtables()