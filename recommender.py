import pandas as pd
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def load_movies(path="data/movies.csv"):
    """Load and preprocess the movies dataset."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, path)

    movies = pd.read_csv(path)
    movies['genres'] = movies['genres'].fillna('')  # Replace missing genres
    movies['combined'] = movies['title'] + ' ' + movies['genres'].str.replace('|', ' ')  # Combine for TF-IDF
    return movies


class MovieRecommender:
    """A simple content-based movie recommender using TF-IDF and cosine similarity."""

    def __init__(self, movies_df):
        self.movies = movies_df

        # Convert text data (title + genres) into TF-IDF vectors
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(movies_df['combined'])

        # Compute cosine similarity matrix between all movies
        self.similarity = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

        # Clean movie titles: remove year and lowercase them for better matching
        self.movies['clean_title'] = self.movies['title'].apply(
            lambda x: re.sub(r'\(\d{4}\)', '', str(x)).strip().lower()
        )

        # Create a reverse lookup index: title → dataframe index
        self.indices = pd.Series(self.movies.index, index=self.movies['clean_title']).drop_duplicates()

    def recommend(self, title, n=5):
        """Return top-N similar movies based on a given title."""

        # Validate input
        if not isinstance(title, str) or len(title.strip()) == 0:
            return []

        title = title.lower().strip()

        # If exact match not found, try to find partial matches
        if title not in self.indices:
            possible_matches = [t for t in self.indices.index if title in t]
            if not possible_matches:
                return []
            title = possible_matches[0]

        # Get movie index and similarity scores
        idx = self.indices[title]
        scores = list(enumerate(self.similarity[idx].flatten().tolist()))

        # Sort by similarity score (highest first)
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        # Get top N most similar movies
        movie_indices = [i[0] for i in scores[1:n + 1]]

        # Ensure indices are valid
        movie_indices = [i for i in movie_indices if i < len(self.movies)]

        if not movie_indices:
            return []

        # Return only movie titles and genres for display
        return self.movies.iloc[movie_indices][['title', 'genres']]
