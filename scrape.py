from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sqlite3

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch {url}")

def fetch_cached_html():
    with open('cache.html', 'r') as html:
        return html.read()

def parse_article_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_spans = soup.find_all('span', 'titleline')

    return [(span.contents[0].get('href'), span.contents[0].contents[0]) for span in title_spans]

def save_to_database(links, db_path='hackernews.sqlite'):
    now = datetime.now()
    now_formatted = now.isoformat()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Articles
                (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, title TEXT,
                shared_date TEXT)''') # using ISO8601 datetime string as sqlite3 doesn't support datetimez

    # each link is a tuple of article_url and article_title
    for link in links:
        cur.execute('INSERT INTO Articles (url, title, shared_date) VALUES (?, ?, ?)', (link[0], link[1], now_formatted))

    conn.commit()
    conn.close()

def main():
    url = "https://news.ycombinator.com"
    html = fetch_html(url)
    # html = fetch_cached_html()
    articles = parse_article_info(html)
    save_to_database(articles)
    print('finished saving to db... exiting')

if __name__ == '__main__':
    main()
