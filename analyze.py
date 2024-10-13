from logging_config import setup_logger
import os
import re
import sqlite3

logger = setup_logger('analyze.py')
logger.info('Starting analyze.py...')

stop_words = {
    '-', '–', 'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
    'and', 'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been',
    'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can',
    'can\'t', 'come', 'could', 'did', 'do', 'does', 'doing', 'down', 'during',
    'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having',
    'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers',
    'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d',
    'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it',
    'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'my', 'myself',
    'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
    'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she',
    'she\'d', 'she\'ll', 'she\'s', 'should', 'so', 'some', 'such', 'than',
    'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
    'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve',
    'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very',
    'was', 'we', 'were', 'what', 'what\'s', 'when', 'when\'s', 'where',
    'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s',
    'with', 'won\'t', 'would', 'you', 'you\'d', 'you\'ll', 'you\'re',
    'you\'ve', 'your', 'yours', 'yourself', 'yourselves'
}

def clean_text(text):
    alpha_numeric_only = re.sub(r'\W+', ' ', text)
    return [word for word in alpha_numeric_only.split() if word.lower() not in stop_words]

def find_third_slash_position(string):
    position = -1
    for _ in range(3):
        position = string.find('/', position + 1)
        if position == -1:
            return -1  # Return -1 if there are fewer than three slashes
    return position

db_path = os.path.abspath('hackernews.sqlite')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
words_cur = conn.cursor()
urls_cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT,
            count INTEGER DEFAULT 0)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            count INTEGER DEFAULT 0)''')

articles_to_update = []
cur.execute('''SELECT * FROM Articles WHERE processed = 0''')
for record in cur:
    id = record[0]
    third_slash_position = find_third_slash_position(record[1])
    host = record[1][:third_slash_position]
    words = clean_text(record[2])
    logger.info(f'Looping {host} {words}')

    for word in words:
        words_cur.execute('SELECT id, count FROM Words WHERE word = ?', (word,))
        result = words_cur.fetchone()

        if result:
            # Word was added previously, update the count
            word_id, word_count = result
            logger.info(f'Duplicate word, updating count... {word_id} {word} {word_count}')
            words_cur.execute('UPDATE Words SET count = ? WHERE id = ?', (word_count + 1, word_id))
        else:
            logger.info(f'New word, adding to Words {word}')
            # new word found, add it with a count of 0
            words_cur.execute('INSERT INTO Words (word, count) VALUES (?, ?)', (word, 1))

    urls_cur.execute('SELECT * FROM Urls WHERE url = ?', (host, ))
    url_record = urls_cur.fetchone()
    if url_record:
        url_id = url_record[0]
        count = url_record[2]
        urls_cur.execute('UPDATE Urls SET count = ? WHERE id = ?', (count + 1, url_id))
    else:
        urls_cur.execute('INSERT INTO Urls (url, count) VALUES (?, ?)', (host, 1))

    articles_to_update.append(id)

conn.commit()

for article_id in articles_to_update:
    logger.info(f'Updating Article ID {article_id} to processed DONE')
    cur.execute('UPDATE Articles SET processed = ? WHERE id = ?', (1, article_id))

conn.commit()

logger.info('Finished reading urls and key words from article titles. Exiting analyze.py...')

words_cur.close()
urls_cur.close()
cur.close()
conn.close()
