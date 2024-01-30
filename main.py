from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

# extracting important information from dataframe
allmovies = movies_data[["original_title", "poster_link", "release_date", "runtime", "weighted_rating"]]

# variables to store data
likedMovies = []
disliked_movies = []
not_watched = []
# method to fetch data from database
def assignValue():
  mdata = {
    "original_title": allmovies.iloc[0, 0],
    "poster_link": allmovies.iloc[0, 1],
    "release_date": allmovies.iloc[0, 2],
    "runtime": allmovies.iloc[0, 3],
    "weighted_rating": allmovies.iloc[0, 4]

  }
  return mdata

# /movies api
@app.route("/movies")
def getMovie():
  movieData = assignValue()
  return jsonify({
    "data": movieData,
    "status": "success"

  })


# /like api
@app.route("/like")
def liked():
  global allmovies
  movie_data = assignValue()
  likedMovies.append(movie_data)
  allmovies.drop([0], inplace=True)
  allmovies = allmovies.reset_index(drop=True)
  return jsonify({
    "status": "success"
  })


# /dislike api
@app.route("/dislike")
def disliked():
  global allmovies
  movie_data = assignValue()
  disliked_movies.append(movie_data)
  allmovies.drop([0], inplace=True)
  allmovies = allmovies.reset_index(drop=True)
  return jsonify({
    "status": "success"
  })


# /did_not_watch api
@app.route("/notWatch")
def DidNotWatch():
  global allmovies
  movie_data = assignValue()
  not_watched.append(movie_data)
  allmovies.drop([0], inplace=True)
  allmovies = allmovies.reset_index(drop=True)
  return jsonify({
      "status": "success"
  })

@app.route('/popularMovies')
def popularMovies() :
  popularMovieData = []
  for index, row in output.iterrows():
    p = {
      "original_title" : row['original_title'],
      "poster_link": row['poster_link'],
      "release_date": row['release_date'] or "NA",
      "duration": row['runtime'],
      "Rating": row['weighted_rating']

    }
    popularMovieData.append(p)
  return jsonify({
    "data" : popularMovieData,
    "status" : "success 200"
  })

@app.route('/reccommendation')
def reccommended_movies():
  global likedMovies
  columnNames = ['original_title', 'poster_link', 'release_date', 'duration', 'rating']
  allreccommended = pd.DataFrame(columns = columnNames)
  for i in likedMovies:
    output = get_recommendations(i["original_title"])
    allreccommended = allreccommended._append(output)
  allreccommended.drop_duplicates(subset=['original_title'], inplace=True)
  reccommendedMovieData = []
  print(allreccommended)
  for index, row in allreccommended.iterrows():
    p = {
      "original_title" : row['original_title'],
      "poster_link": row['poster_link'],
      "release_date": row['release_date'] or "NA",
      "duration": row['runtime'],
      "Rating": row['weighted_rating']

    }
    reccommendedMovieData.append(p)
  return jsonify({
    "data" : reccommendedMovieData,
    "status" : "success 200"
  })
  


if __name__ == "__main__":
  app.run()