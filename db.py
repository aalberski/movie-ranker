import sqlite3
from tmdb import search_movie
from elo import update_ratings
from datetime import datetime
import json

def create_tables(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elo_rating REAL DEFAULT 1500,
            comparisons_count INTEGER DEFAULT 0,
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
            vote_count INTEGER
        )
        """
    )

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

    conn.commit()

def build_db(datafile, database):
    conn = sqlite3.connect(database)
    create_tables(conn)

    for index, row in datafile.iterrows():
        try:
            movie_response = search_movie(row['Name'], row['Year'])
            # print(movie_response['title'])
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

def get_pair(database):
    conn = sqlite3.connect(database)
    conn.row_factory= sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, poster_path FROM movies ORDER BY comparisons_count ASC, RANDOM() LIMIT 2
        """
    )
    x = cursor.fetchone()
    y = cursor.fetchone()
    return dict(x), dict(y)

def update_elo(db, winner, loser):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Fetch current winner ELO
    cursor.execute("SELECT id, elo_rating, comparisons_count FROM movies WHERE id = ?", (winner,))
    winner_row = cursor.fetchone()

    # Fetch current loser ELO 
    cursor.execute("SELECT id, elo_rating, comparisons_count FROM movies WHERE id = ?", (loser,))
    loser_row = cursor.fetchone()

    new_elo = update_ratings(winner_row[1], loser_row[1])

    # Update winner ELO
    cursor.execute("UPDATE movies SET elo_rating = ?, comparisons_count = ? WHERE id = ?", (new_elo[0], winner_row[2] + 1, winner))

    # Update loser ELO
    cursor.execute("UPDATE movies SET elo_rating = ?, comparisons_count = ? WHERE id = ?", (new_elo[1], loser_row[2] + 1, loser))

    # Update comparisons table
    cursor.execute("INSERT INTO comparisons(movie_a_id, movie_b_id, winner_id, timestamp) VALUES(?,?,?,?)", (winner, loser, winner, str(datetime.now().time())))

    conn.commit()
    conn.close()

def movie_leaderboard(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title FROM movies ORDER BY elo_rating DESC
        """
    )
    rows = cursor.fetchall()
    leaderboard = rows
        
    print(leaderboard)
    return leaderboard