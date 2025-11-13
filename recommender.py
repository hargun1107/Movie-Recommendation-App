import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import streamlit as st


# ---------------------------------------------------------
# Cache movie data so it's loaded once (not every user)
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_movies(path="data/movies.csv"):
    movies = pd.read_csv(path)
    movies["genres"] = movies["genres"].fillna("")
    movies["combined"] = movies["title"] + " " + movies["genres"].str.replace("|", " ")
    return movies


# ---------------------------------------------------------
# Recommender class (unchanged logic)
# ---------------------------------------------------------
class MovieRecommender:
    def __init__(self, movies_df):
        self.movies = movies_df

        # TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(movies_df["combined"])

        # Similarity matrix
        self.similarity = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

        # Clean movie titles (remove year)
        self.movies["clean_title"] = self.movies["title"].apply(
            lambda x: re.sub(r"\(\d{4}\)", "", str(x)).strip().lower()
        )

        # Index lookup table
        self.indices = pd.Series(
            self.movies.index, index=self.movies["clean_title"]
        ).drop_duplicates()

    # Recommendation method
    def recommend(self, title, n=5):
        title = title.lower().strip()

        # If title is not exact, try partial match
        if title not in self.indices:
            matches = [t for t in self.indices.index if title in t]
            if len(matches) == 0:
                return []
            title = matches[0]

        idx = self.indices[title]

        # Compute similarity
        scores = list(enumerate(self.similarity[idx].flatten().tolist()))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        movie_indices = [i[0] for i in scores[1:n + 1]]
        movie_indices = [i for i in movie_indices if i < len(self.movies)]

        if not movie_indices:
            return []

        return self.movies.iloc[movie_indices][["title", "genres"]]


# ---------------------------------------------------------
# Cache the recommender model so it's built only once
# ---------------------------------------------------------
@st.cache_resource(show_spinner=True)
def build_recommender(movies_df):
    return MovieRecommender(movies_df)
