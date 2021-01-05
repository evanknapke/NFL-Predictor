import constants
import re

# TODO: use more data then just 1 week
def find_new_weights(home_team, away_team, predictions, stats, result):
    actual_scores = get_actual_scores(home_team, away_team, result)
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

    return new_weight_home + new_weight_away

def get_actual_scores(home_team, away_team, result):
    away_abbreviation = away_team.split()[-1]
    home_abbreviation = home_team.split()[-1]
    if (away_abbreviation in result and home_abbreviation in result):
        scores = re.findall(r'\d+', result) # extract scores

    # differentiate between home and away scores
    if result.split()[0] == home_abbreviation and scores[0] > scores[1]:
        home = int(scores[0])
        away = int(scores[1])
    else:
        home = int(scores[1])
        away = int(scores[0])

    return {"home": home, "away": away}

# TODO: grade new weight automatically
# if ml is guessed correctly add 1
def grade_moneyline(home_team, away_team, prediction, result):
    actual_scores = get_actual_scores(home_team, away_team, result)

    if prediction['home_score'] > prediction['away_score']:
        predicted_winner = home_team
    elif prediction['home_score'] < prediction['away_score']:
        predicted_winner = away_team
    else:
        predicted_winner = 'TIE'

    if actual_scores['home'] > actual_scores['away']:
        actual_winner = home_team
    elif actual_scores['home'] < actual_scores['away']:
        actual_winner = away_team
    else:
        actual_winner = 'TIE'

    if predicted_winner == actual_winner:
        correct = 1
    else:
        correct = 0

    return correct
