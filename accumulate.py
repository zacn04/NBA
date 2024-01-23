import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scraper():
    def __init__(self):
        pass
    def get(self, url):
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table by class name
        table = soup.find('table')

        # Check if the table is found
        if table:
            data_rows = []
            tbody = table.find('tbody')
            if tbody:
                for row in tbody.find_all('tr'):
                    # Extract data
                    row_data = [td.text.strip() for td in row.find_all('td')]
                    data_rows.append(row_data)

                df = pd.DataFrame(data_rows)
                url = url.split('/')[-1]
                df.to_csv(f'output{url[8:-5]}.csv', index=False)

                return df
            else:
                return -1
        else:
            return -2


scraper = Scraper()
scraper.get('https://www.basketball-reference.com/leagues/NBA_2023_per_game.html')
