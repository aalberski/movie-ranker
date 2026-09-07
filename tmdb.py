# Adam Alberski

import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

def search_movie(title, year):
    try:
        response = requests.get("https://api.themoviedb.org/3/search/movie", params = {"api_key": api_key, "query": title, "year": year}).json()['results']
        filtered_response = [r for r in response if r['title'] == title and r['release_date'].startswith(str(year))]
        movie_response = filtered_response[0]
        return movie_response
    except:
        return None