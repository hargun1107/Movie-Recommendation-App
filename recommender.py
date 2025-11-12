import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def load_movies(path="data/movies.csv"):
    movies = pd.read_csv(path)
    movies['genres'] = movies['genres'].fillna('')
    # Combine title and genres for similarity
    movies['combined'] = movies['title'] + ' ' + movies['genres'].str.replace('|', ' ')
    return movies


class MovieRecommender:
    def __init__(self, movies_df):
        self.movies = movies_df
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(movies_df['combined'])
        self.similarity = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

        # Clean titles: remove years and lowercase them
        self.movies['clean_title'] = self.movies['title'].apply(
            lambda x: re.sub(r'\(\d{4}\)', '', str(x)).strip().lower()
        )
        # Build index for fast lookup
        self.indices = pd.Series(self.movies.index, index=self.movies['clean_title']).drop_duplicates()

    def recommend(self, title, n=5):
        title = title.lower().strip()

        # Check if exact or partial match exists
        if title not in self.indices:
            possible_matches = [t for t in self.indices.index if title in t]
            if len(possible_matches) == 0:
                return []
            title = possible_matches[0]  # take first match

        idx = self.indices[title]
        # Enumerate to get (movie_index, similarity_score)
        scores = list(enumerate(self.similarity[idx].flattern().tolist()))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        movie_indices = [i[0] for i in scores[1:n + 1]]

        return self.movies.iloc[movie_indices][['title', 'genres']]
