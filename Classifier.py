# Classifier.py
# Custom K-Nearest Neighbors for Movie Recommendation (Regression-style: returns nearest movies)
# Works perfectly with app.py

import numpy as np

class KNearestNeighbours:
    def __init__(self, data, test_point, k=10):
        """
        data        : list of lists (each movie = [genre1, genre2, ..., imdb_score])
        test_point  : list (same format as data rows)
        k           : number of nearest neighbors to return
        """
        self.data = np.array(data)           # All movie feature vectors
        self.test_point = np.array(test_point)
        self.k = k
        self.indices = None                  # Will store indices of k nearest movies

    @staticmethod
    def euclidean_distance(p1, p2):
        """Correct Euclidean distance between two vectors"""
        return np.sqrt(np.sum((p1 - p2) ** 2))

    def fit(self):
        """Find the k nearest movies to the test_point"""
        distances = []
        
        for idx, movie_vector in enumerate(self.data):
            dist = self.euclidean_distance(self.test_point, movie_vector)
            distances.append((dist, idx))
        
        # Sort by distance (ascending)
        distances.sort(key=lambda x: x[0])
        
        # Keep only top k
        self.indices = [idx for _, idx in distances[:self.k]]
        
        return self.indices

    def get_k_nearest(self):
        """Returns list of indices of k nearest movies"""
        if self.indices is None:
            self.fit()
        return self.indices