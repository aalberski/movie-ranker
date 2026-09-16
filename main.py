# Adam Alberski
# 9/4/2026
# movie-ranker

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
import pandas as pd
from db import build_db#, update_elo, get_pair, movie_leaderboard

# Read the CSV file
df = pd.read_csv('watched.csv')

# Build a database
build_db(df.head(5), 'movie_ranker.db')
# build_db(df, 'movie_ranker.db')