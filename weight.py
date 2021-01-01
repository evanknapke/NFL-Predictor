def find_new_weights(home_team, away_team, home_total, away_total, stats, current_weight):
    actual_scores = get_actual_scores(home_team) #dict
    new_weight_home = current_weight
    new_weight_away = current_weight
    for i in range(0,101):
        i = i/100
        home_new_guess = stats['home_avg_pts']*i + stats['away_pts_allowed']*1-i
        away_new_guess = stats['away_avg_pts']*i + stats['home_pts_allowed']*1-i
        if (abs(actual_scores['home'] - home_new_guess) < abs(actual_scores['home'] - home_total)):
            home_total = home_new_guess # new closest score to beat
            new_weight_home = i # new best weight
        if (abs(actual_scores['away'] - away_new_guess) < abs(actual_scores['away'] - away_total)):
            away_total = away_new_guess # new closest score to beat
            new_weight_away = i # new best weight

    # print(away_team + ' @ ' + home_team)
    # # print("Home Weight: " + str(new_weight_home))
    # # print("Away Weight: " + str(new_weight_away))
    # print(away_team + " " + str(away_total))
    # print(home_team + " " + str(home_total))
    # print("\n")

    # TODO: figure out a more accurate new weight for each game rather using the average of all
    return((new_weight_home + new_weight_away) / 2)

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
