from accumulate import Scraper
import pandas as pd
scraper = Scraper()

teamabbrev = {
    'Boston Celtics': 'BOS',
    'Milwaukee Bucks': 'MIL',
    'New York Knicks': 'NYK',
    'Cleveland Cavaliers': 'CLE',
    'Philadelphia 76ers': 'PHI',
    'Indiana Pacers': 'IND',
    'Miami Heat': 'MIA',
    'Orlando Magic': 'ORL',
    'Chicago Bulls': 'CHI',
    'Atlanta Hawks': 'ATL',
    'Brooklyn Nets': 'BRK',
    'Toronto Raptors': 'TOR',
    'Charlotte Hornets': 'CHO',
    'Washington Wizards': 'WAS',
    'Detroit Pistons': 'DET',
    'Oklahoma City Thunder': 'OKC',
    'Minnesota Timberwolves': 'MIN',
    'Los Angeles Clippers': 'LAC',
    'Denver Nuggets': 'DEN',
    'Sacramento Kings': 'SAC',
    'New Orleans Pelicans': 'NOP',
    'Phoenix Suns': 'PHO',
    'Dallas Mavericks': 'DAL',
    'Los Angeles Lakers': 'LAL',
    'Utah Jazz': 'UTA',
    'Houston Rockets': 'HOU',
    'Golden State Warriors': 'GSW',
    'Memphis Grizzlies': 'MEM',
    'Portland Trail Blazers': 'POR',
    'San Antonio Spurs': 'SAS'
}


def gettwoteams(team1=None, team2=None, year=1949) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = scraper.get(f'https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html')
    if type(df) == int:
        print(df)
    #Beware of rate limits
    for index, row in df.iterrows():
        if row[0] == team1:
            t1d = row.to_frame().T
        elif row[0] == team2:
            t2d = row.to_frame().T
    return t1d, t2d

#print(gettwoteams('Los Angeles Lakers', 'Miami Heat', 2016))

def getfaceoffs(team1=None, team2=None, year=1949):
    data = scraper.get(f'https://www.basketball-reference.com/teams/{teamabbrev[team1]}/{year}_games.html')
    data.columns = ['Date', 'Start', 'Yeah', 'Type', 'H/A', 'Opponent', 'Result', 'OT', 'Tm', 'Opp', 'W', 'L', 'Streak', 'Notes']
    ans = []
    for index, row in data.iterrows():
        print(row)
        if row['Opponent'] == team2:  
            if row['Result'] == 'W':
                ans.append(1)
            elif row['Result'] == 'L':
                ans.append(0)
    return ans


def gettwoteamsgeneral(team1=None, team2=None, start=1949, end=2024):
    data1, data2, faceoffs = pd.DataFrame(), pd.DataFrame(), [] #TODO: specify columns
    for year in range(start, end):
        x,y = gettwoteams(team1, team2, year)
        z = getfaceoffs(team1, team2, year)
        data1 = pd.concat([data1, x], ignore_index=True)
        data2 = pd.concat([data2, y], ignore_index=True)
        faceoffs.append(z)
    return data1, data2, faceoffs


def final_dataset(team1, team2, start, end):
    dfA, dfB, outcomes = gettwoteamsgeneral(team1, team2, start, end)
    outcomes = pd.DataFrame(outcomes)
    dfA.insert(3, 'Year', range(start, end))
    dfB.insert(3, 'Year', range(start, end))
    outcomes.insert(1, 'Year', range(start,end))
    df = pd.merge(dfA, dfB, on='Year', how='inner')
    df = pd.merge(df, outcomes, on='Year', how='inner')

print(final_dataset('Boston Celtics', 'Miami Heat', 2001, 2024))





