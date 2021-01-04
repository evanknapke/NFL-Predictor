import constants

def find_new_weights(home_team, away_team, predictions, stats):
    actual_scores = get_actual_scores(home_team) # TODO: search home and away when web scrape is implemented
    new_weight_home = constants.AVG_PTS_WEIGHT
    new_weight_away = constants.AVG_PTS_WEIGHT

    # trying new weights (0.0, 0.1, ..., 0.99, 1.0) to see if it results in a closer result to the actual scores
    for w in range(0,101):
        w = w/100
        home_new_guess = stats['home_avg_pts']*w + stats['away_pts_allowed']*1-w
        away_new_guess = stats['away_avg_pts']*w + stats['home_pts_allowed']*1-w
        if (abs(actual_scores['home'] - home_new_guess) < abs(actual_scores['home'] - predictions['home_score'])):
            home_total = home_new_guess # new closest score to beat
            new_weight_home = w # new best weight
        if (abs(actual_scores['away'] - away_new_guess) < abs(actual_scores['away'] - predictions['away_score'])):
            away_total = away_new_guess # new closest score to beat
            new_weight_away = w # new best weight

    return {
            'new_weight_home': new_weight_home,
            'new_weight_away': new_weight_away
           }

# TODO: pull actual scores from web or api
# TODO: use more data; only sunday of week 16 data currently used for training
def get_actual_scores(home_team):
    if (home_team == 'Kansas City'):
        away = 14
        home = 17
    elif (home_team == 'NY Jets'):
        away = 16
        home = 23
    elif (home_team == 'Pittsburgh'):
        away = 24
        home = 28
    elif (home_team == 'Jacksonville'):
        away = 41
        home = 17
    elif (home_team == 'Baltimore'):
        away = 13
        home = 27
    elif (home_team == 'Houston'):
        away = 37
        home = 31
    elif (home_team == 'LA Chargers'):
        away = 16
        home = 19
    elif (home_team == 'Washington'):
        away = 20
        home = 13
    elif (home_team == 'Dallas'):
        away = 17
        home = 37
    elif (home_team == 'Seattle'):
        away = 9
        home = 20
    elif (home_team == 'Green Bay'):
        away = 14
        home = 40

    return {"home": home, "away": away}
