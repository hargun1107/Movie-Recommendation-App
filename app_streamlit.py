import streamlit as st
from recommender import load_movies, MovieRecommender

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎥 Movie Recommendation App")

st.write("Type a movie title below and get similar movie suggestions!")

# Load data
movies = load_movies("data/movies.csv")
recommender = MovieRecommender(movies)

movie_title = st.text_input("Enter a movie title (e.g. Toy Story (1995))")

if st.button("Recommend"):
    if not movie_title.strip():
        st.warning("Please enter a movie title.")
    else:
        results = recommender.recommend(movie_title, n=5)
        if len(results) == 0:
            st.error("No movie found with that title. Try typing more precisely.")
        else:
            st.success("Recommended Movies:")
            for _, row in results.iterrows():
                st.write(f"🎬 **{row['title']}** — *{row['genres']}*")
