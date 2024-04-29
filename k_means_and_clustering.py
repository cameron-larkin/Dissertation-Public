# -*- coding: utf-8 -*-
"""K-Means_and_clustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19OiI92ffuvl62Pq3p0rjZ8snR3YTNcIA
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# Load the datasets
players_df = pd.read_excel('Players.xlsx')
transfer_values_df = pd.read_csv('Transfer_Values.csv')

# Preprocessing Transfer Values
def convert_market_value(value):
    if 'm' in value:
        return float(value.replace('€', '').replace('m', ''))
    elif 'k' in value:
        return float(value.replace('€', '').replace('k', '')) / 1000
    return float(value.replace('€', ''))

transfer_values_df['Market Value'] = transfer_values_df['Market Value'].apply(convert_market_value)

# Merge datasets on player names
merged_df = pd.merge(players_df, transfer_values_df, left_on='Player', right_on='Name', how='inner')

# Selecting relevant features
features_df = merged_df[['Gls', 'Ast', 'Min', 'Market Value']]

# Handling missing values and normalization
imputer = SimpleImputer(strategy='mean')
features_imputed = imputer.fit_transform(features_df)
scaler = StandardScaler()
features_normalized = scaler.fit_transform(features_imputed)

# K-means clustering
kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
cluster_labels = kmeans.fit_predict(features_normalized)
features_normalized_df = pd.DataFrame(features_normalized, columns=features_df.columns)
features_normalized_df['Cluster'] = cluster_labels

# Analyzing cluster profiles for K-means
cluster_profiles = features_normalized_df.groupby('Cluster')[features_df.columns].mean()

# Inverse transform the cluster profiles to get them back to the original scale
cluster_profiles_original_scale = scaler.inverse_transform(cluster_profiles)
cluster_profiles_df = pd.DataFrame(cluster_profiles_original_scale, columns=features_df.columns)

print("K-means Cluster Profiles:\n", cluster_profiles_df)

pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_normalized)

# Hierarchical clustering
Z = linkage(features_pca, method='ward')

# Plotting the dendrogram
plt.figure(figsize=(10, 7))
plt.title("Hierarchical Clustering Dendrogram")
dendrogram(Z, truncate_mode='lastp', p=12, leaf_rotation=45., leaf_font_size=10., show_contracted=True)
plt.xlabel("Cluster size")
plt.ylabel("Distance")
plt.show()