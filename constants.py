GET_NEW_WEIGHTS = False # boolean, False to not calculate a new weight

TRAINING_SCHEDULE_URL = 'https://www.espn.com/nfl/schedule/_/week/16/seasontype/2' # for training
UPCOMING_SCHEDULE_URL = 'https://www.espn.com/nfl/schedule/' # for upcoming games

AVG_PTS_URL = 'https://www.teamrankings.com/nfl/stat/points-per-game'
AVG_PTS_ALLOWED_URL = 'https://www.teamrankings.com/nfl/stat/opponent-points-per-game'

SAVE_TO_TXT = False # boolean, False to print to console, True to save to .txt in out folder
FILENAME = 'results' # string, used as filename if SAVE_TO_TXT is True

SCORE_DECIMALS = 0 # int, 0 for no decimals in rounding
SPREAD_DECIMALS = 1 # int, 0 for no decimals in rounding

AVG_PTS_WEIGHT =  0.61 # float 1.0 to 0.0, update this after training
AVG_PTS_ALLOWED_WEIGHT = 1 - AVG_PTS_WEIGHT # opposite of AVG_PTS_WEIGHT to equal 100%
