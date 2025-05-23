import sqlite3
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# --- Load ZIP info from Kaggle dataset ---
zipinfo = pd.read_csv("uszips.csv")
zipinfo = zipinfo.rename(columns={
    "postal code": "zip",
    "place name": "city",
    "admin name1": "state",
    "latitude": "lat",
    "longitude": "lng"
})
zipinfo['zip'] = zipinfo['zip'].astype(str).str.zfill(5)

# --- Find Nearby ZIPs ---
def get_nearby_zipcodes(center_zip, radius=20):
    df = zipinfo.copy()
    center_zip = str(center_zip).zfill(5)
    df['zip'] = df['zip'].astype(str).str.zfill(5)
    center_row = df[df['zip'] == center_zip]
    if center_row.empty:
        raise ValueError(f"ZIP {center_zip} not found in dataset.")
    center_point = (center_row.iloc[0]['lat'], center_row.iloc[0]['lng'])
    df['distance'] = df.apply(lambda row: geodesic(center_point, (row['lat'], row['lng'])).miles, axis=1)
    return df[df['distance'] <= radius]

# --- Load Real Estate Data from DB ---
def load_real_data_from_db(zip_list, db_path='reina_redfinzipdata.db'):
    conn = sqlite3.connect(db_path)
    zip_tuple = tuple(zip_list)
    query = f"""
    SELECT ZIP, STATE_CODE, MEDIAN_SALE_PRICE, MEDIAN_LIST_PRICE,
           HOMES_SOLD, INVENTORY, MONTHS_OF_SUPPLY, MEDIAN_DOM
    FROM zip_data
    WHERE ZIP IN ({','.join(['?'] * len(zip_tuple))})
    """
    df = pd.read_sql_query(query, conn, params=zip_tuple)
    conn.close()
    return df.rename(columns={
        'ZIP': 'zipcode',
        'MEDIAN_SALE_PRICE': 'median_price',
        'MEDIAN_LIST_PRICE': 'median_list_price',
        'HOMES_SOLD': 'homes_sold',
        'INVENTORY': 'inventory',
        'MONTHS_OF_SUPPLY': 'months_supply',
        'MEDIAN_DOM': 'dom'
    }).dropna(subset=['median_price'])

# --- Score ZIPs ---
def compute_scores(df):
    df = df.copy()
    df['inventory'] = df['inventory'].fillna(df['inventory'].median())
    df['homes_sold'] = df['homes_sold'].fillna(0)
    df['dom'] = df['dom'].fillna(df['dom'].median())
    dom_score = 1 - (df['dom'] / df['dom'].max())
    demand_score = df['homes_sold'] / (df['inventory'] + 1)
    price_score = 1 - (df['median_price'] / df['median_price'].max())
    df['investment_score'] = 0.4 * dom_score + 0.4 * demand_score + 0.2 * price_score
    return df

# --- Plot Results ---
def show_results(df, highlight_zip=None):
    df = df.copy()

    # Normalize scores to 100% scale
    max_score = df['investment_score'].max()
    df['investment_score'] = (df['investment_score'] / max_score) * 100

    # Include the center ZIP if it's not already in top list
    if highlight_zip and highlight_zip not in df['zipcode'].astype(str).tolist():
        print(f"Including center ZIP {highlight_zip} in results.")
        extra_data = load_real_data_from_db([highlight_zip])
        if not extra_data.empty:
            extra_data = compute_scores(extra_data)
            extra_data['investment_score'] = (extra_data['investment_score'] / max_score) * 100
            df = pd.concat([extra_data, df])

    df = df.drop_duplicates(subset='zipcode')

    print("\nTop Investment Regions:")
    print(df[['zipcode', 'median_price', 'investment_score', 'homes_sold', 'inventory', 'dom']])

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df['zipcode'].astype(str), df['investment_score'])

    colors = []
    for z in df['zipcode'].astype(str):
        if z == highlight_zip:
            colors.append("crimson")
        elif len(colors) == 0:
            colors.append("gold")
        elif len(colors) == 1:
            colors.append("silver")
        elif len(colors) == 2:
            colors.append("peru")
        else:
            colors.append("skyblue")

    for bar, color in zip(bars, colors):
        bar.set_color(color)

    plt.title('Top Investment Scores (%)', fontsize=18)
    plt.xlabel('ZIP Code', fontsize=14)
    plt.ylabel('Investment Score (%)', fontsize=14)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{round(yval)}%",
                 ha='center', va='bottom', fontsize=10)

    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --- Regional Ranking ---
def top_zipcodes_by_region(region_type, region_value):
    region_type = region_type.lower()
    if region_type not in ['city', 'state']:
        print(" Region type must be 'city' or 'state'.")
        return

    region_df = zipinfo[zipinfo[region_type].str.lower() == region_value.lower()]
    zip_list = region_df['zip'].dropna().unique().tolist()

    if not zip_list:
        print(f" No ZIP codes found for {region_type.title()} = {region_value}")
        return

    data = load_real_data_from_db(zip_list)
    if data.empty:
        print(f" No real estate data found for ZIPs in {region_type.title()} {region_value}")
        return

    data = data.drop_duplicates(subset='zipcode')
    scored_data = compute_scores(data)
    top_picks = scored_data.sort_values(by='investment_score', ascending=False).head(5)
    show_results(top_picks)

# --- Proximity Ranking ---
def top_zipcodes_by_proximity(center_zip, radius=20):
    try:
        nearby_df = get_nearby_zipcodes(center_zip, radius)
        zip_list = nearby_df['zip'].astype(str).str.zfill(5).tolist()
        data = load_real_data_from_db(zip_list)
        if data.empty:
            print(" No real estate data found for nearby ZIPs.")
            return
        data = data.drop_duplicates(subset='zipcode')
        scored_data = compute_scores(data)
        top_picks = scored_data.sort_values(by='investment_score', ascending=False).head(5)
        show_results(top_picks, highlight_zip=str(center_zip).zfill(5))
    except Exception as e:
        print(f" Error: {e}")

# --- CLI Loop ---
def cli_loop():
    print(" Reina Real Estate CLI")
    print("Type:")
    print("  zip    → to search nearby ZIPs")
    print("  city   → to search top ZIPs in a city")
    print("  state  → to search top ZIPs in a state")
    print("  quit   → to exit")

    while True:
        command = input("\nEnter command (zip/city/state/quit): ").strip().lower()

        if command == 'zip':
            center_zip = input("Enter ZIP code: ").strip()
            radius = input("Enter radius in miles (default 20): ").strip()
            radius = int(radius) if radius.isdigit() else 20
            top_zipcodes_by_proximity(center_zip, radius)

        elif command == 'city':
            city = input("Enter city name: ").strip()
            top_zipcodes_by_region("city", city)

        elif command == 'state':
            state = input("Enter state name: ").strip()
            top_zipcodes_by_region("state", state)

        elif command == 'quit':
            print(" Exiting. Goodbye!")
            break

        else:
            print(" Unknown command. Try zip / city / state / quit.")

# --- Entry Point ---
if __name__ == "__main__":
    cli_loop()
