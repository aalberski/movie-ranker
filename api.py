#api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import update_elo, get_pair, movie_leaderboard
from fastapi.middleware.cors import CORSMiddleware


# Build an API
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get('/')
def root():
    return {'Movie Ranker'}

@app.get('/pair')
def fetch_pair():
    return get_pair('movie_ranker.db')

@app.post('/vote')
def vote_pair(winner: int, loser: int):
    update_elo('movie_ranker.db', winner, loser)
    return {'Winner: ' + str(winner)}

@app.get('/leaderboard')
def get_leaderboard():
    return movie_leaderboard('movie_ranker.db')