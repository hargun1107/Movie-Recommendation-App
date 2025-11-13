import streamlit as st
from recommender import load_movies, MovieRecommender

# ========================= PAGE CONFIG =========================
st.set_page_config(page_title="🎬 Movie Recommender App", layout="wide")

# ========================= CUSTOM TOGGLE SWITCH =========================
toggle_css = """
<style>
.switch {
  position: relative;
  display: inline-block;
  width: 70px;
  height: 34px;
}
.switch input {display:none;}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}
.slider:before {
  position: absolute;
  content: "🌙";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
  text-align: center;
  padding-top: 2px;
  font-size: 16px;
}
input:checked + .slider {
  background-color: #4CAF50;
}
input:checked + .slider:before {
  transform: translateX(36px);
  content: "☀️";
}
</style>
"""

st.markdown(toggle_css, unsafe_allow_html=True)

# Switch widget
theme_switch = st.sidebar.checkbox("Toggle Theme", value=True)
theme = "Dark" if theme_switch else "Light"

# ========================= THEME COLORS =========================
if theme == "Dark":
    background = "#0b0b0b"
    text_color = "#e5e5e5"
    card_color = "#1f1f1f"
    title_color = "#e50914"
    genre_bg = "#222"
    genre_text = "#e50914"
else:
    background = "#f5f5f5"
    text_color = "#111111"
    card_color = "#ffffff"
    title_color = "#c91818"
    genre_bg = "#eee"
    genre_text = "#d90429"

# ========================= CSS =========================
st.markdown(f"""
<style>
    body {{
        background-color: {background};
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
    }}
    .main {{
        background-color: {background};
    }}
    .title {{
        color: {title_color};
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }}
    .movie-card {{
        background-color: {card_color};
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin: 10px;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    .movie-card:hover {{
        transform: scale(1.03);
    }}
    .movie-title {{
        color: {text_color};
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }}
    .genre-tag {{
        display: inline-block;
        background-color: {genre_bg};
        color: {genre_text};
        border-radius: 6px;
        padding: 3px 8px;
        margin: 3px;
        font-size: 12px;
    }}
    .no-results {{
        color: #ff4c4c;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        margin-top: 30px;
    }}
</style>
""", unsafe_allow_html=True)

# ========================= HEADER =========================
st.markdown("<h1 class='title'>🎬 Movie Recommender App</h1>", unsafe_allow_html=True)

# ========================= LOAD MOVIES =========================
movies = load_movies("data/movies.csv")
recommender = MovieRecommender(movies)

# ========================= AUTOCOMPLETE MOVIE LIST =========================
movie_list = sorted(movies['title'].unique())

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 Find Similar Movies")
    movie_title = st.selectbox("Search or choose a movie:", movie_list)

    recommend_button = st.button("🎥 Recommend")

with col2:
    if recommend_button and movie_title.strip():
        with st.spinner("✨ Finding similar movies..."):
            results = recommender.recommend(movie_title, n=6)

        if len(results) == 0:
            st.markdown(
                "<div class='no-results'>❌ No matches found. Try another title.</div>",
                unsafe_allow_html=True
            )
        else:
            st.subheader(f"🎞 Recommendations for **{movie_title.title()}**")
            cols = st.columns(3)

            for i, (_, row) in enumerate(results.iterrows()):
                with cols[i % 3]:
                    st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='movie-title'>{row['title']}</div>", unsafe_allow_html=True)
                    for genre in row['genres'].split('|'):
                        st.markdown(f"<span class='genre-tag'>{genre}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            st.success("✅ Recommendations loaded!")
            st.balloons()
