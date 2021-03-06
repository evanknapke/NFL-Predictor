import constants
import os
import pandas as pd
import requests
import sys
import train

def main():
    # create dataframes
    if (constants.GET_NEW_WEIGHTS):
        matchups_df = save_to_df(constants.TRAINING_SCHEDULE_URL)
        new_weight = 0.0
        correct_ml = 0
    else:
        matchups_df = save_to_df(constants.UPCOMING_SCHEDULE_URL)
    pts_df = save_to_df(constants.AVG_PTS_URL)
    pts_allowed_df = save_to_df(constants.AVG_PTS_ALLOWED_URL)

    amount_of_games = matchups_df.shape[0]

    for i in range(amount_of_games): # length of rows in df
        try:
            # search for team by name, index 1 is home teams column, index 0 is away teams column
            home_team_raw = matchups_df.iloc[i][1]
            away_team_raw = matchups_df.iloc[i][0]

            home_team = clean_name(home_team_raw)
            away_team = clean_name(away_team_raw)

            stats = get_matchup_stats(home_team, away_team, pts_df, pts_allowed_df)
            prediction = get_prediction(home_team, away_team, stats)

            if (not constants.GET_NEW_WEIGHTS): # displaying or training
                if (constants.SAVE_TO_TXT):
                    # saving results to .txt file in ./out/ folder
                    filename = './out/'+constants.FILENAME+'.txt'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    sys.stdout = open(filename, 'a')
                    display_prediction(home_team, away_team, prediction)
                    sys.stdout.close()
                else:
                    # displaying results to console
                    display_prediction(home_team, away_team, prediction)
            else:
                # for training
                result = matchups_df.iloc[i][2]
                new_weight += train.find_new_weights(home_team_raw, away_team_raw, prediction, stats, result)
                correct_ml += train.grade_moneyline(home_team_raw, away_team_raw, prediction, result)
        except IndexError:
            # happens when there is something other then a team in the columns
            # example: "AFC Wild Card Playoffs" header
            amount_of_games -= 1 # decrement the amount of rows since this instance was not a valid game
            pass

    if (constants.GET_NEW_WEIGHTS):
        display_new_weights(new_weight, amount_of_games)
        print("Current ML Win Percentage: " + str( (correct_ml / amount_of_games)*100) + '%')


def save_to_df(url):
    r = requests.get(url)
    df_list = pd.read_html(r.text) # parses all the tables in webpage to a list
    df = pd.concat(df_list) # concatenates all tables on page together into 1 dataframe
    return df

def get_matchup_stats(home_team, away_team, pts_df, pts_allowed_df):
    # get index of home and away team in the pts_df
    home_i = pts_df[pts_df['Team'] == home_team].index[0]
    away_i = pts_df[pts_df['Team'] == away_team].index[0]

    # get avg points of each team using the index
    home_avg_pts = pts_df.iloc[home_i]['2020']
    away_avg_pts = pts_df.iloc[away_i]['2020']

    # get index of home and away team in the pts_allowed_df
    home_i = pts_allowed_df[pts_allowed_df['Team'] == home_team].index[0]
    away_i = pts_allowed_df[pts_allowed_df['Team'] == away_team].index[0]

    # get avg points of each team using the index
    home_pts_allowed = pts_allowed_df.iloc[home_i]['2020']
    away_pts_allowed = pts_allowed_df.iloc[away_i]['2020']

    return {
            "home_avg_pts": home_avg_pts,
            "away_avg_pts": away_avg_pts,
            "home_pts_allowed": home_pts_allowed,
            "away_pts_allowed": away_pts_allowed
           }

def get_prediction(home_team, away_team, stats):
    home_score = stats['home_avg_pts']*constants.AVG_PTS_WEIGHT + stats['away_pts_allowed']*constants.AVG_PTS_ALLOWED_WEIGHT
    away_score = stats['away_avg_pts']*constants.AVG_PTS_WEIGHT + stats['home_pts_allowed']*constants.AVG_PTS_ALLOWED_WEIGHT
    spread = round(abs(home_score - away_score), constants.SPREAD_DECIMALS)

    # round after spread is configured for spread's accuracy
    home_score = round(home_score, constants.SCORE_DECIMALS)
    away_score = round(away_score, constants.SCORE_DECIMALS)

    # cast float to int if rounding to whole number
    if (constants.SCORE_DECIMALS == 0):
        home_score = int(home_score)
        away_score = int(away_score)
    if (constants.SPREAD_DECIMALS == 0):
        spread = int(spread)

    return {
            "away_score": away_score,
            "home_score": home_score,
            "spread": spread
           }

def display_prediction(home_team, away_team, prediction):
    # decide who the favorite is for the spread symbols
    spread = str(prediction['spread'])
    if (prediction['home_score'] > prediction['away_score']):
        home_spread = '(-' + spread + ')'
        away_spread = '(+' + spread + ')'
    else:
        home_spread = '(+' + spread + ')'
        away_spread = '(-' + spread + ')'

    print(away_team +' @ '+ home_team)
    print( '{:<6s} {:<15s} {:<5s}'.format(away_spread, away_team, str(prediction['away_score'])) )
    print( '{:<6s} {:<15s} {:<5s}'.format(home_spread, home_team, str(prediction['home_score'])) )
    print( '{:<22s} {:<5s}'.format('Combined Score ', str(prediction['home_score'] + prediction['away_score'])) )
    print('\n')

# TODO: update so this divides by games in train.py
def display_new_weights(new_weight, amount_of_games):
    new_weight = new_weight / amount_of_games
    print('New Weight:  ' + str( (new_weight) / 2)) # divide by 2 because it is taking the average weight for home and away team

def clean_name(team):
    # special cases (teams share a city and are listed differently on the sites)
    if team == 'Los Angeles LAC':
        return 'LA Chargers'
    elif team == 'Los Angeles LAR':
        return 'LA Rams'
    elif team == 'Los Angeles LAC':
        return 'LA Chargers'
    elif team == 'Los Angeles LAR':
        return 'LA Rams'
    elif team == 'New York NYG':
        return 'NY Giants'
    elif team == 'New York NYJ':
        return 'NY Jets'

    else:
        return team[:-3].strip() # just remove abbreviation if not a special case

main()
