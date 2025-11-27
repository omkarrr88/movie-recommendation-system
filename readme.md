# Movie Recommender System  
**"Because you watched Inception..." – Built from scratch with love**

A smart, fast, and beautiful movie recommendation web app powered by **K-Nearest Neighbors (KNN)** implemented **without scikit-learn**.  
Recommends movies in two ways:
- **Movie-based**: "If you liked this movie, here are 10 similar ones"
- **Genre-based**: "Show me high-rated Action + Sci-Fi + Thriller movies"

---

### Features
- 5000+ movies from the famous **IMDb 5000 Movie Dataset**
- Custom **KNN algorithm from scratch** (no scikit-learn!)
- Fetches **real posters, director, cast, plot, and rating count** live from IMDb
- Two recommendation modes: Movie-based & Genre-based
- Clean, modern UI built with **Streamlit**
- Lightning fast with NumPy optimization
- 100% offline data (JSON) – no database needed

---

### Tech Stack
| Technology       | Purpose                     |
|------------------|-----------------------------|
| Python           | Core language               |
| Streamlit        | Web interface               |
| NumPy            | Fast distance calculations  |
| BeautifulSoup    | Scrape IMDb posters/info    |
| PIL (Pillow)     | Image processing            |
| JSON             | Local movie database        |

---

### How to Run Locally (30 seconds)

```bash
# 1. Clone the repo

# 2. Install dependencies
pip install streamlit pillow beautifulsoup4 requests numpy

# 3. Run the app
streamlit run app.py
```

Open your browser → **http://localhost:8501**  
Enjoy recommending!

---

### Project Structure
```
movie-recommender/
├── app.py                  # Main Streamlit app (updated & clean)
├── Classifier.py           # Custom KNN class (from scratch)
├── movie_data.json         # Preprocessed movie features (genres + rating)
├── movie_titles.json       # Movie titles + IMDb links
├── bg2.jpg                 # Logo / background
├── screenshot.png          # For README (optional)
└── README.md               # This file
```

---

### Deploy for Free on Streamlit Community Cloud (2 minutes)

1. Push your code to GitHub
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Connect your GitHub repo → select `app.py` → Deploy!

You’ll get a free public URL like:  
`https://yourusername-movie-recommender.streamlit.app`

---

### Dataset Source
- [Kaggle: IMDb 5000 Movie Dataset](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset)
- Preprocessed and cleaned for this project


### Made with ❤️ by [Your Name]
**Star this repo if you liked it!**  
Feel free to fork, improve, and share

---
**"Good movies aren't found. They're recommended."**
```
