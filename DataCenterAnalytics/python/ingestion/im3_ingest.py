import pandas as pd
from datetime import datetime

# 1. Load raw file
raw_path = "../data_raw/osm_datacenters.csv"
df = pd.read_csv(raw_path)

# 2. Standardize column names (lowercase, underscores)
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# 3. Convert coordinates to numeric
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

# 4. Drop rows without valid coordinates
df = df.dropna(subset=["lat", "lon"])

# 5. Enforce useful data types
numeric_cols = ["sqft", "state_id", "county_id"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 6. Add ingestion timestamp
df["ingested_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

# 7. Save processed file
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
processed_path = f"../data_processed/im3_datacenters_{timestamp}.csv"
df.to_csv(processed_path, index=False)

print("IM3 Data Center dataset processed successfully.")
print(f"Saved to: {processed_path}")