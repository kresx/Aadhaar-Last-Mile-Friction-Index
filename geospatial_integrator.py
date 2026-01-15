import pandas as pd

print("Loading datasets...")
analytics_df = pd.read_csv("AADHAAR_FINAL_ANALYTICS_WITH_ML.csv")

geo_df = pd.read_csv("lat-&-lon-india-district.csv")

geo_df['District_Standard'] = geo_df['District'].str.title().str.strip()
analytics_df['district_clean'] = analytics_df['district_clean'].str.strip()

print("Merging Geospatial data...")
merged_df = pd.merge(
    analytics_df, 
    geo_df[['District_Standard', 'Latitude', 'Longitude']], 
    left_on='district_clean', 
    right_on='District_Standard', 
    how='left'
)

missing = merged_df[merged_df['Latitude'].isna()]
print(f"Matched: {len(merged_df) - len(missing)} districts.")
print(f"Missing Coordinates for: {len(missing)} districts (These won't appear on map).")

output_file = "AADHAAR_DASHBOARD_FINAL.csv"
merged_df.to_csv(output_file, index=False)
print(f"SUCCESS! Saved final dashboard data to: {output_file}")