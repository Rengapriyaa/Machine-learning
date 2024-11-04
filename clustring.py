import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

# Load your dataset (adjust the path to where your dataset is stored)
wine_data = pd.read_csv('/kaggle/input/wine-dataset-for-clustering/wine-clustering.csv')

# Normalize the data
scaler = StandardScaler()
wine_scaled = scaler.fit_transform(wine_data)

# 1. K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42, init='k-means++', n_init=10, max_iter=300)
kmeans.fit(wine_scaled)

# Initial centroids, final clusters, epoch size, and error rate for K-Means
initial_centroids = kmeans.cluster_centers_
final_clusters_kmeans = kmeans.labels_
epoch_size = kmeans.n_iter_
error_rate = kmeans.inertia_

# Output K-Means results
print("K-Means Clustering Results:")
print(f"Initial Centroids:\n{initial_centroids}")
print(f"Final Clusters:\n{final_clusters_kmeans}")
print(f"Epoch Size: {epoch_size}")
print(f"Error Rate (Inertia): {error_rate}\n")

# 2. Hierarchical Agglomerative Clustering
hierarchical_clustering = AgglomerativeClustering(n_clusters=3)
final_clusters_hierarchical = hierarchical_clustering.fit_predict(wine_scaled)

# Output Hierarchical Clustering results
print("Hierarchical Agglomerative Clustering Results:")
