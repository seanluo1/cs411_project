import requests
from bs4 import BeautifulSoup
import sqlite3

def get_db():
    db = sqlite3.connect('instance/app.sqlite')
    db.row_factory = sqlite3.Row

    return db

db = get_db()

#setup web scraper
url = 'https://en.wikipedia.org/wiki/Rolling_Stone_100_Best_Songs_of_the_Decade'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

#find specific table and rows in scraped web page
table = soup.find('table')
table_body = table.find('tbody')
rows = table.find_all('tr')

#add all songs to db
for i in range(1, len(rows)):
    row = rows[i]
    cols = row.find_all('td')
    cols = [elem.text.strip() for elem in cols]

    song_name = cols[1]
    genre = cols[2]
    link = 'https://en.wikipedia.org' + row.select_one('a')['href']

    db.execute(
        'INSERT INTO Song (SongName, Genre, Song_Url) VALUES (?,?,?)',
        (song_name, genre, link)
    )

db.commit()
db.close()
