import constants
import os
import pandas as pd
import requests
import sys
import weight

def main():
    # TODO: update save_to_df so you dont need to change when training
    matchups_df = save_to_df(constants.SCHEDULE_URL) # change to save_to_df2 if training
    pts_df = save_to_df(constants.AVG_PTS_URL)
    pts_allowed_df = save_to_df(constants.AVG_PTS_ALLOWED_URL)
    new_weight_home = 0.0 # for training
    new_weight_away = 0.0 # for training
    for i in range(matchups_df.shape[0]): # length of rows in df
        home_team = clean_name(matchups_df.iloc[i][1])
        away_team = clean_name(matchups_df.iloc[i][0])
        stats = get_matchup_stats(home_team, away_team, pts_df, pts_allowed_df)

        predictions = get_predictions(home_team, away_team, stats)
        if (not constants.GET_NEW_WEIGHTS):
            if (constants.SAVE_TO_TXT):
                filename = './out/'+constants.FILENAME+'.txt'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                sys.stdout = open(filename, 'a')
                display_predictions(home_team, away_team, predictions)
                sys.stdout.close()
            else:
                display_predictions(home_team, away_team, predictions)
        else:
            new_weights = weight.find_new_weights(home_team, away_team, predictions, stats)
            new_weight_home += new_weights['new_weight_home']
            new_weight_away += new_weights['new_weight_away']

    if (constants.GET_NEW_WEIGHTS):
        new_weight_home = new_weight_home/matchups_df.shape[0]
        new_weight_away = new_weight_away/matchups_df.shape[0]
        print('New Home Weight: ' + str(new_weight_home))
        print('New Away Weight: ' + str(new_weight_away))
        print('Average Weight:  ' + str( (new_weight_home + new_weight_away) / 2))

# TODO: rewrite these into 1 function to take in all tables on the page
#      or only select the table for the matchups
#      or find new website that works better that puts matchups into one table
def save_to_df(url):
    r = requests.get(url)
    df_list = pd.read_html(r.text) # parses all the tables in webpage to a list
    df = df_list[0] # first table on the page
    df.head()
    return df

def save_to_df2(url):
    r = requests.get(url)
    df_list = pd.read_html(r.text) # parses all the tables in webpage to a list
    df = df_list[2]
    df.head()
    return df

def get_matchup_stats(home_team, away_team, pts_df, pts_allowed_df):
    home_i = pts_df[pts_df['Team'] == home_team].index[0]
    away_i = pts_df[pts_df['Team'] == away_team].index[0]
    home_avg_pts = pts_df.iloc[home_i]['2020']
    away_avg_pts = pts_df.iloc[away_i]['2020']

    home_i = pts_allowed_df[pts_allowed_df['Team'] == home_team].index[0]
    away_i = pts_allowed_df[pts_allowed_df['Team'] == away_team].index[0]
    home_pts_allowed = pts_allowed_df.iloc[home_i]['2020']
    away_pts_allowed = pts_allowed_df.iloc[away_i]['2020']

    return {
            "home_avg_pts": home_avg_pts,
            "away_avg_pts": away_avg_pts,
            "home_pts_allowed": home_pts_allowed,
            "away_pts_allowed": away_pts_allowed
           }

# TODO: clean and fix commented out code
def get_predictions(home_team, away_team, stats):
    home_score = stats['home_avg_pts']*constants.AVG_PTS_WEIGHT + stats['away_pts_allowed']*constants.AVG_PTS_ALLOWED_WEIGHT
    away_score = stats['away_avg_pts']*constants.AVG_PTS_WEIGHT + stats['home_pts_allowed']*constants.AVG_PTS_ALLOWED_WEIGHT
    spread = round(abs(home_score - away_score), constants.SPREAD_DECIMALS)

    home_score = round(home_score, constants.SCORE_DECIMALS)
    away_score = round(away_score, constants.SCORE_DECIMALS)

    if (constants.SCORE_DECIMALS == 0):
        home_score = int(home_score)
        away_score = int(away_score)
    if (constants.SPREAD_DECIMALS == 0):
        spread = int(spread)

    if (home_score > away_score):
        winner = home_team
    elif (away_score > home_score):
        winner = away_team
    else:
        winner = 'TIE'

    return {
            "away_score": away_score,
            "home_score": home_score,
            "winner": winner,
            "spread": spread
           }

def display_predictions(home_team, away_team, predictions):
    spread = str(predictions['spread'])
    if (predictions['home_score'] > predictions['away_score']):
        home_spread = '(-' + spread + ')'
        away_spread = '(+' + spread + ')'
    else:
        home_spread = '(+' + spread + ')'
        away_spread = '(-' + spread + ')'

    print(away_team +' @ '+ home_team)
    print( '{:<6s} {:<15s} {:<5s}'.format(away_spread, away_team, str(predictions['away_score'])) )
    print( '{:<6s} {:<15s} {:<5s}'.format(home_spread, home_team, str(predictions['home_score'])) )
    print( '{:<22s} {:<5s}'.format('Combined Score ', str(predictions['home_score'] + predictions['away_score'])))
    print('\n')

def clean_name(team):
    # special cases
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
        return team[:-3].strip() # remove abbreviations

main()
