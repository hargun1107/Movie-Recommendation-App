import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def load_movies(path="data/movies.csv"):
    movies = pd.read_csv(path)
    movies["genres"] = movies["genres"].fillna("")
    movies["combined"] = movies["title"] + " " + movies["genres"].str.replace("|", " ")
    return movies


class MovieRecommender:
    def __init__(self, movies_df):
        self.movies = movies_df

        # TF-IDF
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(movies_df["combined"])
        self.similarity = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

        # Clean titles (remove year)
        self.movies["clean_title"] = self.movies["title"].apply(
            lambda x: re.sub(r"\(\d{4}\)", "", str(x)).strip().lower()
        )

        # Index for lookup
        self.indices = pd.Series(self.movies.index, index=self.movies["clean_title"]).drop_duplicates()

    def recommend(self, title, n=5):
        title = title.lower().strip()

        # Title not exact → try partial matching
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
