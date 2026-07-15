import requests
import pandas as pd
import json
import time
from datetime import datetime

# Load NOAA token
with open("../config/noaa_token.txt", "r") as f:
    TOKEN = f.read().strip()

url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
headers = {"token": TOKEN}

# Focus on Virginia (FIPS:51). To minimize noise, we can also bind a specific station ID if known.
params = {
    "datasetid": "GHCND",
    "datatypeid": ["TMAX", "TMIN", "TAVG"],
    "locationid": "FIPS:51",
    "startdate": "2023-01-01",
    "enddate": "2023-12-31",
    "limit": 1000,
    "offset": 1  # Start at record 1
}

all_results = []
count = 0
max_records = 50000  # Defensive ceiling so a loop doesn't run infinitely

print("Starting paginated NOAA data extraction...")

while count < max_records:
    print(f"Fetching records starting at offset: {params['offset']}...")
    response = requests.get(url, headers=headers, params=params)
    
    # Handle API rate limiting gracefully
    if response.status_code == 429:
        print("Rate limit hit. Sleeping for 10 seconds...")
        time.sleep(10)
        continue
        
    data = response.json()
    
    # Break if no more results are returned
    if "results" not in data or not data["results"]:
        print("No more records found. Extraction complete.")
        break
        
    records = data["results"]
    all_results.extend(records)
    
    # Increment offset by the limit to fetch the next page
    params["offset"] += params["limit"]
    count += len(records)
    
    # Respectful delay between API calls
    time.sleep(0.5)

# Save raw JSON cumulative dataset
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
raw_path = f"../data_raw/noaa_raw_combined_{timestamp}.json"
with open(raw_path, "w") as f:
    json.dump(all_results, f, indent=2)

# Convert to DataFrame
df = pd.DataFrame(all_results)

# Clean column names
df.columns = [c.lower().replace(" ", "_") for c in df.columns]

# Save processed CSV
processed_path = f"../data_processed/noaa_daily_{timestamp}.csv"
df.to_csv(processed_path, index=False)

print(f"Successfully compiled {len(df)} climate records across the full timeline into {processed_path}")