import requests
from bs4 import BeautifulSoup
import csv


def main():
    url_list =['https://www.espn.com/nba/salaries']
    for i in range(2,12): # The web has only 12 pages
            url_list.append('https://www.espn.com/nba/salaries/_/page/'+str(i))
    players_data = []
    for url in url_list:
        temp_players_data = scrape_nba_player_salaries(url)
        players_data = players_data + temp_players_data

    csv_file_name = 'nba_player_salaries.csv'
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Ranking', 'Name', 'Position', 'Team', 'Salary'])
        writer.writerows(players_data)
    print(f'Data successfully saved to {csv_file_name}')


def scrape_nba_player_salaries(url):
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Make a request to get the HTML content with headers
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML

    player_data = []
    rows = soup.find_all('tr', class_=['oddrow', 'evenrow'])  # find all player rows

    for row in rows:  # Loop Over Players
        columns = row.find_all('td')
        ranking = columns[0].text.strip()
        name_position = columns[1].text.strip()  # Name and position are in the same column
        name, position = name_position.rsplit(' ', 1)  # Separate into two variables
        team = columns[2].text.strip()
        salary = columns[3].text.strip()
        salary_int = int(salary.replace('$', '').replace(',', ''))
        player_data.append([ranking, name, position, team, salary_int])
    
    return player_data



main()