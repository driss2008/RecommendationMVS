import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:7]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

logo_path = 'f.jpg'
st.image(logo_path, use_column_width=True)

st.header('Movie Recommender System')
movie_dict= pickle.load(open('movie_list.pkl','rb'))
movies=pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    num_cols = 3  # Adjust the number of columns as per your preference
    col_width = 200  # Adjust this value to change column width and image size

    # Calculate the number of rows needed based on the number of movies
    num_rows = (len(recommended_movie_names) - 1) // num_cols + 1

    # Create a list of columns
    cols = st.columns(num_cols)

    # Iterate through the movies and display them in the columns
    for i in range(len(recommended_movie_names)):
        with cols[i % num_cols]:
            st.markdown(f"***{recommended_movie_names[i]}***")
            st.image(recommended_movie_posters[i], width=col_width) 