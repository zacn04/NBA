from accumulate import Scraper
import pandas
scraper = Scraper()


#Need some optimisation/preprocessing for the scraper.get function so that 
#I don't have to further optimise
def gettwoteams(team1=None, team2=None, year=1949) -> tuple[pandas.DataFrame, pandas.DataFrame]:
    df = scraper.get(f'https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html')
    #Beware of rate limits
    for index, row in df.iterrows():
        if row[0] == team1:
            t1d = row.to_frame().T
        elif row[0] == team2:
            t2d = row.to_frame().T
    return t1d, t2d

print(gettwoteams('Los Angeles Lakers', 'Miami Heat', 2016))
