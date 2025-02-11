import random
import joblib
import pandas as pd
import numpy as np
import time
import requests
import sqlite3
import pickle



def season_fixtures(years):
    
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october-2019', 'october-2020', 'october', 'november', 'december']

    fixtures = pd.DataFrame()

    for year in years:

        for month in months:

            try:
                time.sleep(2)
                url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_games-' + month + '.html'

                tables = pd.read_html(url)
                usable = tables[0].dropna(subset=['PTS'])
                fixtures = pd.concat([fixtures, usable[['Date', 'Home/Neutral']]]).reset_index(drop=True)
            except:
                continue

    return fixtures

def key_code_constructor(fixtures, month_dict, team_dict):

    fixture_key_code = []

    for _, row in fixtures.iterrows():

        year = row['Date'][-4:]
        month = month_dict[row['Date'][5:8]]
        day = row['Date'][-8:-6]
        date = str(np.where(len(str(int(day)))==1,'0'+str(int(day)),str(int(day))))
        filler = '0'
        team = team_dict[row['Home/Neutral']]

        keycode = year+month+date+filler+team

        fixture_key_code.append(keycode)

    return fixture_key_code

def game_scraper(game):

    boxscoreurl = 'https://www.basketball-reference.com/boxscores/' + game + '.html'
    pbpurl = 'https://www.basketball-reference.com/boxscores/pbp/' + game + '.html'

    bstables = pd.read_html(boxscoreurl)
    astarters = bstables[1].head(5).iloc[:, 0].values.tolist()
    hstarters = bstables[-1].head(5).iloc[:, 0].values.tolist()
    time.sleep(2)
    pbptables = pd.read_html(pbpurl)
    pbp = pbptables[0]

    game_dict = {
        game: {
            'AwayStarters': astarters,
            'HomeStarters': hstarters,
            'PlayByPlay': pbp
        }
    }
    return game_dict

def master_scraper(years, month_dict, team_dict):

    starttime = time.time()
    num_years = len(years)
    fixtures = season_fixtures(years)

    key_codes = key_code_constructor(fixtures, month_dict, team_dict)
    num_games = len(key_codes)

    gamesperyear = int(num_games / num_years)

    master_dict = {}

    for key_code in key_codes:

        master_dict[key_code] = game_scraper(key_code)

        if key_codes.index(key_code) % gamesperyear == 0:
            print(f'Season Checkpoint: ~{int((time.time() - starttime)/60)} minutes elapsed')


    return master_dict

month_dict = {

    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'

}

team_dict = {

    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BRK',
    'Charlotte Hornets': 'CHO',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'Los Angeles Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHO',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'

}

master_dict = master_scraper([2020,2021,2022,2023,2024], month_dict, team_dict)

conn = sqlite3.connect("nba_play_by_play.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data BLOB
    )
""")
conn.commit()
serialized_dict = pickle.dumps(master_dict)
cursor.execute("INSERT INTO game_data (data) VALUES (?)", (serialized_dict,))
conn.commit()

conn.close()