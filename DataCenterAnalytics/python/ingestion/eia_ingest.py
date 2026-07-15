import requests
import pandas as pd
import json
import time
from datetime import datetime

# Load API key
with open("../config/eia_key.txt", "r") as f:
    API_KEY = f.read().strip()

# Define the monthly "chunks" to fetch safely
months = [
    ("2026-01-01T00", "2026-01-31T23"),
    ("2026-02-01T00", "2026-02-28T23"),
    ("2026-03-01T00", "2026-03-31T23"),
    ("2026-04-01T00", "2026-04-30T23"),
    ("2026-05-01T00", "2026-05-31T23"),
    ("2026-06-01T00", "2026-06-22T23") # Up to today
]

all_daily_records = []

for start, end in months:
    print(f"Fetching EIA data from {start[:7]}...")
    
    url = (
        f"https://api.eia.gov/v2/electricity/rto/region-data/data/?"
        f"api_key={API_KEY}"
        f"&frequency=hourly"
        f"&data[0]=value"
        f"&facets[respondent][]=PJM"
        f"&start={start}"
        f"&end={end}"
        f"&length=100000" # Generous ceiling for a single month
    )
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {start}. Skipping.")
        continue
        
    data = response.json()
    records = data["response"]["data"]
    
    # Convert this month's chunk into a temporary DataFrame
    df_chunk = pd.DataFrame(records)
    df_chunk.columns = [c.lower().replace(" ", "_") for c in df_chunk.columns]
    
    # IDEA 2: Clean and Aggregate IN-MEMORY before saving!
    # Extract just the 'YYYY-MM-DD' date string out of the 'period' column
    df_chunk['date'] = df_chunk['period'].str.split('T').str[0]
    df_chunk['value'] = pd.to_numeric(df_chunk['value'], errors='coerce')
    
    # Group by Date and Type (D or NG), summing up the hourly values into daily totals
    df_daily = df_chunk.groupby(['date', 'type'])['value'].sum().reset_index()
    
    # Append the condensed rows to our master list
    all_daily_records.append(df_daily)
    
    # Respectful pause to keep the API happy
    time.sleep(1)

# 1. Combine all condensed monthly dataframes into one master table
master_df = pd.concat(all_daily_records, ignore_index=True)

# FIX: Force-filter out any unexpected grid metrics (like DF or TI) 
# to guarantee we only have D and NG before pivoting.
master_df = master_df[master_df['type'].isin(['D', 'NG'])]

# 2. Pivot the data safely
master_pivoted = master_df.pivot(index='date', columns='type', values='value').reset_index()

# 3. Rename the exact 3 columns
master_pivoted.columns = ['Date', 'Daily_Demand_MWh', 'Daily_Generation_MWh']

# Save the beautifully organized, ultra-lightweight dataset
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
processed_path = f"../data_processed/eia_daily_compiled_{timestamp}.csv"
master_pivoted.to_csv(processed_path, index=False)

print(f"Success! Saved clean, pivoted, daily data to {processed_path}")
print(master_pivoted.head(10))