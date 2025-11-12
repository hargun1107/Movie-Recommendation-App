import streamlit as st
import requests
from recommender import load_movies, MovieRecommender
import os

# ========== CONFIG ==========
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    body {
        background-color: #0b0b0b;
        color: #e5e5e5;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #0b0b0b;
    }
    .title {
        color: #e50914;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .movie-card {
        background-color: #1f1f1f;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin: 10px;
        transition: transform 0.3s ease;
    }
    .movie-card:hover {
        transform: scale(1.03);
    }
    .movie-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    .genre-tag {
        display: inline-block;
        background-color: #222;
        color: #e50914;
        border-radius: 6px;
        padding: 3px 8px;
        margin: 3px;
        font-size: 12px;
    }
    .no-results {
        color: #ff4c4c;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        margin-top: 30px;
    }
    @media (max-width: 768px) {
        .movie-card {
            margin: 5px;
            padding: 10px;
        }
        .movie-title {
            font-size: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("<h1 class='title'>🎬 Movie Recommender App</h1>", unsafe_allow_html=True)

# ========== LOAD DATA & MODEL ==========
movies = load_movies("data/movies.csv")
recommender = MovieRecommender(movies)


TMDB_API_KEY = st.secrets.get("TMDB_API_KEY") if st.secrets else os.getenv("TMDB_API_KEY")

def get_poster(title):
    """Fetch movie poster using TMDB API."""
    if not TMDB_API_KEY:
        return None
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.quote(title)}"
        response = requests.get(url)
        data = response.json()
        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    return None

# ========== LAYOUT ==========
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 Find Similar Movies")
    movie_title = st.text_input("Enter a movie title:", "")
    
    col_buttons = st.columns(2)
    with col_buttons[0]:
        recommend_button = st.button("🎥 Recommend")
    with col_buttons[1]:
        clear_button = st.button("🧹 Clear")
    
    if clear_button:
        st.experimental_rerun()

with col2:
    if recommend_button and movie_title.strip():
        results = recommender.recommend(movie_title, n=6)
        if len(results) == 0:
            st.markdown("<div class='no-results'>❌ No matches found. Try another title.</div>", unsafe_allow_html=True)
        else:
            st.subheader(f"🎞 Recommendations for **{movie_title.title()}**")
            cols = st.columns(3)
            for i, (_, row) in enumerate(results.iterrows()):
                with cols[i % 3]:
                    poster_url = get_poster(row['title'])
                    st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                    if poster_url:
                        st.image(poster_url, use_container_width=True)
                    st.markdown(f"<div class='movie-title'>{row['title']}</div>", unsafe_allow_html=True)
                    for genre in row['genres'].split('|'):
                        st.markdown(f"<span class='genre-tag'>{genre}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
    elif not movie_title.strip() and recommend_button:
        st.markdown("<div class='no-results'>⚠️ Please enter a movie title.</div>", unsafe_allow_html=True)
