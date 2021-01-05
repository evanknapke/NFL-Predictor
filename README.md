# NFL-Predictor
Pulls live stats from the web to predict outcomes of the upcoming schedule.

## Dependencies:
- Python 3+ (3.7.3 tested)
- Pandas (`pip install pandas`)

## How To

### Run the project:
1. Download/clone project
2. cd into the NFL-Predictor directory
3. Run `python nfl_predictor.py`
4. Results will be printed to the console if SAVE_TO_TXT constant is false

### Save results to a .txt file:
1. Open [constants.py](./constants.py) in a text editor
2. Change SAVE_TO_TXT to `True`
3. Edit FILENAME to change the .txt filename
4. Save [constants.py](./constants.py)

### Change the decimals to be rounded:
1. Open [constants.py](./constants.py) in a text editor
2. Change SCORE_DECIMALS variable to the amount of decimals you want for the scores and combined totals
3. Change SPREAD_DECIMALS variable to the amount of decimals you want for the spread
4. Save [constants.py](./constants.py)

### Adjust the results:
1. Open [constants.py](./constants.py) in a text editor
2. Change AVG_PTS_WEIGHT to a float between 1.0 and 0.0
3. You can optional change the AVG_PTS_ALLOWED_WEIGHT as well, however it is recommended to leave it so that the 2 equal 100%
4. Save [constants.py](./constants.py)
