# Adam Alberski
# 9/4/2026
# movie-ranker

import json
import sys
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import sqlite3
from rich import print

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
df = pd.read_csv('watched.csv')
conn = sqlite3.connect('movie_ranker.db')

# Create the movie table
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        adult BOOLEAN,
        backdrop_path TEXT,
        genre_ids TEXT,
        tmdb_id INTEGER UNIQUE,
        title TEXT NOT NULL,
        original_language TEXT,
        original_title TEXT,
        overview TEXT,
        popularity REAL,
        poster_path TEXT,
        release_date TEXT,
        softcore BOOLEAN,
        video BOOLEAN,
        vote_average REAL,
        vote_count INTEGER,
        elo_rating REAL DEFAULT 1500,
        comparisons_count INTEGER DEFAULT 0
    )
    """
)

# Create the comparisons table
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS comparisons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_a_id INTEGER NOT NULL,
        movie_b_id INTEGER NOT NULL,
        winner_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
)

# Loop through the movie csv file
for index, row in df.iterrows():
    try:
            title = row['Name']
            year = row['Year']
            response = requests.get("https://api.themoviedb.org/3/search/movie", params = {"api_key": api_key, "query": title, "year": year}).json()['results']
            filtered_response = [r for r in response if r['title'] == title and r['release_date'].startswith(str(year))]
            movie_response = filtered_response[0]
            print(movie_response['title'])
            conn.execute(
                """
                    INSERT INTO movies(adult, backdrop_path, genre_ids, tmdb_id, title, original_language, original_title, overview, popularity, poster_path, release_date, softcore, video, vote_average, vote_count)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (movie_response['adult'], movie_response['backdrop_path'], json.dumps(movie_response['genre_ids']), movie_response['id'], movie_response['title'], movie_response['original_language'], movie_response['original_title'], movie_response['overview'], movie_response['popularity'], movie_response['poster_path'], movie_response['release_date'], movie_response['softcore'], movie_response['video'], movie_response['vote_average'], movie_response['vote_count'])
            )
    except:
        print('Failed to find ',  row['Name'])


conn.commit()
conn.close()



