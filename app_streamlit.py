import streamlit as st
import re
from recommender import load_movies, build_recommender

# ---------------------------------------------------------
# Page settings
# ---------------------------------------------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")


# ---------------------------------------------------------
# CSS for auto Light/Dark mode
# ---------------------------------------------------------
st.markdown("""
<style>

body, .main {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* Dark Mode */
:root {
    --background-color: #0b0b0b;
    --text-color: #ffffff;
    --card-bg: #1f1f1f;
}

/* Light Mode */
@media (prefers-color-scheme: light) {
    :root {
        --background-color: #ffffff;
        --text-color: #000000;
        --card-bg: #f2f2f2;
    }
}

.movie-card {
    background-color: var(--card-bg);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.no-results {
    color: #ff4c4c;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommender App</h1>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Load data + model (CACHED → super fast)
# ---------------------------------------------------------
movies = load_movies("data/movies.csv")
recommender = build_recommender(movies)


# ---------------------------------------------------------
# Input section
# ---------------------------------------------------------
st.subheader("🔍 Find Similar Movies")

movie_list = sorted(movies["title"].unique())

col1, col2 = st.columns([1, 1])

with col1:
    dropdown_choice = st.selectbox("Choose from list:", movie_list)

with col2:
    typed_choice = st.text_input("Or type your movie name:")

movie_title = typed_choice.strip() if typed_choice.strip() else dropdown_choice

recommend_button = st.button("🎥 Recommend")


# ---------------------------------------------------------
# Recommendation logic
# ---------------------------------------------------------
if recommend_button:

    clean_title = re.sub(r"\(\d{4}\)", "", movie_title).strip()

    results = recommender.recommend(clean_title, n=6)

    if len(results) == 0:
        st.markdown(
            "<p class='no-results'>❌ No matches found. Try another title.</p>",
            unsafe_allow_html=True
        )
    else:
        st.balloons()  # 🎉 BALLOONS!

        st.subheader(f"🎞 Recommendations for: **{movie_title}**")

        for _, row in results.iterrows():
            st.markdown(f"""
                <div class='movie-card'>
                    <b>{row['title']}</b><br>
                    <i>{row['genres']}</i>
                </div>
            """, unsafe_allow_html=True)
