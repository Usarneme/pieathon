from bs4 import BeautifulSoup
from datetime import datetime
import logging
import os
import requests
import sqlite3

# Configure logging
logging.basicConfig(filename='/Users/usarneme/Library/Logs/hackernews_scraper.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        logging.error(f"Failed to fetch {url}")
        raise Exception(f"Failed to fetch {url}")

def fetch_cached_html():
    with open('cache.html', 'r') as html:
        return html.read()

def parse_article_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_spans = soup.find_all('span', 'titleline')

    return [(span.contents[0].get('href'), span.contents[0].contents[0]) for span in title_spans]

def save_to_database(links):
    db_path = os.path.abspath('hackernews.sqlite')
    now = datetime.now()
    now_formatted = now.isoformat()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Articles
                (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, title TEXT,
                shared_date TEXT)''') # using ISO8601 datetime string as sqlite3 doesn't support datetimez

    # each link is a tuple of article_url and article_title
    for link in links:
        # only allow saving new/unique article URLs with the try/except
        try:
            cur.execute('INSERT INTO Articles (url, title, shared_date) VALUES (?, ?, ?)', (link[0], link[1], now_formatted))
            conn.commit()
        except sqlite3.IntegrityError:
            logging.error(f"Url already exists: {link[0]}. Skipping save...")
            print(f"Url already exists: {link[0]}. Skipping save...")

    conn.commit()
    cur.close()
    conn.close()

def main():
    url = "https://news.ycombinator.com"
    html = fetch_html(url)
    # html = fetch_cached_html()
    articles = parse_article_info(html)
    save_to_database(articles)
    logging.info('finished saving to db... exiting')

if __name__ == '__main__':
    main()
