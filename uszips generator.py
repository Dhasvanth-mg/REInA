import pandas as pd
import pgeocode

# Load U.S. ZIP code data
nomi = pgeocode.Nominatim('us')
df = nomi._data[['postal_code', 'latitude', 'longitude']].dropna()

# Rename columns to match expected format
df = df.rename(columns={
    'postal_code': 'zip',
    'latitude': 'lat',
    'longitude': 'lng'
})

# Add optional placeholder columns
df['school_rating'] = 5.0
df['university_distance_mi'] = 10.0
df['military_distance_mi'] = 20.0

# Save to CSV
df.to_csv("us_zips.csv", index=False)
print("✅ us_zips.csv generated.")
