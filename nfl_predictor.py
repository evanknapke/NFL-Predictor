import constants
import pandas as pd
import requests
import sys
import weight

def main():
    matchups_df = save_to_df(constants.SCHEDULE_URL)
    pts_df = save_to_df(constants.AVG_PTS_URL)
    pts_allowed_df = save_to_df(constants.AVG_PTS_ALLOWED_URL)
    new_weight = 0.0
    overall_new_weight = 0.0
    for i in range(matchups_df.shape[0]): # length of rows in df
        home_team = clean_name(matchups_df.iloc[i][1])
        away_team = clean_name(matchups_df.iloc[i][0])
        stats = get_matchup_stats(home_team, away_team, pts_df, pts_allowed_df)

        if (constants.SAVE_TO_TXT):
            sys.stdout = open(constants.FILENAME+'.txt', 'a')
            new_weight = display_predictions(home_team, away_team, stats)
            sys.stdout.close()
        else:
            new_weight = display_predictions(home_team, away_team, stats)

        overall_new_weight += new_weight
    overall_new_weight = overall_new_weight/matchups_df.shape[0]
    if (overall_new_weight != 0):
        print(overall_new_weight)

# TODO rewrite these into 1 function to take in all tables on the page
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

# TODO: clean and break this up into new functions
def display_predictions(home_team, away_team, stats):
    home_total = stats['home_avg_pts']*constants.AVG_PTS_WEIGHT + stats['away_pts_allowed']*constants.AVG_PTS_ALLOWED_WEIGHT
    away_total = stats['away_avg_pts']*constants.AVG_PTS_WEIGHT + stats['home_pts_allowed']*constants.AVG_PTS_ALLOWED_WEIGHT
    combined_total = round( (home_total + away_total), constants.SCORE_DECIMALS)
    difference = round(abs(home_total - away_total), constants.SPREAD_DECIMALS)

    home_total = round(home_total, constants.SCORE_DECIMALS)
    away_total = round(away_total, constants.SCORE_DECIMALS)

    if (constants.SCORE_DECIMALS == 0):
        home_total = int(home_total)
        away_total = int(away_total)
        combined_total = int(combined_total)
    if (constants.SPREAD_DECIMALS == 0):
        difference = int(difference)

    if (home_total > away_total):
        winner = home_team
    elif (away_total > home_total):
        winner = away_team
    else:
        winner = 'TIE'

    print(away_team + ' @ ' + home_team)
    print(str(away_total) + ' - ' + str(home_total) + ' ('+winner+' -'+str(difference)+')')
    print('Total pts: ' + str(combined_total))
    print('\n')

    if (constants.GET_NEW_WEIGHTS):
        new_weight = weight.find_new_weights(home_team, away_team, home_total, away_total, stats, AVG_PTS_WEIGHT)
    else:
        new_weight = 0

    return(new_weight)

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
