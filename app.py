import streamlit as st
from PIL import Image
import json
import requests
import io
from urllib.request import urlopen
from bs4 import BeautifulSoup
from Classifier import KNearestNeighbours  # Our new clean KNN class

# ========================== LOAD DATA ==========================
@st.cache_data
def load_data():
    with open('movie_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('movie_titles.json', 'r', encoding='utf-8') as f:
        titles = json.load(f)
    return data, titles

data, movie_titles = load_data()
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# ========================== HELPER FUNCTIONS ==========================
def movie_poster_fetcher(imdb_link):
    try:
        response = requests.get(imdb_link, headers=hdr, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find("meta", property="og:image")
        if meta_tag and meta_tag.get("content"):
            img_url = meta_tag["content"]
            img_data = urlopen(img_url).read()
            image = Image.open(io.BytesIO(img_data))
            image = image.resize((180, 260))
            st.image(image, use_container_width=False)
    except:
        st.caption("Poster not available")

def get_movie_info(imdb_link):
    try:
        response = requests.get(imdb_link, headers=hdr, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Description
        desc_tag = soup.find("meta", property="og:description")
        if desc_tag:
            parts = desc_tag["content"].split(".")
            director = parts[0].strip() if len(parts) > 0 else "Director: N/A"
            cast = "Cast: " + parts[1].replace("With", "").strip() if len(parts) > 1 else "Cast: N/A"
            story = "Story: " + parts[2].strip() + "." if len(parts) > 2 else "Story: N/A"
        else:
            director = cast = story = "Info not found"

        # Rating count
        rating_span = soup.find("span", class_="sc-bde20123-1 iZlgcd")
        rating_count = rating_span.text if rating_span else "N/A"

        return director, cast, story, f"User Ratings: {rating_count}"
    except:
        return "Director: N/A", "Cast: N/A", "Story: N/A", "User Ratings: N/A"

# ========================== RECOMMENDER FUNCTION ==========================
def KNN_Movie_Recommender(test_point, k=10):
    """
    Returns k most similar movies using our custom KNN
    """
    model = KNearestNeighbours(data=data, test_point=test_point, k=k)
    indices = model.get_k_nearest()  # List of movie indices

    recommendations = []
    for idx in indices:
        title = movie_titles[idx][0]
        link = movie_titles[idx][2]
        rating = data[idx][-1]  # IMDb score
        recommendations.append((title, link, rating))
    return recommendations

# ========================== STREAMLIT UI ==========================
st.set_page_config(page_title="Movie Recommender", page_icon="film", layout="centered")

# Header
col1, col2 = st.columns([1, 4])
with col1:
    try:
        logo = Image.open('bg2.jpg')
        st.image(logo, width=120)
    except:
        st.error("Logo not found")
with col2:
    st.title("Movie Recommender System")
    st.markdown("*Powered by IMDb 5000 Dataset • KNN from Scratch*")

st.markdown("---")

genres_list = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
               'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror',
               'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance',
               'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

movie_names = [m[0] for m in movie_titles]
category = st.selectbox("Choose Recommendation Type", ["--Select--", "Movie-based", "Genre-based"])

# ======================== MOVIE-BASED ========================
if category == "Movie-based":
    st.subheader("Find movies similar to one you love")
    selected_movie = st.selectbox("Pick a movie", ["--Select--"] + movie_names)

    if selected_movie != "--Select--":
        col1, col2 = st.columns([1, 3])
        with col1:
            fetch_poster = st.checkbox("Show movie posters", value=True)
        with col2:
            n_reco = st.slider("Number of recommendations", 5, 20, 10)

        if st.button("Get Recommendations"):
            idx = movie_names.index(selected_movie)
            test_vector = data[idx][:]  # Full genre + rating vector

            with st.spinner("Finding similar movies..."):
                results = KNN_Movie_Recommender(test_vector, k=n_reco + 1)  # +1 to exclude itself
                results = results[1:]  # Remove the selected movie itself

            st.success(f"Top {n_reco} movies similar to **{selected_movie}**")
            for i, (title, link, rating) in enumerate(results, 1):
                with st.expander(f"{i}. **{title}** • IMDb: {rating} stars"):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if fetch_poster:
                            movie_poster_fetcher(link)
                    with col2:
                        director, cast, story, ratings_count = get_movie_info(link)
                        st.markdown(f"[{title}]({link})")
                        st.caption(director)
                        st.caption(cast)
                        st.caption(story)
                        st.caption(ratings_count)

# ======================== GENRE-BASED ========================
elif category == "Genre-based":
    st.subheader("Discover movies by genre + minimum rating")
    selected_genres = st.multiselect("Select genres (you can pick multiple)", genres_list)
    min_rating = st.slider("Minimum IMDb Rating", 1.0, 10.0, 8.0, 0.1)
    n_reco = st.slider("Number of movies", 5, 20, 10)
    fetch_poster = st.checkbox("Show posters", value=True)

    if st.button("Find Movies") and selected_genres:
        # Build test vector: 1 if genre selected, else 0 + desired min rating
        test_vector = [1 if g in selected_genres else 0 for g in genres_list]
        test_vector.append(min_rating)

        with st.spinner("Searching for best matches..."):
            results = KNN_Movie_Recommender(test_vector, k=n_reco)

        st.success(f"Top {n_reco} movies matching your taste")
        for i, (title, link, rating) in enumerate(results, 1):
            with st.expander(f"{i}. **{title}** • IMDb: {rating} stars"):
                col1, col2 = st.columns([1, 4])
                with col1:
                    if fetch_poster:
                        movie_poster_fetcher(link)
                with col2:
                    director, cast, story, ratings_count = get_movie_info(link)
                    st.markdown(f"[{title}]({link})")
                    st.caption(director)
                    st.caption(cast)
                    st.caption(story)
                    st.caption(ratings_count)

elif category == "--Select--":
    st.info("Please select a recommendation type above to start recommending!")

# Footer
st.markdown("---")
st.caption("Made with love | KNN from scratch | Data: IMDb 5000 Movies Dataset")