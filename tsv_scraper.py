import pandas as pd
import sqlite3

# Load Redfin TSV
df = pd.read_csv("redfin_data.tsv", sep="\t")

# Filter/rename columns if needed
df = df.rename(columns={
    "ZIP": "ZIP",
    "STATE": "STATE_CODE",
    "MEDIAN_SALE_PRICE": "MEDIAN_SALE_PRICE",
    "MEDIAN_LIST_PRICE": "MEDIAN_LIST_PRICE",
    "HOMES_SOLD": "HOMES_SOLD",
    "INVENTORY": "INVENTORY",
    "MONTHS_OF_SUPPLY": "MONTHS_OF_SUPPLY",
    "MEDIAN_DOM": "MEDIAN_DOM"
})

# Only keep relevant columns (if needed)
columns_to_keep = [
    "ZIP", "STATE_CODE", "MEDIAN_SALE_PRICE", "MEDIAN_LIST_PRICE",
    "HOMES_SOLD", "INVENTORY", "MONTHS_OF_SUPPLY", "MEDIAN_DOM"
]
df = df[columns_to_keep]

# Fix ZIPs as 5-digit strings
df["ZIP"] = df["ZIP"].astype(str).str.zfill(5)

# Write to SQLite
conn = sqlite3.connect("reina_redfinzipdata.db")
df.to_sql("zip_data", conn, if_exists="replace", index=False)
conn.close()

print("✅ Data imported to reina_redfinzipdata.db into table 'zip_data'")
