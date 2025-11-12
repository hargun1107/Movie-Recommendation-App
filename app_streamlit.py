import streamlit as st
import os
import traceback

st.set_page_config(page_title="🎬 Movie Recommender - Debug Mode", layout="wide")

st.markdown("""
    <h1 style='text-align:center; color:#e50914;'>🎬 Movie Recommender - Debug Mode</h1>
    <p style='text-align:center; color:#aaa;'>This version helps identify deployment issues on Streamlit Cloud.</p>
""", unsafe_allow_html=True)

try:
    # === Step 1: Import recommender safely ===
    st.write("🔍 Importing recommender module...")
    from recommender import load_movies, MovieRecommender
    st.success("✅ Successfully imported recommender.py")

    # === Step 2: Check current working directory ===
    cwd = os.getcwd()
    st.write(f"📁 Current working directory: `{cwd}`")

    # === Step 3: Check if 'data' folder exists ===
    data_path = os.path.join(cwd, "data")
    if not os.path.exists(data_path):
        st.warning(f"⚠️ 'data' folder not found at: `{data_path}`")
    else:
        files = os.listdir(data_path)
        st.info(f"📂 Contents of /data: {files}")

    # === Step 4: Load movies ===
    st.write("🎞 Attempting to load movies.csv ...")
    movies = load_movies("movies.csv") if os.path.exists("movies.csv") else load_movies("data/movies.csv")
    st.success(f"✅ Loaded {len(movies)} movies successfully!")

    # === Step 5: Initialize recommender ===
    recommender = MovieRecommender(movies)
    st.success("✅ Recommender model initialized successfully!")

    # === Step 6: Test Recommend Function ===
    test_movie = "toy story"
    st.write(f"🎬 Testing recommendation for: **{test_movie.title()}**")
    results = recommender.recommend(test_movie, n=5)
    st.dataframe(results)

    st.balloons()
    st.success("🎉 Everything loaded successfully! You can now switch back to normal mode.")

except Exception as e:
    st.error("❌ An error occurred while running the app.")
    st.code(str(e), language="python")
    st.markdown("### 🔎 Full Traceback:")
    st.code(traceback.format_exc(), language="python")

    st.markdown("""
    ---
    **ℹ️ Troubleshooting Tips**
    - Ensure `/data/movies.csv` exists in your GitHub repo (case-sensitive)
    - Check that `recommender.py` is in the same directory as this file
    - Verify your `requirements.txt` contains `pandas`, `numpy`, `scikit-learn`, and `streamlit`
    - If you see a secrets error, make sure you added `TMDB_API_KEY` in Streamlit Cloud > App Settings > Secrets
    ---
    """)