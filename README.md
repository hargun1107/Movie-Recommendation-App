# 🎬 Movie Recommender App

A simple yet powerful content-based movie recommendation system built with Python, Pandas, Scikit-Learn, and Streamlit.
This app allows users to search for any movie and instantly receive personalized movie recommendations based on genre and title similarity.

🚀 Features:

🔍 Smart Movie Search

1. Choose from a dropdown list of all movie titles
2. Or type your movie name manually
3. The system automatically picks the user’s manual input if both fields are filled

🎯 Accurate Content-Based Recommendations

1. Uses TF-IDF Vectorization
2. Computes movie similarity using cosine similarity
3. Removes year from titles automatically for better matching
4. Handles partial matches (e.g., typing “toy stor” finds Toy Story)

🎨 Modern UI with Auto Light/Dark Mode

1. Automatically detects system theme
2. Smooth visuals designed with custom CSS
3. Movie results displayed inside clean movie cards
4. ❌ Error message for unmatched titles
5. 🎈 Balloons animation when recommendations succeed

📦 Fully Deployable

1. Runs locally
2. 100% compatible with Streamlit Cloud
3. Works even without API keys (since the poster API was removed)

🧠 How It Works

The app uses a content-based filtering model:
1. Loads the movies.csv dataset
2. Cleans movie titles and combines them with genre info
3. Transforms movie descriptions using TF-IDF Vectorizer
4. Computes similarity scores between movies
5. Returns the top recommended movies for any chosen title

No user data, accounts, or ratings required.

🛠️ Tech Stack
Component:	Technology Used
App Framework:	Streamlit
ML / NLP:	Scikit-Learn (TF-IDF Vectorizer + Cosine Similarity)
Data Processing:	Pandas, NumPy
Deployment:	Streamlit Cloud
Styling:	Custom CSS + Auto Theme Detection

📡 Live Demo (Test the App Online)

The Movie Recommendation App is live and accessible online using Streamlit Cloud.

👉 Try the live demo here:
🔗 https://movie-recommendation-app-exbzknddpwagjzmzbkjwa4.streamlit.app/

📞 Contact

If you have any questions or suggestions:

📧 LinkedIn: http://www.linkedin.com/in/hargun-kohli-124378346

🔗 GitHub: http://www.linkedin.com/in/hargun-kohli-124378346