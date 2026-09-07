K = 32

def expected_score(a, b):
    return 1 / (1 + 10**((b - a)/400))

def update_ratings(winner, loser):
    # winner
    winner_expected = expected_score(winner, loser)
    winner_rating = winner + K * (1 - winner_expected)

    # loser
    loser_expected = expected_score(loser, winner)
    loser_rating = loser + K * (0 - loser_expected)

    return([winner_rating, loser_rating])
