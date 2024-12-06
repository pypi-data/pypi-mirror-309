import os
import random
from typing import List

import numpy as np
import pandas as pd
from prettytable import PrettyTable
from sklearn.cluster import KMeans
import random
import pandas as pd
import numpy as np
from typing import List
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class ClusterAnalysis:
    def __init__(
        self,
        cluster_queue: List[int],  # ex: [5,10,15,20,25,30]
        training_data: pd.DataFrame,
        min_ratio: float,  # percent total df, such as 0.01 for 1%
        numerical_cols: List[str],
        sample_size: int,  # such as 5
        threshold: int,
        target: str,
        epochs: int,
    ):
        self.cluster_queue = cluster_queue
        self.training_data = training_data
        self.min_ratio = min_ratio
        self.numerical_cols = numerical_cols
        self.sample_size = sample_size
        self.threshold = threshold
        self.target = target
        self.epochs = epochs
        self.results = []

    # Function to get random columns
    def get_random_cols(self) -> List[str]:
        return random.sample(self.numerical_cols, self.sample_size)

    # Function to run clustering analysis
    def run_clustering(self):
        for n_clusters in self.cluster_queue:
            for epoch in range(self.epochs):
                random_cols = self.get_random_cols()
                subset_df = (
                    self.training_data[random_cols]
                    .replace([np.inf, -np.inf], np.nan)
                    .dropna()
                )

                if subset_df.empty:
                    continue  # Skip if no data left after dropping NaNs

                # Apply KMeans clustering
                kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
                labels = kmeans.fit_predict(subset_df)

                # Assign cluster labels
                cluster_df = self.training_data.loc[subset_df.index].copy()
                cluster_df["Cluster"] = labels

                # Filter out clusters with less than min_ratio of total rows
                min_size = self.min_ratio * len(self.training_data)
                cluster_counts = cluster_df["Cluster"].value_counts()
                valid_clusters = cluster_counts[cluster_counts >= min_size].index

                for cluster in valid_clusters:
                    cluster_data = cluster_df[cluster_df["Cluster"] == cluster]
                    fitness = (cluster_data[self.target] > self.threshold).mean() * 100
                    cluster_name = f"{' '.join(random_cols)}__Cluster {cluster}__Cluster Queue {n_clusters}"
                    self.results.append(
                        {
                            "Cluster Name": cluster_name,
                            "Fitness": fitness,
                            "Cluster Size": len(cluster_data),
                        }
                    )

        # Sort the results by fitness in descending order and keep top 10
        self.results = sorted(self.results, key=lambda x: x["Fitness"], reverse=True)[
            :10
        ]

    # Function to display results
    def display_results(self):
        table = PrettyTable()
        table.field_names = ["Cluster Name", "Fitness (%)", "Cluster Size"]
        for result in self.results:
            table.add_row(
                [
                    result["Cluster Name"],
                    f"{result['Fitness']:.2f}",
                    result["Cluster Size"],
                ]
            )
        print(table)






class DbScanClusterAnalysis:
    def __init__(
        self,
        eps: float,  # DBSCAN epsilon parameter
        min_samples: int,  # Minimum samples per cluster for DBSCAN
        training_data: pd.DataFrame,
        min_ratio: float,  # percent total df, such as 0.01 for 1%
        numerical_cols: List[str],
        sample_size: int,  # such as 5
        threshold: int,
        target: str,
        epochs: int,
    ):
        self.eps = eps
        self.min_samples = min_samples
        self.training_data = training_data
        self.min_ratio = min_ratio
        self.numerical_cols = numerical_cols
        self.sample_size = sample_size
        self.threshold = threshold
        self.target = target
        self.epochs = epochs
        self.results = []

    # Function to get random columns
    def get_random_cols(self) -> List[str]:
        return random.sample(self.numerical_cols, self.sample_size)

    # Function to run clustering analysis
    def run_clustering(self):
        for epoch in range(self.epochs):
            random_cols = self.get_random_cols()
            subset_df = self.training_data[random_cols].replace([np.inf, -np.inf], np.nan).dropna()
            
            if subset_df.empty:
                continue  # Skip if no data left after dropping NaNs
            
            # Apply DBSCAN clustering
            dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples)
            labels = dbscan.fit_predict(subset_df)
            
            # Assign cluster labels
            cluster_df = self.training_data.loc[subset_df.index].copy()
            cluster_df['Cluster'] = labels
            
            # Filter out noise and small clusters
            min_size = self.min_ratio * len(self.training_data)
            cluster_counts = cluster_df['Cluster'].value_counts()
            valid_clusters = cluster_counts[cluster_counts >= min_size].index

            for cluster in valid_clusters:
                if cluster == -1:  # Skip noise points
                    continue
                cluster_data = cluster_df[cluster_df['Cluster'] == cluster]
                fitness = (cluster_data[self.target] > self.threshold).mean() * 100
                cluster_name = f"{' '.join(random_cols)}__Cluster {cluster}__Epoch {epoch}"
                self.results.append({
                    'Cluster Name': cluster_name,
                    'Fitness': fitness,
                    'Cluster Size': len(cluster_data)
                })

        # Sort the results by fitness in descending order and keep top 10
        self.results = sorted(self.results, key=lambda x: x['Fitness'], reverse=True)[:10]

    # Function to display results
    def display_results(self):
        table = PrettyTable()
        table.field_names = ["Cluster Name", "Fitness (%)", "Cluster Size"]
        for result in self.results:
            table.add_row([
                result['Cluster Name'],
                f"{result['Fitness']:.2f}",
                result['Cluster Size']
            ])
        print(table)

    def plot_clusters(self):
        random_cols = self.get_random_cols()
        subset_df = self.training_data[random_cols].replace([np.inf, -np.inf], np.nan).dropna()
        
        if subset_df.empty:
            return  # Skip if no data left after dropping NaNs
        
        # Add the target column (ensure it is aligned with the subset_df)
        target = self.training_data[self.target]
        subset_df[self.target] = target[subset_df.index]

        # Apply DBSCAN clustering
        dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        labels = dbscan.fit_predict(subset_df.drop(columns=[self.target]))
        
        # Apply PCA for dimensionality reduction
        pca = PCA(n_components=2)
        pca_transformed = pca.fit_transform(subset_df.drop(columns=[self.target]))
        
        # Plot the clusters with target color
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(pca_transformed[:, 0], pca_transformed[:, 1], c=subset_df[self.target], cmap='viridis')
        plt.colorbar(scatter, label='Target Value')
        
        plt.title(f'DBSCAN Clusters in {random_cols}')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.show()


