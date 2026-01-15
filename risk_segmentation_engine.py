import pandas as pd
from sklearn.cluster import KMeans
print("Loading data...")
df = pd.read_csv("AADHAAR_FINAL_ANALYTICS.csv")

X = df[['Friction_Score', 'Child_Risk_Score']]

print("Training Machine Learning Model...")
kmeans = KMeans(n_clusters=3, random_state=42)

kmeans.fit(X) 
df['Cluster_Label'] = kmeans.labels_

print("\n--- ML Cluster Analysis (Average Values) ---")
cluster_summary = df.groupby('Cluster_Label')[['Friction_Score', 'Child_Risk_Score']].mean()
print(cluster_summary)

output_file = "AADHAAR_FINAL_ANALYTICS_WITH_ML.csv"
df.to_csv(output_file, index=False)
print(f"\nSUCCESS! Added Machine Learning Clusters to: {output_file}")