# Adam Alberski
# 9/4/2026
# movie-ranker

import pandas as pd
from db import build_db
from db import update_elo

# Read the CSV file
df = pd.read_csv('watched.csv')

# Build a database
build_db(df.head(5), 'movie_ranker.db')
# build_db(df, 'movie_ranker.db')

update_elo('movie_ranker.db', 1, 2)

